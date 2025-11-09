#!/usr/bin/env python3
"""
Kalshi CLI - Command-line interface for Kalshi Prediction Markets

Built on direct HTTP API access for clean, reliable market data queries.
All commands consolidated in a single file for simplicity and clarity.
"""

import click
import json
import sys
from kalshi_cli.modules.client import KalshiClient, KalshiSearchCache
from kalshi_cli.modules.formatting import (
    json_serial,
    format_market_summary,
    print_market_detail,
    print_event_detail,
    format_timestamp,
)


@click.group()
@click.pass_context
def cli(ctx):
    """
    Kalshi Prediction Markets CLI

    Query market data, events, series, and trades from Kalshi's public API.
    No authentication required for read-only access.

    Examples:
      kalshi markets --limit 5
      kalshi search "election"
      kalshi market TICKER
      kalshi events --status open
    """
    ctx.ensure_object(dict)
    try:
        ctx.obj['client'] = KalshiClient()
    except Exception as e:
        click.echo(f"❌ Failed to initialize Kalshi client: {e}", err=True)
        sys.exit(1)


# ========================================
# Exchange Status Command
# ========================================

@cli.command()
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def status(ctx, output_json):
    """Get exchange status (trading hours, maintenance, etc.)"""
    try:
        client = ctx.obj['client']
        result = client.get_exchange_status()

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            click.echo(f"\nExchange Status:")
            click.echo(f"  Exchange Active: {result.get('exchange_active', 'N/A')}")
            click.echo(f"  Trading Active: {result.get('trading_active', 'N/A')}")
            if result.get('exchange_estimated_resume_time'):
                click.echo(f"  Estimated Resume: {result.get('exchange_estimated_resume_time')}")
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


# ========================================
# Market Commands
# ========================================

@cli.command()
@click.option('--limit', default=10, help='Number of markets to return (1-1000)')
@click.option('--status', default='open', help='Market status (open, closed, settled, or comma-separated)')
@click.option('--event-ticker', help='Filter by event ticker')
@click.option('--series-ticker', help='Filter by series ticker')
@click.option('--tickers', help='Filter by market tickers (comma-separated)')
@click.option('--mve-filter', type=click.Choice(['only', 'exclude']), help='Multivariate events filter')
@click.option('--cursor', help='Pagination cursor')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def markets(ctx, limit, status, event_ticker, series_ticker, tickers, mve_filter, cursor, output_json):
    """List markets with various filters"""
    try:
        client = ctx.obj['client']
        result = client.get_markets(
            limit=limit,
            status=status,
            cursor=cursor,
            event_ticker=event_ticker,
            series_ticker=series_ticker,
            tickers=tickers,
            mve_filter=mve_filter
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            markets_list = result.get('markets', [])
            cursor_val = result.get('cursor', '')

            click.echo(f"\nFound {len(markets_list)} markets:")
            click.echo()

            for i, market in enumerate(markets_list, 1):
                click.echo(f"{i}. {format_market_summary(market)}")

            if cursor_val:
                click.echo(f"\n📄 More results available. Use --cursor {cursor_val[:20]}...")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('ticker')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def market(ctx, ticker, output_json):
    """Get detailed information for a specific market"""
    try:
        client = ctx.obj['client']
        result = client.get_market(ticker)

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            market_data = result.get('market', result)
            print_market_detail(market_data)

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('ticker')
@click.option('--depth', default=10, help='Orderbook depth (0=all, 1-100 for specific depth)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def orderbook(ctx, ticker, depth, output_json):
    """Get orderbook for a specific market"""
    try:
        client = ctx.obj['client']
        result = client.get_market_orderbook(ticker, depth=depth)

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            orderbook_data = result.get('orderbook', {})
            yes_orders = orderbook_data.get('yes', [])
            no_orders = orderbook_data.get('no', [])

            click.echo(f"\n{'='*60}")
            click.echo(f"Orderbook for {ticker}")
            click.echo(f"{'='*60}")

            click.echo("\nYES Side (Bids):")
            click.echo(f"{'Price':<10} {'Quantity':<15} {'Count':<10}")
            click.echo("-" * 40)
            if yes_orders:
                for order in yes_orders[:depth if depth > 0 else len(yes_orders)]:
                    if len(order) >= 2:
                        click.echo(f"{order[0]:<10} {order[1]:<15}")
            else:
                click.echo("  (no orders)")

            click.echo("\nNO Side (Bids):")
            click.echo(f"{'Price':<10} {'Quantity':<15} {'Count':<10}")
            click.echo("-" * 40)
            if no_orders:
                for order in no_orders[:depth if depth > 0 else len(no_orders)]:
                    if len(order) >= 2:
                        click.echo(f"{order[0]:<10} {order[1]:<15}")
            else:
                click.echo("  (no orders)")

            click.echo()

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--limit', default=10, help='Number of trades to return (1-1000)')
@click.option('--ticker', help='Filter trades for specific market')
@click.option('--min-ts', type=int, help='Filter trades after this Unix timestamp')
@click.option('--max-ts', type=int, help='Filter trades before this Unix timestamp')
@click.option('--cursor', help='Pagination cursor')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def trades(ctx, limit, ticker, min_ts, max_ts, cursor, output_json):
    """Get recent trades"""
    try:
        client = ctx.obj['client']
        result = client.get_trades(
            limit=limit,
            ticker=ticker,
            min_ts=min_ts,
            max_ts=max_ts,
            cursor=cursor
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            trades_list = result.get('trades', [])
            cursor_val = result.get('cursor', '')

            click.echo(f"\nFound {len(trades_list)} recent trades:")
            click.echo()

            for i, trade in enumerate(trades_list, 1):
                trade_ticker = trade.get('ticker', 'N/A')
                yes_price = trade.get('yes_price', 0)
                count = trade.get('count', 0)
                created = format_timestamp(trade.get('created_time', ''))

                click.echo(f"{i}. {trade_ticker}")
                click.echo(f"   Price: {yes_price}¢ | Contracts: {count} | Time: {created}")

            if cursor_val:
                click.echo(f"\n📄 More results available. Use --cursor {cursor_val[:20]}...")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('keyword')
@click.option('--limit', default=10, help='Max results to return')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def search(ctx, keyword, limit, output_json):
    """Search markets by keyword using cached data

    First search builds cache (~2-5 min), subsequent searches are instant!
    Cache refreshes every hour automatically.
    Searches: market titles, subtitles, series names
    """
    try:
        client = ctx.obj['client']

        # Use cached search - fast pandas-based searching
        # Pass quiet=True when JSON output is requested to suppress debug messages
        cache = KalshiSearchCache()
        results = cache.search(client, keyword, limit=limit, quiet=output_json)

        if output_json:
            click.echo(json.dumps(results, indent=2, default=json_serial))
        else:
            click.echo(f"\nFound {len(results)} markets matching '{keyword}':")
            click.echo()

            for i, market in enumerate(results, 1):
                click.echo(f"{i}. {format_market_summary(market)}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('series_ticker')
@click.argument('market_ticker')
@click.option('--start-ts', type=int, required=True, help='Start Unix timestamp')
@click.option('--end-ts', type=int, required=True, help='End Unix timestamp')
@click.option('--interval', type=click.Choice(['1', '60', '1440']), default='60', help='Period interval in minutes')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def market_candles(ctx, series_ticker, market_ticker, start_ts, end_ts, interval, output_json):
    """Get candlestick data for a market"""
    try:
        client = ctx.obj['client']
        result = client.get_market_candlesticks(
            series_ticker=series_ticker,
            market_ticker=market_ticker,
            start_ts=start_ts,
            end_ts=end_ts,
            period_interval=int(interval)
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            ticker = result.get('ticker', 'N/A')
            candles = result.get('candlesticks', [])

            click.echo(f"\nCandlestick data for {ticker}:")
            click.echo(f"Found {len(candles)} candlesticks")

            if candles:
                click.echo(f"\nFirst candlestick:")
                first = candles[0]
                price = first.get('price', {})
                click.echo(f"  Open: {price.get('open')}¢")
                click.echo(f"  High: {price.get('high')}¢")
                click.echo(f"  Low: {price.get('low')}¢")
                click.echo(f"  Close: {price.get('close')}¢")
                click.echo(f"  Volume: {first.get('volume', 0)}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


# ========================================
# Event Commands
# ========================================

@cli.command()
@click.option('--limit', default=10, help='Number of events to return (1-200)')
@click.option('--status', type=click.Choice(['open', 'closed', 'settled']), help='Event status filter')
@click.option('--series-ticker', help='Filter by series ticker')
@click.option('--with-markets', is_flag=True, help='Include nested markets')
@click.option('--with-milestones', is_flag=True, help='Include related milestones')
@click.option('--cursor', help='Pagination cursor')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def events(ctx, limit, status, series_ticker, with_markets, with_milestones, cursor, output_json):
    """List events (collections of related markets)"""
    try:
        client = ctx.obj['client']
        result = client.get_events(
            limit=limit,
            status=status,
            series_ticker=series_ticker,
            with_nested_markets=with_markets,
            with_milestones=with_milestones,
            cursor=cursor
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            events_list = result.get('events', [])
            cursor_val = result.get('cursor', '')

            click.echo(f"\nFound {len(events_list)} events:")
            click.echo()

            for i, event in enumerate(events_list, 1):
                event_ticker = event.get('event_ticker', 'N/A')
                title = event.get('title', 'N/A')
                category = event.get('category', 'N/A')

                click.echo(f"{i}. {event_ticker}")
                click.echo(f"   {title}")
                click.echo(f"   Category: {category}")

                if with_markets and event.get('markets'):
                    click.echo(f"   Markets: {len(event.get('markets', []))}")

                click.echo()

            if cursor_val:
                click.echo(f"📄 More results available. Use --cursor {cursor_val[:20]}...")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('event_ticker')
@click.option('--with-markets', is_flag=True, help='Include nested markets')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def event(ctx, event_ticker, with_markets, output_json):
    """Get detailed information for a specific event"""
    try:
        client = ctx.obj['client']
        result = client.get_event(event_ticker, with_nested_markets=with_markets)

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            print_event_detail(result)

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--limit', default=10, help='Number of multivariate events to return (1-200)')
@click.option('--series-ticker', help='Filter by series ticker')
@click.option('--collection-ticker', help='Filter by collection ticker')
@click.option('--with-markets', is_flag=True, help='Include nested markets')
@click.option('--cursor', help='Pagination cursor')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def multivariate(ctx, limit, series_ticker, collection_ticker, with_markets, cursor, output_json):
    """Get multivariate (combo) events"""
    try:
        client = ctx.obj['client']
        result = client.get_multivariate_events(
            limit=limit,
            series_ticker=series_ticker,
            collection_ticker=collection_ticker,
            with_nested_markets=with_markets,
            cursor=cursor
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            events_list = result.get('events', [])
            click.echo(f"\nFound {len(events_list)} multivariate events:")
            click.echo()

            for i, event in enumerate(events_list, 1):
                event_ticker = event.get('event_ticker', 'N/A')
                title = event.get('title', 'N/A')[:60]
                click.echo(f"{i}. {event_ticker}: {title}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('series_ticker')
@click.argument('event_ticker')
@click.option('--start-ts', type=int, required=True, help='Start Unix timestamp')
@click.option('--end-ts', type=int, required=True, help='End Unix timestamp')
@click.option('--interval', type=click.Choice(['1', '60', '1440']), default='60', help='Period interval in minutes')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def event_candles(ctx, series_ticker, event_ticker, start_ts, end_ts, interval, output_json):
    """Get candlestick data aggregated across all markets in an event"""
    try:
        client = ctx.obj['client']
        result = client.get_event_candlesticks(
            series_ticker=series_ticker,
            event_ticker=event_ticker,
            start_ts=start_ts,
            end_ts=end_ts,
            period_interval=int(interval)
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            market_tickers = result.get('market_tickers', [])
            click.echo(f"\nEvent candlesticks for {event_ticker}")
            click.echo(f"Markets included: {len(market_tickers)}")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


# ========================================
# Series Commands
# ========================================

@cli.command()
@click.option('--category', help='Filter by category')
@click.option('--tags', help='Filter by tags')
@click.option('--with-metadata', is_flag=True, help='Include product metadata')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def series_list(ctx, category, tags, with_metadata, output_json):
    """List all series with optional filters"""
    try:
        client = ctx.obj['client']
        result = client.get_series_list(
            category=category,
            tags=tags,
            include_product_metadata=with_metadata
        )

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            series_list_data = result.get('series', [])
            click.echo(f"\nFound {len(series_list_data)} series:")
            click.echo()

            for i, series in enumerate(series_list_data, 1):
                ticker = series.get('ticker', 'N/A')
                title = series.get('title', 'N/A')
                category = series.get('category', 'N/A')
                frequency = series.get('frequency', 'N/A')

                click.echo(f"{i}. {ticker}")
                click.echo(f"   {title}")
                click.echo(f"   Category: {category} | Frequency: {frequency}")
                click.echo()

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('series_ticker')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def series(ctx, series_ticker, output_json):
    """Get information about a specific series"""
    try:
        client = ctx.obj['client']
        result = client.get_series(series_ticker)

        if output_json:
            click.echo(json.dumps(result, indent=2, default=json_serial))
        else:
            series_data = result.get('series', {})

            click.echo(f"\n{'='*60}")
            click.echo(f"Series: {series_data.get('ticker', 'N/A')}")
            click.echo(f"{'='*60}")

            click.echo(f"\nTitle: {series_data.get('title', 'N/A')}")
            click.echo(f"Category: {series_data.get('category', 'N/A')}")
            click.echo(f"Frequency: {series_data.get('frequency', 'N/A')}")

            tags = series_data.get('tags', [])
            if tags:
                click.echo(f"Tags: {', '.join(tags)}")

            sources = series_data.get('settlement_sources', [])
            if sources:
                click.echo(f"\nSettlement Sources:")
                for source in sources:
                    click.echo(f"  • {source.get('name', 'N/A')}: {source.get('url', 'N/A')}")

            click.echo()

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


# ========================================
# Main Entry Point
# ========================================

def main():
    """Main entry point"""
    cli(obj={})


if __name__ == "__main__":
    main()
