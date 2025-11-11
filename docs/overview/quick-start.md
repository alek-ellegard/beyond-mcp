# Quick Start Guide

> Try all 4 approaches in under 10 minutes

## Prerequisites

- Python 3.8+ with `uv` installed ([installation](https://docs.astral.sh/uv/))
- Claude Code CLI (for Skills approach)

## 1. MCP Server (2 min)

**What it does**: Standardized tool protocol, works with any MCP client

```bash
# Setup
cp .mcp.testing .mcp.json

# Run with MCP config
claude --mcp-config .mcp.json

# Try it
# In Claude: "kalshi: get exchange status"
```

**What happens**: Claude discovers 15 tools automatically, but loses context on each call.

---

## 2. CLI (2 min)

**What it does**: Command-line interface for both humans and AI

```bash
# By AI agent
claude

# Load CLI tools
# In Claude: "/prime_kalshi_cli_tools"

# Try it
# In Claude: "kalshi: Get exchange status"
# In Claude: "kalshi: List events"
```

**Or use directly:**
```bash
cd apps/2_cli
uv sync
uv run kalshi status
uv run kalshi events --json --limit 10
```

**What happens**: AI reads CLI help text, executes commands, preserves more context than MCP.

---

## 3. File System Scripts (3 min)

**What it does**: Individual standalone scripts with progressive disclosure

```bash
# By AI agent
claude

# Load scripts via slash command
# In Claude: "/prime_file_system_scripts"

# Try it
# In Claude: "kalshi: Get exchange status"
# In Claude: "kalshi: List events"
```

**Or use directly:**
```bash
cd apps/3_file_system_scripts/scripts
uv run status.py
uv run markets.py --limit 10
uv run search.py "best ai"
```

**What happens**: AI only reads the specific script it needs (~200-300 lines), maximum context efficiency.

---

## 4. Skills (3 min)

**What it does**: Claude Code agent skills with auto-discovery

```bash
cd apps/4_skill/

claude

# Try it (auto-discovered)
# In Claude: "kalshi markets: Get exchange status"
# In Claude: "kalshi markets: search for events about 'best ai'"
```

**First search note**: Initial search builds cache (2-5 min), then instant.

**What happens**: Claude automatically discovers skill based on your query, loads only needed scripts, best context preservation.

---

## Understanding the Output

All 4 approaches return the same data, just accessed differently:

### Exchange Status
```json
{
  "trading_active": true,
  "exchange_active": true
}
```

### Events List
Each approach returns event data with:
- `event_ticker`: Unique identifier
- `title`: Event description
- `category`: Classification
- `markets`: Available markets

## What You Learned

1. **MCP**: Auto-discovery, context loss, standardized
2. **CLI**: Dual-purpose, better context, requires invocation
3. **Scripts**: Maximum efficiency, progressive disclosure, manual discovery
4. **Skills**: Best of both worlds (for Claude Code)

## Next Steps

**Want to understand the approaches deeply?**
→ Read [../approaches/README.md](../approaches/README.md)

**Ready to choose one for your project?**
→ Check [../guides/decision-guide.md](../guides/decision-guide.md)

**Want to see real code examples?**
→ Explore [../guides/examples-walkthrough.md](../guides/examples-walkthrough.md)

---

**Navigation**: [← Back to overview](README.md) | [↑ Docs root](../README.md)
