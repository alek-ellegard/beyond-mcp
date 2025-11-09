# Kalshi MCP Server

Model Context Protocol (MCP) server that provides LLMs with access to Kalshi prediction market data through structured tool calls.

## Overview

This MCP server wraps the Kalshi CLI (located in `../2_cli/`) and exposes each CLI command as an MCP tool. It provides one-to-one mappings, allowing LLMs to:

- Query market data, prices, and orderbooks
- Search for markets by keyword
- Get recent trades and historical data
- Access event and series information
- All without requiring authentication (read-only public API)

## Architecture

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  Claude / LLM Client                            │
│                                                 │
└───────────────────┬─────────────────────────────┘
                    │ MCP Protocol
                    │
┌───────────────────▼─────────────────────────────┐
│                                                 │
│  Kalshi MCP Server (this app)                   │
│  • 15 MCP Tools                                 │
│  • FastMCP Framework                            │
│                                                 │
└───────────────────┬─────────────────────────────┘
                    │ subprocess calls
                    │
┌───────────────────▼─────────────────────────────┐
│                                                 │
│  Kalshi CLI (apps/2_cli/)                       │
│  • Direct HTTP API client                       │
│  • JSON output mode                             │
│                                                 │
└───────────────────┬─────────────────────────────┘
                    │ HTTPS
                    │
┌───────────────────▼─────────────────────────────┐
│                                                 │
│  Kalshi Public API                              │
│  https://api.elections.kalshi.com               │
│                                                 │
└─────────────────────────────────────────────────┘
```

## Installation

```bash
# Navigate to this directory
cd apps/1_mcp_server

# Install dependencies
uv sync
```

## Quick Start

### Test with MCP Inspector

```bash
# Test the server interactively
uv run mcp dev server.py
```

This opens the MCP Inspector where you can:
- Browse available tools
- Test tool calls with different parameters
- See structured responses

### Install in Claude Desktop

```bash
# Install for use with Claude Desktop
uv run mcp install server.py

# Or with custom name
uv run mcp install server.py --name "Kalshi Markets"
```

## Available Tools

The server exposes 15 tools, each mapping to a Kalshi CLI command:

### Exchange

- **get_exchange_status** - Get exchange and trading status

### Markets

- **list_markets** - List markets with filters (status, series, event, etc.)
- **get_market** - Get detailed market information by ticker
- **get_market_orderbook** - View orderbook depth for a market
- **search_markets** - Fast keyword search across markets (uses cache)
- **get_recent_trades** - Get recent trades for all or specific markets
- **get_market_candlesticks** - Historical candlestick data for a market

### Events

- **list_events** - List events (collections of related markets)
- **get_event** - Get detailed event information
- **list_multivariate_events** - Get multivariate/combo events
- **get_event_candlesticks** - Historical candlestick data for an event

### Series

- **list_series** - List all series (~6900 available!)
- **get_series** - Get detailed series information

## Example Usage

Once installed in Claude Desktop, you can ask:

```
"What's the current Kalshi exchange status?"
→ Calls get_exchange_status()

"Show me 5 open markets about Bitcoin"
→ Calls search_markets(keyword="Bitcoin", limit=5)

"Get details for market KXBTCD-25NOV0612-T102499.99"
→ Calls get_market(ticker="KXBTCD-25NOV0612-T102499.99")

"What are recent trades?"
→ Calls get_recent_trades(limit=10)

"List events in the KXHIGHNY series"
→ Calls list_events(series_ticker="KXHIGHNY")
```

## Implementation Details

### Tool Design

Each tool:
1. Accepts the same parameters as the corresponding CLI command
2. Builds and executes `uv run kalshi <command> --json` via subprocess
3. Returns parsed JSON output as structured data
4. Handles errors gracefully with descriptive messages

### No Direct API Calls

The MCP server intentionally **does not** make direct HTTP calls to Kalshi. Instead:
- ✅ Delegates all API logic to the battle-tested CLI
- ✅ Single source of truth for API interaction
- ✅ Easier maintenance (updates only in CLI)
- ✅ Consistent behavior between CLI and MCP usage

### Search Caching

The `search_markets` tool uses the CLI's intelligent caching:
- First search: ~2-5 minutes (builds cache)
- Subsequent searches: Instant (pandas-based)
- Cache refreshes automatically every hour

## Development

### Project Structure

```
apps/1_mcp_server/
├── server.py           # Main MCP server implementation
├── pyproject.toml      # Project dependencies and metadata
└── README.md           # This file
```

### Running Locally

```bash
# Run with stdio transport (default)
uv run python server.py

# Or use mcp dev for interactive testing
uv run mcp dev server.py
```

### Adding New Tools

To add a new tool when the CLI adds a command:

1. Add the CLI command to `../2_cli/`
2. In `server.py`, add a new `@mcp.tool()` decorated function
3. Call `run_kalshi_cli()` with appropriate arguments
4. Document parameters and return value

## API Documentation

All tools use the Kalshi public API endpoints:
- Base URL: `https://api.elections.kalshi.com/trade-api/v2`
- No authentication required for read-only access
- Full API docs: https://docs.kalshi.com/

## Validation

This MCP server has been validated with Claude Code agent. See the full validation report:

📄 **[Validation Report](../../app_docs/kalshi-mcp-server-validation.md)**

The validation confirms:
- ✅ All 13 MCP tools working correctly
- ✅ End-to-end data flow verified (Claude → MCP → CLI → API)
- ✅ CLI integration via subprocess working
- ✅ JSON parsing and error handling validated
- ✅ Production ready for Claude Desktop and CLI usage

## License

MIT
