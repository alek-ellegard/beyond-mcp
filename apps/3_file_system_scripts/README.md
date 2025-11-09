# Kalshi File System Scripts

Standalone, self-contained scripts for Kalshi prediction markets.
Each script is independently executable with zero dependencies between scripts.

## Progressive Disclosure

Run the script with `--help` to see the available options and then call the script to get the data you need.

## Available Scripts

### `scripts/status.py`
**When to use:** Check if Kalshi exchange is operational

### `scripts/markets.py`
**When to use:** Browse available prediction markets

### `scripts/market.py`
**When to use:** Get comprehensive details about a specific market

### `scripts/orderbook.py`
**When to use:** View bid/ask levels for a market

### `scripts/trades.py`
**When to use:** Monitor recent trading activity

### `scripts/search.py`
**When to use:** Find markets by keyword

### `scripts/events.py`
**When to use:** List groups of related markets

### `scripts/event.py`
**When to use:** Get details about a specific event

### `scripts/series_list.py`
**When to use:** Browse all market templates (~6900 available)

### `scripts/series.py`
**When to use:** Get information about a specific market template

## Architecture

- **Self-Contained:** Each script includes all necessary code
- **No External Dependencies:** HTTP client embedded in each script
- **Progressive Discovery:** Only see what you need
- **Incrementally Adoptable:** Use one script or many

## Quick Start

All scripts support `--help` and `--json`:

```bash
uv run scripts/[script].py --help
uv run scripts/[script].py --json
```

No authentication required for any script.