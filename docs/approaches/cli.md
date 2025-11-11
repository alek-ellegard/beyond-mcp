# Approach 2: CLI (Command-Line Interface)

> **Direct HTTP API access via command-line interface**

## Overview

The CLI approach builds a command-line tool that both humans and AI agents can use. It's the "single source of truth" - one implementation that serves multiple consumers.

## Architecture

```
Claude → subprocess → CLI (13 commands) → Direct HTTP → Kalshi API
        [some context]    [medium overhead]
```

**Location**: `apps/2_cli/`

## Key Characteristics

### ✅ Strengths

- **Single source of truth** - Direct API calls, no wrappers
- **Dual output modes** - Human-readable or pure JSON
- **Smart caching** - Pandas-based search with 6-hour TTL
- **Minimal overhead** - Direct httpx calls, no SDK
- **Improved context** - Agent reads ~half as much as MCP Server

### ⚠️ Trade-offs

- **Not automatic** - Agent needs to know to use it
- **Requires setup** - Installation and configuration
- **Subprocess overhead** - Still spawns processes for each call

## Implementation Details

### Command Count
**13 commands** in a single CLI:
- `status` - Exchange operational status
- `markets` - Browse markets with filters
- `market` - Detailed market information
- `orderbook` - Bid/ask depth
- `trades` - Recent trading activity
- `search` - Keyword search (with caching)
- `events` - List event collections
- `event` - Event details
- `series-list` - Browse all series
- `series` - Series information
- And more...

### Core Files

**`kalshi_cli/cli.py`** (552 lines)
- All 13 commands defined
- Shared flag handling
- Output formatting

**`kalshi_cli/modules/client.py`**
- HTTP client implementation
- Search cache management
- Direct API calls

**`kalshi_cli/modules/formatting.py`**
- Human-readable formatters
- JSON output mode
- Consistent display

## How It Works

### For AI Agents

1. **Agent reads** CLI help text (via prime prompt)
2. **Agent decides** which command to use
3. **Agent executes** `kalshi <command>` via subprocess
4. **CLI makes** direct HTTP call to API
5. **CLI returns** formatted output
6. **Agent preserves** context from help text

### For Humans

```bash
cd apps/2_cli
uv sync
uv run kalshi status
uv run kalshi events --json --limit 10
uv run kalshi search "best ai"
```

## Context Preservation

Unlike MCP, the CLI provides better context preservation because:

1. **Help text is loaded once** - Not on every call
2. **Agent sees implementation** - Can understand patterns
3. **Output is consistent** - AI learns format over time

### Example

```
User: "Get the exchange status"
AI: [Reads kalshi help, executes `kalshi status`]
    "Exchange is active and trading is enabled"

User: "Now list some markets"
AI: [Remembers kalshi CLI exists, executes `kalshi markets --limit 5`]
    [Lists 5 markets without re-learning CLI]
```

## Dual Output Modes

### Human-Readable

```bash
$ kalshi markets --limit 3

Markets:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PREZ2024-DEM-1  Democratic Party wins 2024 Presidential Election
  Volume: 1.2M    Open: Yes $0.58 / No $0.42

  PREZ2024-REP-1  Republican Party wins 2024 Presidential Election
  Volume: 1.1M    Open: Yes $0.42 / No $0.58

  ...
```

### JSON Mode

```bash
$ kalshi markets --limit 3 --json
```

```json
[
  {
    "ticker": "PREZ2024-DEM-1",
    "title": "Democratic Party wins 2024 Presidential Election",
    "volume": 1234567,
    "yes_price": 0.58,
    "no_price": 0.42
  },
  ...
]
```

## Smart Caching

### The Search Problem

Kalshi API has no native search endpoint. To search 6,900+ markets:
- **Without caching**: Paginate through thousands on every search (slow)
- **With caching**: Build once, search instantly

### Cache Implementation

**First search**: 2-5 minutes (builds cache)
**Subsequent**: Instant (searches local DataFrame)
**TTL**: 6 hours (auto-refresh when stale)
**Location**: `.kalshi_cache/` at project root

### What's Cached

- All market series (~6,900 items)
- Titles, subtitles, tickers, descriptions
- Stored as pandas DataFrame for fast querying

## Usage

### Installation

```bash
cd apps/2_cli
uv sync
```

### Basic Commands

```bash
# Check exchange status
uv run kalshi status

# List events
uv run kalshi events

# List markets with limit
uv run kalshi markets --limit 10

# Get specific market
uv run kalshi market TICKER-NAME

# Search (first time: builds cache)
uv run kalshi search "election"

# JSON output for any command
uv run kalshi events --json
```

### Prime Prompt for AI

Use the `/prime_kalshi_cli_tools` slash command to load CLI documentation into agent context.

```
In Claude: "/prime_kalshi_cli_tools"
In Claude: "kalshi: List events"
In Claude: "kalshi: Search for markets about AI"
```

## Token Consumption

**Initial load** (prime prompt): ~500-800 tokens
- CLI help text
- Command descriptions
- Example usage

**Per command**: ~50-100 tokens
- Command invocation
- Flag parsing
- Output parsing

**Cumulative**: Much better than MCP (help loaded once)

## When to Use CLI

### ✅ Choose CLI if:

1. **Building new tool** - You control the implementation
2. **Dual-purpose** - Humans AND AI will use it
3. **Need flexibility** - Want to customize/extend
4. **Context matters** - Better than MCP but not scripts
5. **Team tooling** - Standardize operations across team

### ❌ Avoid CLI if:

1. **Context critical** - Need maximum efficiency (use Scripts)
2. **Using Claude Code** - Skills are better
3. **External tool** - MCP is more appropriate
4. **Max portability** - Scripts are more portable

## Real-World Fit

### Ideal For:
- New API integrations
- Internal team tools
- DevOps automation
- Data exploration tools

### Not Ideal For:
- External third-party tools (use MCP)
- Maximum context efficiency (use Scripts)
- Claude Code skills (use Skills)

## Comparison to Other Approaches

| Aspect | MCP Server | **CLI** | Scripts | Skills |
|--------|-----------|---------|---------|--------|
| Context preservation | ❌ Poor | **😐 Medium** | ✅ Good | ✅ Excellent |
| Token efficiency | ❌ Poor | **😐 Medium** | ✅ Good | ✅ Excellent |
| Auto-discovery | ✅ Yes | **❌ No** | ❌ No | ✅ Yes |
| Dual-purpose | ❌ No | **✅ Yes** | ❌ No | ❌ No |
| Customizable | ❌ No | **✅ Yes** | ✅ Yes | ✅ Yes |

## Migration Path

**Moving from CLI to other approaches:**

- **From MCP**: Extract CLI logic (already done in this repo!)
- **To Scripts**: Break CLI commands into standalone files
- **To Skills**: Wrap CLI or scripts in SKILL.md

## Related Documentation

- [MCP Server approach](mcp-server.md) - Standard protocol alternative
- [Scripts approach](scripts.md) - Higher context efficiency
- [Skills approach](skills.md) - Claude Code-specific
- [Decision Guide](../guides/decision-guide.md) - Choose the right approach

## Code Location

```
apps/2_cli/
├── kalshi_cli/
│   ├── cli.py                 # 13 commands (552 lines)
│   └── modules/
│       ├── client.py          # HTTP client & cache
│       └── formatting.py      # Output formatters
├── pyproject.toml             # uv configuration
└── README.md                  # CLI-specific docs
```

---

**Navigation**: [← Back to approaches](README.md) | [Next: Scripts →](scripts.md)
