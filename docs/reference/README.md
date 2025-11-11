# Reference: Quick Lookups & Comparisons

> **Progressive Disclosure**: This is a category index. Read this for an overview, then access specific reference materials as needed.

## Overview

Quick reference materials for fast lookups, comparisons, and definitions. Use these when you need specific information without reading full guides.

## Reference Documents

### [cheat-sheet.md](cheat-sheet.md) ⭐
**One-page quick reference**

Everything you need on a single page: decision tree, comparison table, commands, and best practices.

**Use this when:**
- You need a quick reminder
- You're referencing while coding
- You want everything in one place

**Time**: 1 min scan

---

### [glossary.md](glossary.md)
**Term definitions**

Clear, simple definitions of all concepts, patterns, and terminology used in this repository.

**Use this when:**
- You encounter an unfamiliar term
- You need a precise definition
- You're explaining concepts to others

**Time**: Reference as needed

---

### [trade-off-comparison.md](trade-off-comparison.md)
**Detailed comparison matrix**

Comprehensive comparison of all 4 approaches across 10+ dimensions including context, performance, complexity, and use cases.

**Use this when:**
- Making architectural decisions
- Need detailed comparison
- Evaluating trade-offs

**Time**: 5 min read

---

### [api-details.md](api-details.md)
**Technical specifications**

Kalshi API details, caching implementation, path resolution, and other technical specifics.

**Use this when:**
- Implementing similar patterns
- Debugging issues
- Understanding internals

**Time**: Reference as needed

## Quick Lookup Tables

### Approach Selection (Ultra-Quick)

| If you have... | Use this |
|----------------|----------|
| External tool | MCP Server |
| New tool for humans + AI | CLI |
| Context critical | Scripts or Skills |
| Using Claude Code | Skills |
| Need portability | Scripts |

### Token Efficiency (3 operations)

| Approach | Token Consumption |
|----------|------------------|
| MCP Server | ~4500 tokens |
| CLI | ~1100 tokens |
| Scripts | ~750 tokens |
| Skills | ~750 tokens |

### Auto-Discovery

| Approach | Auto-Discovered? |
|----------|-----------------|
| MCP Server | ✅ Yes |
| CLI | ❌ No |
| Scripts | ❌ No |
| Skills | ✅ Yes |

### Customizable

| Approach | Can Customize? |
|----------|---------------|
| MCP Server | ❌ No (unless you own it) |
| CLI | ✅ Yes |
| Scripts | ✅ Yes |
| Skills | ✅ Yes |

## Common Lookups

### Command Examples

**MCP Server:**
```bash
claude --mcp-config .mcp.json
# In Claude: "kalshi: get exchange status"
```

**CLI:**
```bash
cd apps/2_cli
uv run kalshi status
uv run kalshi search "AI"
```

**Scripts:**
```bash
cd apps/3_file_system_scripts/scripts
uv run status.py
uv run search.py "AI"
```

**Skills:**
```bash
cd apps/4_skill
claude
# In Claude: "kalshi markets: get status"
```

### File Locations

```
beyond-mcp/
├── apps/
│   ├── 1_mcp_server/          # MCP implementation
│   ├── 2_cli/                  # CLI implementation
│   ├── 3_file_system_scripts/  # Scripts implementation
│   └── 4_skill/                # Skills implementation
│
├── docs/                       # This documentation
└── .kalshi_cache/             # Shared cache directory
```

### Key Concepts

**Progressive Disclosure**: Loading only what's needed, when it's needed

**Context Preservation**: Maintaining conversational memory across tool calls

**Prime Prompt**: Initial instructions that guide AI behavior

**Inline Dependencies**: PEP 723 script metadata for zero-install execution

**Agent Skills**: Claude Code's auto-discovery system

See [glossary.md](glossary.md) for full definitions.

## Quick Decision Tree

```
External tool?
├─ Yes → MCP Server
└─ No ↓

Building new?
├─ Yes ↓
└─ No → MCP Server

Context critical?
├─ No → CLI
└─ Yes ↓

Using Claude Code?
├─ Yes → Skills
└─ No → Scripts
```

## Related Documentation

**For choosing an approach:**
→ [../guides/decision-guide.md](../guides/decision-guide.md)

**For implementation patterns:**
→ [../guides/best-practices.md](../guides/best-practices.md)

**For detailed approach info:**
→ [../approaches/README.md](../approaches/README.md)

**For deep technical details:**
→ [../deep-dives/README.md](../deep-dives/README.md)

---

**Navigation**: [← Back to docs root](../README.md) | [Next: Deep Dives →](../deep-dives/README.md)
