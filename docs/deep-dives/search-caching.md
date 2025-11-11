# Search Caching: Implementation Deep Dive

> Building efficient search on APIs without native search endpoints

## The Problem

### Kalshi API Limitation

The Kalshi API provides market data but **no native search endpoint**:

```
Available: GET /markets?limit=100&cursor=...
Missing: GET /search?q=election
```

**Data volume**: ~6,900 market series

### Naive Approach (Don't Do This)

```python
def search(query):
    results = []
    cursor = None

    # Paginate through ALL markets
    while True:
        response = get_markets(limit=100, cursor=cursor)
        for market in response["markets"]:
            if query.lower() in market["title"].lower():
                results.append(market)

        cursor = response.get("cursor")
        if not cursor:
            break

    return results
```

**Cost per search**:
- 69 API calls (6900 / 100)
- 2-5 minutes wait time
- Rate limit risk
- API cost

**Reality**: This is unusable for interactive workflows

## The Solution: Local Caching

### Strategy

1. **Build once**: Fetch all markets, store locally
2. **Search locally**: Use pandas for fast queries
3. **Refresh periodically**: 6-hour TTL

### Architecture

```
First Search (2-5 minutes):
  User query → Build cache → Fetch all markets → Save to disk → Search → Results

Subsequent Searches (instant):
  User query → Check cache → Load from disk → Search → Results

After 6 hours:
  User query → Cache stale → Rebuild → Search → Results
```

## Implementation

### Cache Structure

```
.kalshi_cache/
├── series_cache.csv           # Pandas DataFrame as CSV
├── series_cache_timestamp.txt # ISO format timestamp
└── .gitignore                 # Don't commit cache
```

### Core Functions

#### 1. Check Cache Freshness

```python
from pathlib import Path
from datetime import datetime, timedelta

CACHE_DIR = Path(".kalshi_cache")
CACHE_TTL = timedelta(hours=6)

def is_cache_fresh():
    """Check if cache exists and is within TTL"""
    timestamp_file = CACHE_DIR / "series_cache_timestamp.txt"

    if not timestamp_file.exists():
        return False

    try:
        timestamp = datetime.fromisoformat(
            timestamp_file.read_text().strip()
        )
        age = datetime.now() - timestamp
        return age < CACHE_TTL
    except (ValueError, OSError):
        return False
```

#### 2. Load Cache

```python
import pandas as pd

def load_cache():
    """Load cache from disk"""
    cache_file = CACHE_DIR / "series_cache.csv"

    if not cache_file.exists():
        return None

    try:
        return pd.read_csv(cache_file)
    except Exception as e:
        print(f"Error loading cache: {e}")
        return None
```

#### 3. Build Cache

```python
import httpx

def build_cache():
    """Fetch all series and build cache"""
    print("Building cache (first run, 2-5 minutes)...")

    client = httpx.Client(
        base_url="https://api.elections.kalshi.com/trade-api/v2",
        timeout=30.0
    )

    all_series = []
    cursor = None
    page = 0

    while True:
        page += 1
        print(f"  Fetching page {page}...", end="\r")

        # Fetch page
        response = client.get("/series", params={
            "limit": 100,
            "cursor": cursor
        })
        response.raise_for_status()
        data = response.json()

        # Collect series
        all_series.extend(data.get("series", []))

        # Check for more pages
        cursor = data.get("cursor")
        if not cursor:
            break

    print(f"\n  Fetched {len(all_series)} series")

    # Convert to DataFrame
    df = pd.DataFrame(all_series)

    # Save to cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / "series_cache.csv"
    df.to_csv(cache_file, index=False)

    # Save timestamp
    timestamp_file = CACHE_DIR / "series_cache_timestamp.txt"
    timestamp_file.write_text(datetime.now().isoformat())

    print("  Cache built successfully")
    return df
```

#### 4. Get Cache (Main Entry Point)

```python
def get_cache():
    """Get cache, building if necessary"""
    if is_cache_fresh():
        cache = load_cache()
        if cache is not None:
            return cache

    # Cache is stale or missing
    return build_cache()
```

#### 5. Search Cache

```python
def search(query, limit=10):
    """Search cache by query"""
    cache = get_cache()

    # Search across multiple fields
    query_lower = query.lower()
    mask = (
        cache["title"].str.lower().str.contains(query_lower, na=False) |
        cache["subtitle"].str.lower().str.contains(query_lower, na=False) |
        cache["description"].str.lower().str.contains(query_lower, na=False) |
        cache["series_ticker"].str.lower().str.contains(query_lower, na=False)
    )

    results = cache[mask]

    if limit:
        results = results.head(limit)

    return results
```

## Path Resolution

### The Challenge

Cache needs to be shared across:
- CLI (apps/2_cli/)
- Scripts (apps/3_file_system_scripts/scripts/)
- Skills (apps/4_skill/.claude/skills/kalshi-markets/scripts/)

**Problem**: Different working directories

### Solution: Absolute Path Resolution

```python
from pathlib import Path

# Get script location
SCRIPT_PATH = Path(__file__).resolve()

# Navigate to project root
# For CLI: apps/2_cli/module.py → ../../
# For Scripts: apps/3_file_system_scripts/scripts/search.py → ../../../
# Adjust based on script depth

# For scripts (3 levels deep)
PROJECT_ROOT = SCRIPT_PATH.parent.parent.parent

# For CLI modules (2 levels deep)
PROJECT_ROOT = SCRIPT_PATH.parent.parent

# Resolve cache directory
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"
```

### Verification

```python
# Add debug output
print(f"Script: {SCRIPT_PATH}")
print(f"Project root: {PROJECT_ROOT}")
print(f"Cache dir: {CACHE_DIR}")

# Ensure cache directory exists
CACHE_DIR.mkdir(parents=True, exist_ok=True)
```

## Cache Lifecycle

### Timeline

```
T=0: User searches "election"
  ├─ Cache doesn't exist
  ├─ Build cache (2-5 min)
  ├─ Search cache (instant)
  └─ Return results

T=1min: User searches "AI"
  ├─ Cache exists and fresh
  ├─ Load cache (instant)
  ├─ Search cache (instant)
  └─ Return results

T=6h: User searches "president"
  ├─ Cache exists but stale (>6 hours old)
  ├─ Rebuild cache (2-5 min)
  ├─ Search cache (instant)
  └─ Return results
```

### TTL Rationale

**6 hours chosen because**:
- Markets change, but not constantly
- Balance between freshness and speed
- Typical usage: check markets few times per day
- API limits: avoid excessive rebuilds

**Alternatives**:
- 1 hour: Too frequent, more API calls
- 24 hours: Too stale, miss updates
- Manual: Requires user intervention

## Performance Characteristics

### Build Time

| Factor | Impact | Time |
|--------|--------|------|
| Series count | Linear | ~6900 series |
| Page size | Affects # requests | 100/page = 69 requests |
| Network latency | Per request | ~50-100ms/request |
| Rate limits | May throttle | Occasional delays |

**Typical**: 2-5 minutes

**Best case**: 1.5 minutes (fast network, no throttling)

**Worst case**: 8 minutes (slow network, rate limits)

### Search Time

| Operation | Time | Notes |
|-----------|------|-------|
| Load cache | 50-200ms | Read CSV into DataFrame |
| Search | 10-50ms | Pandas string matching |
| Format output | 5-10ms | Convert to display format |

**Total**: ~100-300ms (instant for user)

**Comparison**: 2-5 minutes (API pagination) → 300ms (cache)

**Speedup**: 400-1000x faster

### Memory Usage

| Component | Size |
|-----------|------|
| Cache file (CSV) | ~2-5 MB |
| DataFrame in memory | ~5-10 MB |
| Search results | < 1 MB |

**Total**: ~10-15 MB (negligible)

## Cache Optimization Strategies

### 1. Selective Fields

**Problem**: Caching everything uses more memory/disk

**Solution**: Cache only needed fields

```python
def build_cache():
    all_series = fetch_all_series()

    # Only keep relevant fields
    df = pd.DataFrame(all_series)
    df = df[[
        "series_ticker",
        "title",
        "subtitle",
        "description",
        "category",
        "tags"
    ]]

    df.to_csv(cache_file, index=False)
    return df
```

### 2. Compression

**Pattern**: Compress cache file

```python
# Save compressed
df.to_csv(cache_file, index=False, compression="gzip")

# Load compressed
df = pd.read_csv(cache_file, compression="gzip")
```

**Benefit**: 50-70% smaller disk usage

**Trade-off**: Slightly slower load (still fast)

### 3. Partial Updates

**Advanced**: Only fetch changed data

```python
def update_cache():
    """Update only new/changed series"""
    cache = load_cache()

    # Get latest series after last update
    new_series = fetch_series_since(last_update)

    # Merge with cache
    updated = pd.concat([cache, pd.DataFrame(new_series)])
    updated = updated.drop_duplicates(subset=["series_ticker"])

    save_cache(updated)
```

**Benefit**: Faster updates (seconds vs. minutes)

**Complexity**: Requires API change tracking

### 4. Index Optimization

**Pattern**: Create search index

```python
# Build index on common search fields
cache["search_text"] = (
    cache["title"].fillna("") + " " +
    cache["subtitle"].fillna("") + " " +
    cache["description"].fillna("")
).str.lower()

# Search on single field
mask = cache["search_text"].str.contains(query.lower())
```

**Benefit**: Faster search on large datasets

## Error Handling

### Network Errors

```python
def build_cache():
    try:
        # Fetch data
        all_series = fetch_all_series()
    except httpx.HTTPError as e:
        print(f"Error fetching data: {e}")
        print("Using stale cache if available...")

        # Fall back to stale cache
        cache = load_cache()
        if cache is not None:
            return cache

        # No cache available
        raise Exception("Cannot build cache and no backup available")
```

### Corrupt Cache

```python
def load_cache():
    try:
        df = pd.read_csv(cache_file)

        # Validate cache structure
        required_fields = ["series_ticker", "title"]
        if not all(field in df.columns for field in required_fields):
            print("Cache is corrupt, rebuilding...")
            return None

        return df
    except Exception as e:
        print(f"Error loading cache: {e}")
        return None
```

### Disk Space

```python
def build_cache():
    # Check available space
    import shutil
    stats = shutil.disk_usage(CACHE_DIR)

    if stats.free < 100_000_000:  # 100 MB
        print("Warning: Low disk space")
        # Consider cleaning old caches

    # Proceed with build
    ...
```

## Testing Strategies

### Unit Tests

```python
import pytest
from datetime import datetime, timedelta

def test_cache_freshness(tmp_path):
    """Test cache TTL logic"""
    cache_dir = tmp_path / ".kalshi_cache"
    cache_dir.mkdir()

    timestamp_file = cache_dir / "series_cache_timestamp.txt"

    # Fresh cache
    timestamp_file.write_text(datetime.now().isoformat())
    assert is_cache_fresh(cache_dir)

    # Stale cache (7 hours old)
    old_time = datetime.now() - timedelta(hours=7)
    timestamp_file.write_text(old_time.isoformat())
    assert not is_cache_fresh(cache_dir)
```

### Integration Tests

```python
def test_search_with_cache(tmp_path):
    """Test end-to-end search"""
    # Mock API responses
    mock_series = [
        {"series_ticker": "PREZ", "title": "Presidential Election"},
        {"series_ticker": "AI", "title": "Best AI Company"},
    ]

    with patch("httpx.Client.get") as mock_get:
        mock_get.return_value.json.return_value = {
            "series": mock_series,
            "cursor": None
        }

        # Search (will build cache)
        results = search("election", cache_dir=tmp_path)

        # Verify results
        assert len(results) == 1
        assert results.iloc[0]["series_ticker"] == "PREZ"
```

### Performance Tests

```python
import time

def test_search_performance():
    """Verify search is fast"""
    # Build cache
    cache = get_cache()

    # Time search
    start = time.time()
    results = search("election")
    elapsed = time.time() - start

    # Should be under 1 second
    assert elapsed < 1.0
```

## Common Issues

### Issue 1: Cache Won't Build

**Symptoms**:
- "Error fetching data" messages
- Cache directory empty

**Causes**:
- Network connectivity
- API rate limits
- Invalid credentials (if auth required)

**Solution**:
```python
# Add retry logic
for attempt in range(3):
    try:
        return build_cache()
    except httpx.HTTPError:
        if attempt < 2:
            time.sleep(5 * (attempt + 1))  # Backoff
        else:
            raise
```

### Issue 2: Search Returns Nothing

**Symptoms**:
- Query returns 0 results
- Known markets not found

**Causes**:
- Case sensitivity
- Incomplete cache
- Field not searched

**Solution**:
```python
# Ensure case-insensitive search
mask = cache["title"].str.lower().str.contains(query.lower())

# Search more fields
mask = (
    cache["title"].str.lower().str.contains(query.lower()) |
    cache["description"].str.lower().str.contains(query.lower())
)
```

### Issue 3: Stale Results

**Symptoms**:
- Old markets returned
- Missing new markets

**Causes**:
- Cache not refreshing
- TTL too long

**Solution**:
```python
# Force refresh
def search(query, force_refresh=False):
    if force_refresh:
        cache = build_cache()
    else:
        cache = get_cache()

    # Search...
```

## Related Patterns

### Pattern: Database Cache

**Alternative**: Use SQLite instead of CSV

```python
import sqlite3

def build_cache():
    conn = sqlite3.connect(CACHE_DIR / "cache.db")

    # Create table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS series (
            series_ticker TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            ...
        )
    """)

    # Insert data
    conn.executemany("INSERT OR REPLACE INTO series VALUES ...", data)

def search(query):
    conn = sqlite3.connect(CACHE_DIR / "cache.db")
    return pd.read_sql(
        "SELECT * FROM series WHERE title LIKE ?",
        conn,
        params=(f"%{query}%",)
    )
```

**Benefit**: Faster search, better indexing

**Trade-off**: More complexity

### Pattern: Incremental Cache

**Alternative**: Update cache incrementally

```python
def update_cache():
    cache = load_cache()

    # Get only series updated after cache timestamp
    last_update = get_cache_timestamp()
    new_series = fetch_series_updated_after(last_update)

    # Merge
    updated = merge_series(cache, new_series)
    save_cache(updated)
```

**Benefit**: Faster updates (seconds)

**Trade-off**: Requires API support for "updated since"

## Best Practices

1. **Always validate cache** - Check structure on load
2. **Use TTL** - Balance freshness vs. performance
3. **Handle errors** - Graceful degradation
4. **Document TTL** - Users should know refresh timing
5. **Test performance** - Ensure cache is faster than API
6. **Clean old caches** - Prevent disk bloat
7. **Share cache location** - Consistent path across approaches

## Related Documentation

- [API Details](../reference/api-details.md) - API specifications
- [Context Preservation](context-preservation.md) - Why caching helps
- [Scripts Deep Dive](standalone-scripts.md) - Implementation pattern

---

**Navigation**: [← Back to deep dives](README.md) | [↑ Docs root](../README.md)
