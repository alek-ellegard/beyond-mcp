# Kalshi CLI

Command-line interface for Kalshi prediction markets using direct HTTP API access.
All 13 commands in a single 552-line file for simplicity.

## Features

- 🚀 **Direct HTTP API** - No SDK overhead, just httpx
- 📊 **Complete Coverage** - All public Kalshi endpoints
- 🎨 **Dual Output** - Human-readable or pure JSON
- ⚡ **Smart Caching** - Instant search after first run
- 🆓 **No Auth Required** - Read-only public access

## Installation

```bash
cd apps/2_cli
uv sync
```

## Quick Start

```bash
# Check exchange status
uv run kalshi status

# List markets
uv run kalshi markets --limit 10

# Search markets (cached)
uv run kalshi search "bitcoin" --limit 5

# Get market details
uv run kalshi market TICKER

# JSON output for automation
uv run kalshi markets --json
```

## Commands (13)

### Core
- `status` - Exchange operational status
- `search` - Cached keyword search (~2-5 min first run, instant after)

### Markets
- `markets` - List with filters (status, series, event, pagination)
- `market` - Detailed market information
- `orderbook` - Bid/ask depth
- `trades` - Recent trading activity
- `market-candles` - Historical candlestick data

### Events & Series
- `events` - List event collections
- `event` - Event details with markets
- `multivariate` - Combo/multivariate events
- `event-candles` - Aggregated event candlesticks
- `series-list` - All ~6900 series templates
- `series` - Series information

## Architecture

```
kalshi_cli/
├── cli.py              # All 13 commands (552 lines)
├── modules/
│   ├── client.py       # HTTP client & search cache
│   ├── formatting.py   # Output formatters
│   └── constants.py    # API configuration
```

### Design Choices

- **Single File Commands** - All commands in cli.py for clarity
- **Direct HTTP** - Using httpx instead of SDK for better control
- **Pure JSON Mode** - Clean output for MCP/automation (no debug messages)
- **Smart Search Cache** - Pandas-based, 6-hour TTL, automatic refresh

## JSON Output

Every command supports `--json` for automation:

```bash
# Pure JSON (no debug output)
uv run kalshi search "election" --json | jq

# Pipe to files
uv run kalshi markets --json > markets.json

# Process with jq
uv run kalshi market TICKER --json | jq '.yes_bid'
```

## Common Workflows

```bash
# Monitor active markets
uv run kalshi markets --status open --limit 20

# Track specific market
watch -n 30 'uv run kalshi market TICKER'

# Export market data
uv run kalshi markets --limit 100 --json > data.json

# Search and filter
uv run kalshi search "bitcoin" --json | jq '.[] | select(.volume_24h > 10000)'
```

## API Details

- **Base URL**: `https://api.elections.kalshi.com/trade-api/v2`
- **No Authentication**: Public read-only access
- **Rate Limits**: Handled automatically
- **Documentation**: https://docs.kalshi.com/

## Development

```bash
# Run any command
uv run kalshi [command] --help

# Test JSON output
uv run kalshi status --json

# Check all commands
uv run kalshi --help
```

## License

MIT