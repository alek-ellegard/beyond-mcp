# Real Examples Walkthrough 🔍

Let's walk through actual scripts from beyond-mcp to see the patterns in action.

---

## Example 1: Simple Script (status.py)

### The Header

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "httpx",      # HTTP client
#     "click",      # CLI framework
# ]
# ///
```

**Just 2 dependencies!** That's all you need to:
- Make HTTP requests
- Build a nice CLI

### The Structure (157 lines total)

```python
# 1. Configuration (10 lines)
API_BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"
API_TIMEOUT = 30.0
USER_AGENT = "Kalshi-CLI/1.0"

# 2. HTTP Client (40 lines)
class KalshiClient:
    """Self-contained HTTP client"""
    def __init__(self):
        self.client = httpx.Client(...)

    def get_exchange_status(self):
        """Make the API call"""
        response = self.client.get("/exchange/status")
        return response.json()

# 3. Formatting (30 lines)
def format_status(data):
    """Pretty print for humans"""
    lines = ["=" * 40]
    lines.append("🏦 KALSHI EXCHANGE STATUS")
    lines.append("=" * 40)

    if data['exchange_active']:
        lines.append("✓ Exchange: ACTIVE")
    else:
        lines.append("✗ Exchange: INACTIVE")

    return "\n".join(lines)

# 4. CLI Interface (40 lines)
@click.command()
@click.option('--json', is_flag=True)
def main(output_json: bool):
    """Main command"""
    with KalshiClient() as client:
        status = client.get_exchange_status()

    if output_json:
        print(json.dumps(status))  # For machines
    else:
        print(format_status(status))  # For humans

# 5. Entry point (5 lines)
if __name__ == "__main__":
    main()
```

### How AI Uses It

**AI wants to check exchange status:**

1. Runs: `uv run status.py --json`
2. Gets: `{"exchange_active": true, "trading_active": true}`
3. Context used: **157 lines** (not 2,000!)

**No other files needed!** ✨

---

## Example 2: Complex Script with Caching (search.py)

This is the most advanced example - 465 lines, fully self-contained.

### The Header

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "httpx",      # HTTP client
#     "click",      # CLI framework
#     "pandas",     # Data caching & searching
# ]
# ///
```

**One extra dependency:** `pandas` for smart caching!

### The Problem It Solves

**Challenge:** Kalshi API has NO search endpoint

**Options:**
1. ❌ Make slow API calls every time → Terrible UX
2. ✅ Build a local cache → Fast searches!

### The Solution (Smart Caching)

```python
# Configuration
CACHE_DIR = Path(__file__).parent.parent.parent.parent / ".kalshi_cache"
CACHE_TTL_HOURS = 6

class KalshiSearchCache:
    """Embedded cache functionality"""

    def build_cache(self):
        """
        Download ALL markets once (2-5 minutes)
        Save as CSV using pandas
        """
        print("Building cache... (this takes 2-5 minutes)")

        # 1. Fetch all events from API
        events = self.fetch_all_events()  # ~100 events

        # 2. Fetch all markets from API
        markets = self.fetch_all_markets()  # ~7,000 markets!

        # 3. Combine data into searchable DataFrame
        df = pd.DataFrame(markets)

        # 4. Save to disk
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = CACHE_DIR / f"kalshi_markets_{timestamp}.csv"
        df.to_csv(cache_file, index=False)

        return df

    def search(self, query: str):
        """
        Search cached data (INSTANT!)
        """
        # Load cache (or build if missing)
        df = self.load_or_build_cache()

        # Search using pandas (super fast!)
        mask = (
            df['ticker'].str.contains(query, case=False, na=False) |
            df['title'].str.contains(query, case=False, na=False) |
            df['subtitle'].str.contains(query, case=False, na=False)
        )

        results = df[mask]
        return results.to_dict('records')
```

### The Performance Difference

**Without caching:**
- Every search: 30+ seconds (API calls)
- Rate limits hit quickly
- Poor user experience

**With caching:**
- First run: 2-5 minutes (build cache)
- Every search after: <1 second! ⚡
- No API calls (except cache refresh)
- Amazing user experience

### How It Works

```bash
# First time (builds cache)
$ uv run search.py bitcoin
Building cache... (this takes 2-5 minutes)
[████████████████████] 100%
Found 12 markets matching 'bitcoin'

# Second time (uses cache)
$ uv run search.py bitcoin
Found 12 markets matching 'bitcoin'
# Instant! ⚡

# 6 hours later (cache expired, auto-rebuild)
$ uv run search.py ethereum
Cache expired, rebuilding...
[████████████████████] 100%
Found 8 markets matching 'ethereum'
```

### File Size

```python
search.py: 465 lines

Includes:
- HTTP client           (60 lines)
- Cache management      (150 lines)
- Search logic          (80 lines)
- Formatting            (50 lines)
- CLI interface         (80 lines)
- Error handling        (45 lines)
```

**Still self-contained!** Everything needed is in one file.

---

## Example 3: The Power of Independence

Let's compare getting market data:

### Traditional Shared Code

```
To read ONE market:

project/
├── src/
│   ├── client.py         ← AI reads this (200 lines)
│   ├── auth.py           ← AI reads this (150 lines)
│   ├── formatting.py     ← AI reads this (180 lines)
│   ├── utils.py          ← AI reads this (120 lines)
│   └── cache.py          ← AI reads this (200 lines)
└── commands/
    └── market.py         ← AI reads this (100 lines)

TOTAL: 950 lines for one operation! 😰
```

### Standalone Scripts

```
To read ONE market:

scripts/
└── market.py             ← AI reads this (219 lines)

TOTAL: 219 lines for one operation! 😊
```

**77% reduction in context!** 🎉

---

## Example 4: Dual Output Modes

Every script supports both human and machine output:

### Human Mode (Default)

```bash
$ uv run markets.py
=====================================
📊 KALSHI MARKETS
=====================================

🎯 INXD-25JAN31-B4100 | S&P 500 reaches 4100 by Jan 31
   Yes: $0.82 | No: $0.18 | Volume: 45,234

🎯 PRES-2024-BIDEN | Biden wins 2024 election
   Yes: $0.45 | No: $0.55 | Volume: 892,341

... (formatted nicely for humans)
```

### JSON Mode (For AI/Automation)

```bash
$ uv run markets.py --json
[
  {
    "ticker": "INXD-25JAN31-B4100",
    "title": "S&P 500 reaches 4100 by Jan 31",
    "yes_price": 0.82,
    "no_price": 0.18,
    "volume": 45234
  },
  {
    "ticker": "PRES-2024-BIDEN",
    "title": "Biden wins 2024 election",
    "yes_price": 0.45,
    "no_price": 0.55,
    "volume": 892341
  }
]
```

**Same script, two modes!** AI just adds `--json` flag.

---

## Example 5: Error Handling

Even errors are dual-mode:

### Human Error

```bash
$ uv run market.py INVALID
❌ Error: Market not found

Check ticker and try again.
Available markets: use 'uv run markets.py'
```

### JSON Error

```bash
$ uv run market.py INVALID --json
{
  "error": "Market not found",
  "code": "NOT_FOUND",
  "ticker": "INVALID"
}
```

**Consistent patterns** make AI's job easier!

---

## Example 6: Absolute Path Resolution

Notice this clever pattern:

```python
# Works regardless of where you run it from!
SCRIPT_FILE = Path(__file__).resolve()
PROJECT_ROOT = SCRIPT_FILE.parent.parent.parent.parent
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"
```

**Why this matters:**

```bash
# All of these work!
$ cd apps/3_file_system_scripts/scripts
$ uv run search.py bitcoin              # ✅ Works

$ cd /home/user/beyond-mcp
$ uv run apps/3_file_system_scripts/scripts/search.py bitcoin  # ✅ Works

$ cd /tmp
$ uv run /path/to/beyond-mcp/apps/.../search.py bitcoin  # ✅ Works
```

Cache always goes to the right place!

---

## Key Patterns Demonstrated

### 1. Self-Contained Client

```python
class KalshiClient:
    """Minimal HTTP client - just what THIS script needs"""

    def __init__(self):
        self.client = httpx.Client(
            base_url=API_BASE_URL,
            timeout=API_TIMEOUT,
            headers={"User-Agent": USER_AGENT}
        )

    def make_request(self, endpoint: str):
        """Make the specific request we need"""
        response = self.client.get(endpoint)
        response.raise_for_status()
        return response.json()
```

**NOT a generic client!** Just what this script needs.

### 2. Smart Defaults

```python
@click.command()
@click.option('--json', is_flag=True,
              help='Output as JSON instead of human-readable format')
@click.option('--limit', default=100,
              help='Maximum number of results (default: 100)')
def main(json: bool, limit: int):
    """Every script has sensible defaults"""
```

### 3. Help System

```bash
$ uv run markets.py --help
Usage: markets.py [OPTIONS]

List all active markets on Kalshi.

Options:
  --json          Output as JSON instead of human-readable
  --limit INTEGER Maximum number of results (default: 100)
  --help          Show this message and exit
```

**AI can learn by asking!** No need to read code.

---

## The Complete Picture

All 10 scripts follow this pattern:

| Script | Lines | Purpose |
|--------|-------|---------|
| status.py | 157 | Exchange status |
| markets.py | 254 | List all markets |
| market.py | 219 | Get one market |
| orderbook.py | 205 | Market orderbook |
| trades.py | 233 | Recent trades |
| **search.py** | **465** | **Cached search** |
| events.py | 226 | List events |
| event.py | 205 | Get one event |
| series_list.py | 214 | Browse series |
| series.py | 196 | Series details |

**Each script:**
- ✅ Works independently
- ✅ Has inline dependencies
- ✅ Provides dual output
- ✅ Includes help
- ✅ Handles errors well
- ✅ Uses absolute paths

**AI's perspective:**
- Need markets? Read 254 lines
- Need search? Read 465 lines
- Need both? Read 719 lines (not 2,374!)

---

## Try It Yourself

1. **Pick a script:**
   ```bash
   cd apps/3_file_system_scripts/scripts
   ```

2. **Read it:**
   ```bash
   cat status.py
   # It's all there! Everything you need.
   ```

3. **Run it:**
   ```bash
   uv run status.py
   # Just works!
   ```

4. **Modify it:**
   - Change the formatting
   - Add new options
   - Adjust the logic
   - Everything is in one file!

5. **Share it:**
   ```bash
   cp status.py ~/my-project/
   # That's it! Fully portable.
   ```

---

## The Magic Moment

The first time you do this:

```bash
# Copy a single script file
$ cp search.py /tmp/test.py

# Go to different directory
$ cd /tmp

# Run it
$ uv run test.py bitcoin
Building cache... (this takes 2-5 minutes)
Found 12 markets matching 'bitcoin'
```

**It just works!**

- No setup
- No installation
- No configuration
- Just one file

That's the power of standalone scripts with inline dependencies! ✨
