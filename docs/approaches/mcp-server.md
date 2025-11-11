# Approach 1: MCP Server

> **Classic Model Context Protocol implementation**

## Overview

The MCP Server approach uses the standardized Model Context Protocol to expose tools to any MCP-compatible AI client. This is the "standard" way to build AI tools.

## Architecture

```
Claude/LLM → MCP Protocol → MCP Server → subprocess → CLI → Kalshi API
            [context lost]                    [overhead]
```

**Location**: `apps/1_mcp_server/`

## Key Characteristics

### ✅ Strengths

- **Standardized integration** - Works with any MCP-compatible client
- **Tool discovery** - Auto-exposes 15 tools to LLMs
- **Clean abstractions** - MCP protocol handles complexity
- **Wide compatibility** - Not tied to specific AI/client

### ❌ Weaknesses

- **Instant context loss** - Every tool call loses conversational context
- **Wrapper overhead** - Delegates to CLI via subprocess
- **High token consumption** - Full tool definitions loaded each time
- **Limited customization** - Unless you own the server

## Implementation Details

### Tool Count
**15 tools** exposed via FastMCP:
- Exchange status
- Market operations (list, get, orderbook, trades)
- Event operations (list, get)
- Series operations (list, get)
- Search functionality
- And more...

### Core Files

**`server.py`** - FastMCP server definition
- Wraps CLI commands in MCP tool interface
- Each tool is stateless
- Protocol handles discovery & invocation

### How It Works

1. **Client connects** to MCP server
2. **Server advertises** available tools
3. **Client makes request** (e.g., "get exchange status")
4. **Server receives request** via MCP protocol
5. **Server calls CLI** via subprocess
6. **CLI executes** and returns result
7. **Server forwards** response to client
8. **Context is lost** - next request starts fresh

## Context Loss Example

```
User: "Get the exchange status"
AI: [Calls MCP tool, sees status is active]
    "The exchange is currently active"

User: "What was that status again?"
AI: [No memory of previous call]
    "I'll check..." [Makes new MCP call]
```

The AI must re-query because context is not preserved between tool calls.

## Usage

### Setup

```bash
# Copy test config
cp .mcp.testing .mcp.json

# Start Claude with MCP config
claude --mcp-config .mcp.json
```

### Example Interactions

```
In Claude: "kalshi: get exchange status"
In Claude: "kalshi: list markets about AI"
In Claude: "kalshi: search for 'election' events"
```

## Token Consumption

**Per tool call**: ~1000-1500 tokens
- Full tool definitions
- MCP protocol overhead
- CLI wrapper code

**Cumulative**: Grows linearly with tool calls

## When to Use MCP Server

### ✅ Choose MCP if:

1. **Using external tools** you don't control
2. **Need standardization** across multiple AI clients
3. **Building for ecosystem** - want wide compatibility
4. **Context loss acceptable** - tools are simple/stateless
5. **Want auto-discovery** - client automatically finds tools

### ❌ Avoid MCP if:

1. **Context critical** - need conversational memory
2. **Building custom tools** - you control the code
3. **Token efficiency matters** - operating at scale
4. **Iterative workflows** - tools build on each other

## Real-World Fit

### Ideal For:
- Third-party tool integration (GitHub, Slack, etc.)
- Simple, stateless operations
- Multi-client deployments
- Standardized enterprise tools

### Not Ideal For:
- Conversational workflows
- Context-dependent operations
- High-frequency tool use
- Custom team tooling

## Comparison to Other Approaches

| Aspect | MCP Server | CLI | Scripts | Skills |
|--------|-----------|-----|---------|--------|
| Context preservation | ❌ Poor | 😐 Medium | ✅ Good | ✅ Excellent |
| Token efficiency | ❌ Poor | 😐 Medium | ✅ Good | ✅ Excellent |
| Auto-discovery | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| Portability | ✅ High | 😐 Medium | ✅ High | ❌ Low |
| Customizable | ❌ No* | ✅ Yes | ✅ Yes | ✅ Yes |

*Unless you own/fork the server

## Migration Path

**Moving from MCP to other approaches:**

- **To CLI**: Extract core logic from MCP wrappers
- **To Scripts**: Break down into individual operations
- **To Skills**: Wrap scripts in SKILL.md for Claude Code

## Related Documentation

- [CLI approach](cli.md) - Single source of truth alternative
- [Scripts approach](scripts.md) - Progressive disclosure pattern
- [Skills approach](skills.md) - Best of both worlds
- [Decision Guide](../guides/decision-guide.md) - Choose the right approach

## External Resources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Spec](https://modelcontextprotocol.io/)

---

**Navigation**: [← Back to approaches](README.md) | [Next: CLI →](cli.md)
