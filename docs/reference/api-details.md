# API Details & Technical Specifications

> Technical implementation details for the beyond-mcp repository

## Kalshi API Specification

### Base Configuration

**Base URL**: `https://api.elections.kalshi.com/trade-api/v2`

**Authentication**: None required (read-only public data)

**Rate Limiting**: Standard API rate limits apply

**Data Volume**: ~6,900 market series available

### Available Endpoints

#### Exchange Status
```
GET /exchange/status
Response: { "trading_active": bool, "exchange_active": bool }
```

#### Markets
```
GET /markets
Params: limit, cursor, event_ticker, series_ticker, status
Response: { "markets": [...], "cursor": "..." }
```

#### Single Market
```
GET /markets/{ticker}
Response: { "ticker": "...", "title": "...", ... }
```

#### Market Orderbook
```
GET /markets/{ticker}/orderbook
Response: { "yes": [...], "no": [...] }
```

#### Market Trades
```
GET /markets/{ticker}/trades
Params: limit, cursor
Response: { "trades": [...], "cursor": "..." }
```

#### Events
```
GET /events
Params: limit, cursor, series_ticker, status
Response: { "events": [...], "cursor": "..." }
```

#### Single Event
```
GET /events/{ticker}
Response: { "event_ticker": "...", "title": "...", ... }
```

#### Series
```
GET /series
Params: limit, cursor
Response: { "series": [...], "cursor": "..." }
```

#### Single Series
```
GET /series/{ticker}
Response: { "series_ticker": "...", "title": "...", ... }
```

## Search Caching Implementation

### The Problem

Kalshi API doesn't provide a native search endpoint. To search across ~6,900 markets:

**Without caching**:
- Paginate through all markets (100 per page)
- 69 API calls minimum
- 2-5 minutes per search
- API rate limits

**With caching**:
- Build cache once (2-5 minutes)
- Search locally (instant)
- Refresh every 6 hours
- No repeated API calls

### Cache Structure

**Location**: `.kalshi_cache/` at project root

**Files**:
- `series_cache.csv` - All series data
- `series_cache_timestamp.txt` - Last update time

**Data Cached**:
```python
{
    "series_ticker": str,
    "title": str,
    "subtitle": str,
    "description": str,
    "tags": list[str],
    "category": str,
    # ... other fields
}
```

### Cache Implementation

```python
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path(".kalshi_cache")
CACHE_TTL = timedelta(hours=6)

def get_cache():
    timestamp_file = CACHE_DIR / "series_cache_timestamp.txt"
    cache_file = CACHE_DIR / "series_cache.csv"

    # Check if cache exists and is fresh
    if timestamp_file.exists():
        timestamp = datetime.fromisoformat(
            timestamp_file.read_text().strip()
        )
        if datetime.now() - timestamp < CACHE_TTL:
            return pd.read_csv(cache_file)

    # Build new cache
    return build_cache()

def build_cache():
    # Fetch all series (with pagination)
    all_series = []
    cursor = None

    while True:
        response = api_get("/series", params={
            "limit": 100,
            "cursor": cursor
        })
        all_series.extend(response["series"])
        cursor = response.get("cursor")
        if not cursor:
            break

    # Save to cache
    df = pd.DataFrame(all_series)
    df.to_csv(CACHE_DIR / "series_cache.csv", index=False)

    timestamp_file = CACHE_DIR / "series_cache_timestamp.txt"
    timestamp_file.write_text(datetime.now().isoformat())

    return df

def search(query):
    df = get_cache()

    # Search across multiple fields
    mask = (
        df["title"].str.contains(query, case=False, na=False) |
        df["subtitle"].str.contains(query, case=False, na=False) |
        df["description"].str.contains(query, case=False, na=False) |
        df["series_ticker"].str.contains(query, case=False, na=False)
    )

    return df[mask]
```

### Cache Sharing

**Location Strategy**: Cache is stored at project root (`.kalshi_cache/`)

**Path Resolution**:
```python
# In any script, resolve to project root
from pathlib import Path

# Assuming scripts are in apps/X/scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"
```

**Shared by**:
- CLI (apps/2_cli)
- Scripts (apps/3_file_system_scripts)
- Skills (apps/4_skill)

**Why this works**:
- Absolute path resolution
- Works from any working directory
- No relative path issues
- Cache built once, used by all

## Path Resolution Patterns

### Problem

Scripts can be invoked from any directory:
```bash
# Different working directories
cd /
uv run /home/user/beyond-mcp/apps/3_file_system_scripts/scripts/status.py

cd /home/user/beyond-mcp
uv run apps/3_file_system_scripts/scripts/status.py

cd apps/3_file_system_scripts/scripts
uv run status.py
```

### Solution

Use `Path(__file__).resolve()` for absolute paths:

```python
from pathlib import Path

# Get script's absolute path
SCRIPT_PATH = Path(__file__).resolve()

# Navigate to project root (3 levels up for scripts in apps/X/scripts/)
PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent

# Resolve cache directory
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"

# Always works, regardless of working directory
```

### Verification

```python
# Verify path resolution
print(f"Script: {SCRIPT_PATH}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Cache dir: {CACHE_DIR}")

# Output (always correct):
# Script: /home/user/beyond-mcp/apps/3_file_system_scripts/scripts/status.py
# Project root: /home/user/beyond-mcp
# Cache dir: /home/user/beyond-mcp/.kalshi_cache
```

## Inline Dependencies (PEP 723)

### Specification

[PEP 723](https://peps.python.org/pep-0723/) defines inline script metadata:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "httpx",
#   "pandas",
#   "click",
# ]
# ///
```

### How It Works

1. **Shebang**: `#!/usr/bin/env -S uv run --script`
   - Makes script executable
   - Tells uv to handle execution

2. **Metadata block**: `# /// script ... ///`
   - Declares Python version requirement
   - Lists dependencies
   - Parsed by uv

3. **Execution**:
   ```bash
   uv run script.py
   # uv reads metadata
   # uv creates isolated environment
   # uv installs dependencies
   # uv runs script
   ```

### Benefits

- ✅ No virtual environment setup
- ✅ No `pip install` needed
- ✅ Dependencies declared in file
- ✅ Reproducible execution
- ✅ Self-contained scripts

### Example

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "httpx",
# ]
# ///

import httpx

def main():
    response = httpx.get("https://api.example.com")
    print(response.json())

if __name__ == "__main__":
    main()
```

Run directly:
```bash
uv run script.py
# Just works - no setup needed
```

## HTTP Client Pattern

### Shared vs. Embedded

**Traditional (shared)**:
```
project/
├── shared/
│   └── http_client.py  # Shared module
└── tools/
    ├── tool1.py  # Imports shared.http_client
    └── tool2.py  # Imports shared.http_client
```

**This repo (embedded)**:
```
scripts/
├── tool1.py  # Embedded HTTP client
└── tool2.py  # Embedded HTTP client
```

### Why Embed?

1. **Context efficiency**: AI reads one file, not imports
2. **Independence**: Each script works alone
3. **Portability**: Copy file, it works
4. **Version stability**: Changes don't break other scripts

### HTTP Client Implementation

```python
import httpx
from typing import Optional, Dict, Any

class KalshiClient:
    def __init__(self):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True
        )

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
        """Make GET request to Kalshi API"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error: {e}")
            return None

    def close(self):
        """Clean up HTTP client"""
        self.client.close()
```

**Size**: ~50 lines

**Cost**: Repeated in each script

**Benefit**: -1000+ tokens of import resolution for AI

## Error Handling Patterns

### API Errors

```python
try:
    response = client.get("/endpoint")
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    if e.response.status_code == 404:
        print("Not found")
    elif e.response.status_code == 429:
        print("Rate limited")
    else:
        print(f"HTTP error: {e}")
except httpx.RequestError as e:
    print(f"Request failed: {e}")
```

### Cache Errors

```python
try:
    cache = get_cache()
except FileNotFoundError:
    print("Building cache (first run)...")
    cache = build_cache()
except Exception as e:
    print(f"Cache error: {e}")
    print("Continuing without cache...")
```

### Path Errors

```python
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"

# Ensure directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Safe file operations
cache_file = CACHE_DIR / "cache.csv"
if cache_file.exists():
    df = pd.read_csv(cache_file)
else:
    df = build_cache()
```

## Performance Characteristics

### Latency (Typical)

| Operation | MCP | CLI | Scripts | Skills |
|-----------|-----|-----|---------|--------|
| Exchange status | 200ms | 150ms | 100ms | 150ms |
| List markets (10) | 250ms | 200ms | 150ms | 200ms |
| Search (cached) | 300ms | 250ms | 200ms | 250ms |
| Search (uncached) | 180s | 180s | 180s | 180s |

**Note**: Uncached search takes 2-5 min to build cache

### Memory Usage

| Approach | Base | + Cache | Peak |
|----------|------|---------|------|
| MCP Server | 50MB | 120MB | 150MB |
| CLI | 30MB | 100MB | 120MB |
| Scripts | 20MB | 90MB | 100MB |
| Skills | 25MB | 95MB | 105MB |

### Token Consumption

See [trade-off-comparison.md](trade-off-comparison.md) for detailed analysis.

## Testing Patterns

### Unit Tests

```python
import pytest
from script import KalshiClient

def test_client_initialization():
    client = KalshiClient()
    assert client.base_url.startswith("https://")

def test_get_status(mocker):
    client = KalshiClient()
    mocker.patch.object(
        client.client,
        'get',
        return_value=MockResponse({"trading_active": True})
    )
    result = client.get("/exchange/status")
    assert result["trading_active"] is True
```

### Integration Tests

```python
def test_real_api():
    """Test against real Kalshi API"""
    client = KalshiClient()
    result = client.get("/exchange/status")

    assert result is not None
    assert "trading_active" in result
    assert isinstance(result["trading_active"], bool)
```

### Cache Tests

```python
def test_cache_build(tmp_path):
    """Test cache building"""
    cache_dir = tmp_path / ".kalshi_cache"
    cache_dir.mkdir()

    # Build cache
    cache = build_cache(cache_dir)

    # Verify cache file exists
    assert (cache_dir / "series_cache.csv").exists()

    # Verify cache is valid DataFrame
    assert isinstance(cache, pd.DataFrame)
    assert len(cache) > 0
```

## Related Documentation

- [Standalone Scripts Deep Dive](../deep-dives/standalone-scripts.md) - Implementation patterns
- [Search Caching Deep Dive](../deep-dives/search-caching.md) - Cache architecture
- [Trade-off Comparison](trade-off-comparison.md) - Performance comparison

---

**Navigation**: [← Back to reference](README.md) | [↑ Docs root](../README.md)
