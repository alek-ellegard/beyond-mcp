# Approach 3: File System Scripts

> **Progressive disclosure via standalone scripts**

## Overview

The Scripts approach breaks functionality into individual, self-contained Python files. Each script is fully independent with embedded dependencies, optimized for progressive disclosure and maximum context efficiency.

## Architecture

```
Claude → Read tool → Individual script → Embedded HTTP client → Kalshi API
        [context preserved]           [minimal overhead]
```

**Location**: `apps/3_file_system_scripts/scripts/`

## Key Characteristics

### ✅ Strengths

- **Progressive disclosure** - Only load scripts you need (~200-300 lines each)
- **Complete isolation** - Each script is fully self-contained
- **Zero shared dependencies** - HTTP client embedded in each script
- **Context efficient** - Agent only reads relevant scripts
- **High portability** - Just Python files (+ httpx)
- **No installation** - Run with `uv run script.py`

### ⚠️ Trade-offs

- **Code duplication** - HTTP client repeated in each script (intentional)
- **No shared state** - Cache and utilities duplicated
- **Manual discovery** - AI must know scripts exist (use prime prompt)

## Implementation Details

### Script Count
**10 standalone scripts**, each ~200-300 lines:

1. `status.py` - Exchange operational status
2. `markets.py` - Browse markets with filters
3. `market.py` - Detailed market information
4. `orderbook.py` - Bid/ask depth
5. `trades.py` - Recent trading activity
6. `search.py` - Keyword search (with caching)
7. `events.py` - List event collections
8. `event.py` - Event details
9. `series_list.py` - Browse all ~6,900 series
10. `series.py` - Series information

### Script Structure

Each script follows the same pattern:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "httpx",
#   "pandas",  # if needed
# ]
# ///

import httpx
from pathlib import Path

# Embedded HTTP client
class KalshiClient:
    def __init__(self):
        self.base_url = "https://api.elections.kalshi.com/trade-api/v2"
        self.client = httpx.Client()

    def get(self, endpoint):
        # Direct HTTP implementation
        ...

# Script-specific functionality
def main():
    client = KalshiClient()
    # Do the thing
    ...

if __name__ == "__main__":
    main()
```

## Progressive Disclosure in Action

### Traditional Approach (CLI/MCP)

Agent loads entire tool definition (~500-1500 lines):

```
Claude reads:
  - All 13 commands
  - All flags and options
  - Implementation details
  - Output formatters
  Total: ~1000-1500 tokens
```

### Scripts Approach

Agent loads only what's needed:

```
User: "Get exchange status"
Claude reads: status.py only (~200 lines, ~300 tokens)

User: "Now search for AI markets"
Claude reads: search.py only (~250 lines, ~350 tokens)

Total: ~650 tokens vs. 1500 tokens (57% savings)
```

## Code Duplication: A Feature, Not a Bug

**Why duplicate HTTP client code?**

1. **Complete isolation** - Each script can evolve independently
2. **No import complexity** - Copy file, it works
3. **Version stability** - Changes don't break other scripts
4. **Context efficiency** - No need to load shared modules
5. **Portability** - One file = one tool

**Trade-off accepted**: ~50 lines of HTTP code per script vs. shared import overhead and coupling.

## How It Works

### For AI Agents

1. **Agent loads** script via prime prompt or direct file read
2. **Agent executes** `uv run script.py` with args
3. **Script runs** with embedded dependencies (no install)
4. **Script makes** direct HTTP call
5. **Agent preserves** context (only loaded one script)

### For Humans

```bash
cd apps/3_file_system_scripts/scripts

# Run directly with uv
uv run status.py
uv run markets.py --limit 10
uv run search.py "best ai"
uv run market.py PREZ2024-DEM-1
```

## Inline Dependencies (uv magic)

Each script uses [PEP 723](https://peps.python.org/pep-0723/) inline metadata:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "httpx",
# ]
# ///
```

**What this means:**
- ✅ No virtual environment needed
- ✅ No `pip install` needed
- ✅ Dependencies declared in script
- ✅ `uv` handles everything automatically

## Context Efficiency Comparison

### Token consumption per operation:

| Approach | Initial Load | Per Operation | Total (3 ops) |
|----------|-------------|---------------|---------------|
| MCP Server | 1500 | 1500 each | 4500 |
| CLI | 800 | 100 each | 1100 |
| **Scripts** | **0** | **250-300 each** | **750-900** |

**Scripts use 83% fewer tokens than MCP, 31% fewer than CLI** (for 3 operations).

## Path Resolution

All scripts use absolute path resolution:

```python
from pathlib import Path

# Always resolves to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"
```

**Why this matters:**
- Works when invoked from any directory
- Cache location is consistent
- No relative path issues

## Usage

### Installation

```bash
# Install uv (if not already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# No other setup needed!
```

### Running Scripts

```bash
cd apps/3_file_system_scripts/scripts

# Check status
uv run status.py

# List markets
uv run markets.py --limit 5

# Search (builds cache on first run)
uv run search.py "election"

# Get specific market
uv run market.py TICKER-NAME
```

### Prime Prompt for AI

Use `/prime_file_system_scripts` to load script documentation:

```
In Claude: "/prime_file_system_scripts"
In Claude: "kalshi: Get exchange status"
In Claude: "kalshi: Search for markets about AI"
```

## Search Caching (Shared Across Scripts)

Even though scripts are isolated, they share a cache directory:

**Location**: `.kalshi_cache/` at project root
**First search**: 2-5 minutes (builds cache)
**Subsequent**: Instant
**TTL**: 6 hours

Each script independently manages cache but reads/writes to same location.

## When to Use Scripts

### ✅ Choose Scripts if:

1. **Context preservation critical** - Need maximum efficiency
2. **Lots of tools** - Don't need them all at once
3. **High portability** - Just copy Python files
4. **Independent operations** - Tools don't need to share state
5. **Iterative development** - Modify one tool without affecting others

### ❌ Avoid Scripts if:

1. **Using Claude Code** - Skills are better (same scripts + auto-discovery)
2. **Shared state needed** - Tools must coordinate
3. **Want auto-discovery** - MCP or Skills are better
4. **Humans need CLI** - CLI approach is better for dual-purpose

## Real-World Fit

### Ideal For:
- One-off integrations
- Research tools
- Data science workflows
- Portable utilities
- Team script libraries

### Not Ideal For:
- Interactive CLIs
- Stateful workflows
- Enterprise standardization (use MCP)
- Claude Code projects (use Skills)

## Comparison to Other Approaches

| Aspect | MCP Server | CLI | **Scripts** | Skills |
|--------|-----------|-----|-------------|--------|
| Context preservation | ❌ Poor | 😐 Medium | **✅ Excellent** | ✅ Excellent |
| Token efficiency | ❌ Poor | 😐 Medium | **✅ Excellent** | ✅ Excellent |
| Auto-discovery | ✅ Yes | ❌ No | **❌ No** | ✅ Yes |
| Portability | 😐 Medium | 😐 Medium | **✅ Excellent** | 😐 Medium |
| Code duplication | ✅ None | ✅ None | **❌ High** | ❌ High |
| Independence | ❌ No | ❌ No | **✅ Complete** | ✅ Complete |

## Migration Path

**Moving to Scripts:**

- **From MCP**: Extract tool logic into individual scripts
- **From CLI**: Break commands into separate files
- **To Skills**: Wrap scripts in SKILL.md (same files!)

## Related Documentation

- [Skills approach](skills.md) - Same pattern + auto-discovery
- [Standalone Scripts Deep Dive](../deep-dives/standalone-scripts.md) - Technical details
- [Decision Guide](../guides/decision-guide.md) - Choose the right approach
- [Best Practices](../guides/best-practices.md) - Progressive disclosure patterns

## Code Location

```
apps/3_file_system_scripts/
└── scripts/
    ├── status.py           # ~200 lines
    ├── markets.py          # ~250 lines
    ├── market.py           # ~200 lines
    ├── orderbook.py        # ~200 lines
    ├── trades.py           # ~200 lines
    ├── search.py           # ~300 lines (includes cache)
    ├── events.py           # ~220 lines
    ├── event.py            # ~200 lines
    ├── series_list.py      # ~250 lines
    └── series.py           # ~200 lines
```

---

**Navigation**: [← Back to approaches](README.md) | [Next: Skills →](skills.md)
