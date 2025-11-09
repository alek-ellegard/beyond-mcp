#!/usr/bin/env python3
"""
Kalshi MCP Server

MCP server that wraps the Kalshi CLI, providing one-to-one tool mappings
for each CLI command. All tools call the underlying CLI via subprocess.

Usage:
    uv run mcp dev server.py
    uv run mcp install server.py
"""

import json
import subprocess
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP(
    "Kalshi Prediction Markets",
    instructions="Access Kalshi prediction market data including markets, events, series, trades, and more. "
    "All data is read-only and requires no authentication.",
)

# Path to the CLI project
CLI_PATH = Path(__file__).parent.parent / "2_cli"


def run_kalshi_cli(*args) -> dict:
    """
    Execute kalshi CLI command and return parsed JSON output.

    Args:
        *args: CLI arguments to pass to kalshi command

    Returns:
        Parsed JSON output from the CLI

    Raises:
        RuntimeError: If CLI command fails
    """
    cmd = ["uv", "run", "kalshi", *args, "--json"]
    try:
        result = subprocess.run(
            cmd,
            cwd=CLI_PATH,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"CLI command failed: {e.stderr}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse CLI output: {e}") from e


# ========================================
# Exchange Status
# ========================================


@mcp.tool()
def get_exchange_status() -> dict:
    """
    Get the current Kalshi exchange status.

    Returns exchange_active, trading_active, and estimated_resume_time.
    """
    return run_kalshi_cli("status")


# ========================================
# Market Tools
# ========================================


@mcp.tool()
def list_markets(
    limit: int = 10,
    status: str = "open",
    event_ticker: Optional[str] = None,
    series_ticker: Optional[str] = None,
    tickers: Optional[str] = None,
    mve_filter: Optional[str] = None,
    cursor: Optional[str] = None,
) -> dict:
    """
    List Kalshi markets with various filters.

    Args:
        limit: Number of markets to return (1-1000, default: 10)
        status: Market status filter - 'open', 'closed', 'settled', or comma-separated
        event_ticker: Filter by event ticker
        series_ticker: Filter by series ticker
        tickers: Filter by market tickers (comma-separated)
        mve_filter: Multivariate events filter - 'only' or 'exclude'
        cursor: Pagination cursor for next page

    Returns:
        Dict with 'markets' array and optional 'cursor' for pagination
    """
    args = ["markets", "--limit", str(limit), "--status", status]
    if event_ticker:
        args.extend(["--event-ticker", event_ticker])
    if series_ticker:
        args.extend(["--series-ticker", series_ticker])
    if tickers:
        args.extend(["--tickers", tickers])
    if mve_filter:
        args.extend(["--mve-filter", mve_filter])
    if cursor:
        args.extend(["--cursor", cursor])

    return run_kalshi_cli(*args)


@mcp.tool()
def get_market(ticker: str) -> dict:
    """
    Get detailed information for a specific market.

    Args:
        ticker: Market ticker symbol (e.g., 'KXBTCD-25NOV0612-T102499.99')

    Returns:
        Complete market details including prices, volume, status, and metadata
    """
    return run_kalshi_cli("market", ticker)


@mcp.tool()
def get_market_orderbook(ticker: str, depth: int = 10) -> dict:
    """
    Get the orderbook for a specific market.

    Args:
        ticker: Market ticker symbol
        depth: Orderbook depth (0 = all levels, 1-100 for specific depth, default: 10)

    Returns:
        Dict with 'orderbook' containing yes/no bid arrays
    """
    return run_kalshi_cli("orderbook", ticker, "--depth", str(depth))


@mcp.tool()
def search_markets(keyword: str, limit: int = 10) -> dict:
    """
    Search markets by keyword using cached data.

    Searches across market titles, subtitles, and series names.
    First search builds cache (~2-5 min), subsequent searches are instant.

    Args:
        keyword: Search keyword
        limit: Max results to return (default: 10)

    Returns:
        Dict with matching markets
    """
    return run_kalshi_cli("search", keyword, "--limit", str(limit))


@mcp.tool()
def get_recent_trades(
    limit: int = 10,
    ticker: Optional[str] = None,
    min_ts: Optional[int] = None,
    max_ts: Optional[int] = None,
    cursor: Optional[str] = None,
) -> dict:
    """
    Get recent trades across markets or for a specific market.

    Args:
        limit: Number of trades to return (1-1000, default: 10)
        ticker: Filter trades for specific market ticker
        min_ts: Filter trades after this Unix timestamp
        max_ts: Filter trades before this Unix timestamp
        cursor: Pagination cursor

    Returns:
        Dict with 'trades' array and optional 'cursor'
    """
    args = ["trades", "--limit", str(limit)]
    if ticker:
        args.extend(["--ticker", ticker])
    if min_ts is not None:
        args.extend(["--min-ts", str(min_ts)])
    if max_ts is not None:
        args.extend(["--max-ts", str(max_ts)])
    if cursor:
        args.extend(["--cursor", cursor])

    return run_kalshi_cli(*args)


@mcp.tool()
def get_market_candlesticks(
    series_ticker: str,
    market_ticker: str,
    start_ts: int,
    end_ts: int,
    interval: int = 60,
) -> dict:
    """
    Get candlestick data for a specific market.

    Args:
        series_ticker: Series ticker containing the market
        market_ticker: Market ticker
        start_ts: Start timestamp (Unix timestamp)
        end_ts: End timestamp (Unix timestamp)
        interval: Period interval in minutes - 1 (1min), 60 (1hr), 1440 (1day)

    Returns:
        Dict with 'ticker' and 'candlesticks' array
    """
    return run_kalshi_cli(
        "market-candles",
        series_ticker,
        market_ticker,
        "--start-ts",
        str(start_ts),
        "--end-ts",
        str(end_ts),
        "--interval",
        str(interval),
    )


# ========================================
# Event Tools
# ========================================


@mcp.tool()
def list_events(
    limit: int = 10,
    status: Optional[str] = None,
    series_ticker: Optional[str] = None,
    with_markets: bool = False,
    with_milestones: bool = False,
    cursor: Optional[str] = None,
) -> dict:
    """
    List Kalshi events (collections of related markets).

    Args:
        limit: Number of events to return (1-200, default: 10)
        status: Event status filter - 'open', 'closed', 'settled'
        series_ticker: Filter by series ticker
        with_markets: Include nested markets in response
        with_milestones: Include related milestones
        cursor: Pagination cursor

    Returns:
        Dict with 'events' array, optional 'milestones', and 'cursor'
    """
    args = ["events", "--limit", str(limit)]
    if status:
        args.extend(["--status", status])
    if series_ticker:
        args.extend(["--series-ticker", series_ticker])
    if with_markets:
        args.append("--with-markets")
    if with_milestones:
        args.append("--with-milestones")
    if cursor:
        args.extend(["--cursor", cursor])

    return run_kalshi_cli(*args)


@mcp.tool()
def get_event(event_ticker: str, with_markets: bool = False) -> dict:
    """
    Get detailed information for a specific event.

    Args:
        event_ticker: Event ticker (e.g., 'KXELONMARS-99')
        with_markets: Include nested markets in the response

    Returns:
        Dict with 'event' object and 'markets' array
    """
    args = ["event", event_ticker]
    if with_markets:
        args.append("--with-markets")

    return run_kalshi_cli(*args)


@mcp.tool()
def list_multivariate_events(
    limit: int = 10,
    series_ticker: Optional[str] = None,
    collection_ticker: Optional[str] = None,
    with_markets: bool = False,
    cursor: Optional[str] = None,
) -> dict:
    """
    Get multivariate (combo) events.

    Args:
        limit: Number of events to return (1-200, default: 10)
        series_ticker: Filter by series ticker
        collection_ticker: Filter by collection ticker
        with_markets: Include nested markets
        cursor: Pagination cursor

    Returns:
        Dict with 'events' array and 'cursor'
    """
    args = ["multivariate", "--limit", str(limit)]
    if series_ticker:
        args.extend(["--series-ticker", series_ticker])
    if collection_ticker:
        args.extend(["--collection-ticker", collection_ticker])
    if with_markets:
        args.append("--with-markets")
    if cursor:
        args.extend(["--cursor", cursor])

    return run_kalshi_cli(*args)


@mcp.tool()
def get_event_candlesticks(
    series_ticker: str,
    event_ticker: str,
    start_ts: int,
    end_ts: int,
    interval: int = 60,
) -> dict:
    """
    Get candlestick data aggregated across all markets in an event.

    Args:
        series_ticker: Series ticker
        event_ticker: Event ticker
        start_ts: Start timestamp (Unix timestamp)
        end_ts: End timestamp (Unix timestamp)
        interval: Period interval in minutes - 1, 60, or 1440

    Returns:
        Dict with 'market_tickers', 'market_candlesticks', and 'adjusted_end_ts'
    """
    return run_kalshi_cli(
        "event-candles",
        series_ticker,
        event_ticker,
        "--start-ts",
        str(start_ts),
        "--end-ts",
        str(end_ts),
        "--interval",
        str(interval),
    )


# ========================================
# Series Tools
# ========================================


@mcp.tool()
def list_series(
    category: Optional[str] = None,
    tags: Optional[str] = None,
    with_metadata: bool = False,
) -> dict:
    """
    List all available series (market templates).

    Returns ~6900 series! Use filters to narrow results.

    Args:
        category: Filter by category (e.g., 'Politics', 'Economics')
        tags: Filter by tags (comma-separated)
        with_metadata: Include product metadata

    Returns:
        Dict with 'series' array containing all matching series
    """
    args = ["series-list"]
    if category:
        args.extend(["--category", category])
    if tags:
        args.extend(["--tags", tags])
    if with_metadata:
        args.append("--with-metadata")

    return run_kalshi_cli(*args)


@mcp.tool()
def get_series(series_ticker: str) -> dict:
    """
    Get detailed information about a specific series.

    Args:
        series_ticker: Series ticker (e.g., 'KXHIGHNY')

    Returns:
        Dict with 'series' object containing metadata, settlement sources, etc.
    """
    return run_kalshi_cli("series", series_ticker)


# ========================================
# Main Entry Point
# ========================================


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
