# Overview: What is Beyond-MCP?

> **Progressive Disclosure**: This is a category index. Read this for an overview, then navigate to specific documents as needed.

## The Core Problem

**MCP Servers cause instant context loss.** Every tool call forces the AI to forget conversational context, leading to inefficiency at scale.

When you have one or two MCP Servers, this isn't a big deal. But as you scale to many agents, tools, and contexts - this cost becomes a bottleneck.

## The Core Question

**Should we always use MCP Servers?**

The answer: **Not always!** This repository explores 4 different approaches, each with different trade-offs.

## The Two Fundamental Trade-offs

### 1. Context Preservation vs. Portability

- **MCP Servers**: Work everywhere, but AI forgets context
- **Alternative approaches**: Better context, but may be less portable

### 2. Standardization vs. Control

- **MCP Servers**: Standardized protocol, less customization
- **Alternative approaches**: Full control, requires more work

## What This Repository Demonstrates

This repo implements **the exact same functionality** (accessing Kalshi prediction market data) in **4 different ways**:

1. **MCP Server** - The standard approach
2. **CLI** - Command-line interface
3. **File System Scripts** - Standalone scripts with progressive disclosure
4. **Skills** - Claude Code agent skills

By comparing identical functionality across different approaches, you can clearly see the engineering trade-offs.

## Documents in This Category

### [quick-start.md](quick-start.md)
**Get started with each approach in 5 minutes**
- Installation steps
- First command to run
- What to expect
- ~3 min read

## Quick Summary Table

| Aspect | MCP Server | CLI | Scripts | Skills |
|--------|-----------|-----|---------|--------|
| **Context Loss** | High | Medium | Low | Low |
| **Portability** | High | Medium | Medium | Low |
| **Auto-Discovery** | Yes | No | No | Yes |
| **Customizable** | No* | Yes | Yes | Yes |
| **Complexity** | Low | Medium | Medium | Medium |

*Unless you own/fork the server

## Key Insight

**There is no "best" approach.** The right choice depends on:

- Who built it? (You or external)
- Who uses it? (Humans, AI, or both)
- What matters? (Portability or efficiency)
- Which AI? (Claude Code or any)

## Next Steps

**For conceptual understanding:**
→ Read [quick-start.md](quick-start.md) to try each approach

**For detailed comparison:**
→ Navigate to [../approaches/README.md](../approaches/README.md)

**To choose an approach:**
→ Jump to [../guides/decision-guide.md](../guides/decision-guide.md)

---

**Navigation**: [← Back to docs root](../README.md) | [Next: Quick Start →](quick-start.md)
