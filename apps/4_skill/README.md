# Kalshi Markets Skill

Claude Code Agent Skill for accessing Kalshi prediction market data with autonomous invocation and progressive disclosure.

## Features

- **Model-Invoked** - Claude autonomously activates based on context
- **Progressive Disclosure** - Only loads scripts when needed (~200-300 lines each)
- **Context Preservation** - Minimal token usage compared to MCP
- **Team Sharing** - Commit to git for team access
- **Zero Setup** - No server, no config, just works

## How It Works

```
Claude (detects keyword) -> Loads SKILL.md -> Runs relevant script -> Kalshi API
```

The skill automatically activates when Claude detects keywords like:
- "prediction markets"
- "Kalshi markets"
- "betting odds"
- "market prices"

## Quick Start

```bash
cd apps/4_skill/

claude

# Claude will auto-detect and use the skill
prompt: "What's the Kalshi exchange status?"
prompt: "Search for markets about llms"
prompt: "Show me recent trades"
```

## Available Scripts (10)

Each script is self-contained with embedded HTTP client:

- `status.py` - Exchange operational status
- `markets.py` - Browse markets with filters
- `market.py` - Detailed market information
- `orderbook.py` - Bid/ask depth
- `trades.py` - Recent trading activity
- `search.py` - Keyword search (with caching)
- `events.py` - List event collections
- `event.py` - Event details
- `series_list.py` - Browse all ~6900 series
- `series.py` - Series information

## Architecture

```
.claude/skills/kalshi-markets/
├── SKILL.md              # Skill description & trigger keywords
└── scripts/              # 10 standalone scripts (same as approach #3)
    ├── status.py
    ├── markets.py
    └── ...
```

## Advantages Over MCP

- **Context Preserved** - No context loss between calls
- **Progressive Loading** - Only read what you need
- **Git Shareable** - Commit once, team uses everywhere
- **No Server Required** - Pure filesystem, no processes
- **Fully Customizable** - Edit scripts and SKILL.md as needed

## When to Use

- Using Claude Code specifically
- Want autonomous skill discovery
- Context preservation is critical
- Team collaboration via git
- Building reusable team capabilities

## Development

All scripts support `--help` and `--json`:

```bash
uv run .claude/skills/kalshi-markets/scripts/status.py --help
uv run .claude/skills/kalshi-markets/scripts/search.py "bitcoin" --json
```

No authentication required for any script.
