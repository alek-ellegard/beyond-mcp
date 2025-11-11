# Approaches: The 4 Ways to Build AI Tools

> **Progressive Disclosure**: This is a category index. Read this for comparison, then dive into specific approaches as needed.

## Overview

This repository demonstrates **4 different approaches** to building the same functionality (Kalshi prediction market access):

1. [MCP Server](mcp-server.md) - The standard way
2. [CLI](cli.md) - The flexible way
3. [Scripts](scripts.md) - The efficient way
4. [Skills](skills.md) - The smart way

## High-Level Comparison

| Approach | Best For | Context | Discovery | Complexity |
|----------|----------|---------|-----------|------------|
| **[MCP Server](mcp-server.md)** | External tools, standardization | ❌ Loses | ✅ Auto | Low |
| **[CLI](cli.md)** | New tools, human + AI use | 😐 Medium | ❌ Manual | Medium |
| **[Scripts](scripts.md)** | Max efficiency, portability | ✅ Preserves | ❌ Manual | Medium |
| **[Skills](skills.md)** | Claude Code, team collab | ✅✅ Best | ✅ Auto | Medium |

## Visual Architecture Comparison

### Data Flow

```
MCP Server:
Claude → MCP Protocol → MCP Server → subprocess → CLI → API
        [context lost]                    [overhead]

CLI:
Claude → subprocess → CLI → Direct HTTP → API
        [some context]    [medium overhead]

Scripts:
Claude → Read tool → Script → Embedded HTTP → API
        [context preserved] [minimal overhead]

Skills:
Claude → Skill loader → Script → Embedded HTTP → API
        [context preserved] [auto-discovery]
```

## Key Differentiators

### Context Window Consumption

**Ranking (best to worst):**
1. **Scripts/Skills**: ~200-300 lines per script (progressive disclosure)
2. **CLI**: ~500-800 lines (help text + implementation)
3. **MCP Server**: ~1000+ lines (full tool definitions + wrappers)

### Invocation Method

**Agent-invoked (automatic):**
- MCP Server ✅
- Skills ✅

**Manual invocation (AI must decide):**
- CLI ❌
- Scripts ❌

### Customizability

**Full control:**
- CLI ✅
- Scripts ✅
- Skills ✅

**Limited control:**
- MCP Server ❌ (unless you own it)

### Portability

**Works anywhere:**
- Scripts ✅ (just Python + httpx)
- Skills ✅ (portable but Claude Code-specific)

**Requires setup:**
- CLI ⚠️ (needs installation)
- MCP Server ⚠️ (needs MCP client)

## Detailed Architecture

### 1. MCP Server

**Pattern**: Wrapper around existing CLI

- 15 tool definitions in FastMCP
- Each tool calls CLI via subprocess
- MCP protocol handles discovery & invocation
- Context lost on every call

**Read more**: [mcp-server.md](mcp-server.md)

---

### 2. CLI

**Pattern**: Single-purpose command-line tool

- 13 commands in one CLI
- Direct HTTP calls (no SDK)
- Dual output modes (human/JSON)
- Smart caching for search

**Read more**: [cli.md](cli.md)

---

### 3. Scripts

**Pattern**: Standalone executable files

- 10 independent scripts
- Each ~200-300 lines
- Embedded HTTP client
- Progressive disclosure by design

**Read more**: [scripts.md](scripts.md)

---

### 4. Skills

**Pattern**: Claude Code agent skill system

- Same scripts as approach #3
- Wrapped in SKILL.md for discovery
- Auto-invoked by Claude
- Git-based sharing

**Read more**: [skills.md](skills.md)

---

## Choosing Between Approaches

### Quick Decision Tree

```
Is it an external tool you don't control?
├─ Yes → MCP Server
└─ No → Continue

Are you building something new?
├─ Yes → CLI (80% of time)
└─ No → Continue

Is context preservation critical?
├─ Yes → Scripts or Skills
│   └─ Using Claude Code? → Skills
│   └─ Otherwise → Scripts
└─ No → CLI
```

### By Use Case

**External tool integration**
→ [MCP Server](mcp-server.md)

**New tool for humans and AI**
→ [CLI](cli.md)

**Maximum context efficiency**
→ [Scripts](scripts.md)

**Claude Code team tooling**
→ [Skills](skills.md)

## Documents in This Category

### [mcp-server.md](mcp-server.md)
**Approach 1: Model Context Protocol**
- Architecture & implementation details
- 15 tools auto-discovered
- Wrapper pattern around CLI
- When to use MCP

### [cli.md](cli.md)
**Approach 2: Command-Line Interface**
- Single source of truth design
- 13 commands with dual output
- Smart caching implementation
- CLI best practices

### [scripts.md](scripts.md)
**Approach 3: Standalone Scripts**
- Progressive disclosure pattern
- 10 self-contained scripts
- Embedded dependencies
- Context optimization

### [skills.md](skills.md)
**Approach 4: Claude Code Skills**
- Agent skill architecture
- Auto-discovery mechanism
- Git-based collaboration
- Skill-specific patterns

## Next Steps

**For implementation details:**
→ Read individual approach documents above

**To make a decision:**
→ Check [../guides/decision-guide.md](../guides/decision-guide.md)

**For best practices:**
→ See [../guides/best-practices.md](../guides/best-practices.md)

---

**Navigation**: [← Back to docs root](../README.md) | [Next: Guides →](../guides/README.md)
