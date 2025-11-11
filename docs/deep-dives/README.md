# Deep Dives: In-Depth Technical Explorations

> **Progressive Disclosure**: This is a category index. These are comprehensive technical documents - read only when you need deep understanding.

## Overview

In-depth technical explorations of specific patterns, implementations, and architectural decisions. These documents go beyond practical guidance to explain the "why" and "how" in detail.

## Deep Dive Documents

### [standalone-scripts.md](standalone-scripts.md) ⭐⭐⭐
**Understanding `uv` + inline dependencies pattern**

Comprehensive explanation of the standalone scripts pattern including PEP 723 inline metadata, path resolution, code duplication trade-offs, and implementation details.

**Topics covered:**
- PEP 723 inline script metadata
- `uv run --script` execution model
- Embedded vs. shared dependencies
- Path resolution strategies
- Why code duplication is intentional
- Self-contained script architecture

**Read this if:**
- Implementing standalone scripts
- Want to understand PEP 723
- Curious about `uv` capabilities
- Evaluating code duplication trade-offs

**Time**: 10-15 min read

---

### [context-preservation.md](context-preservation.md) ⭐⭐
**Theory and practice of context preservation**

Deep dive into why context preservation matters, how different approaches handle it, token economics, and strategies for maintaining conversational memory.

**Topics covered:**
- What is context and why it matters
- Context loss in MCP protocol
- Progressive disclosure theory
- Token consumption analysis
- Multi-turn conversation patterns
- Context window optimization

**Read this if:**
- Building context-sensitive tools
- Optimizing token consumption
- Understanding LLM context windows
- Evaluating architectural trade-offs

**Time**: 12-15 min read

---

### [search-caching.md](search-caching.md) ⭐
**Implementation details of the search cache**

Technical deep dive into the search caching implementation: why it's needed, how it works, TTL management, and pandas-based local search.

**Topics covered:**
- Why Kalshi has no native search
- Building comprehensive cache
- TTL and refresh strategies
- Pandas DataFrame search
- Cache sharing across approaches
- Performance characteristics

**Read this if:**
- Implementing similar caching
- Understanding cache architecture
- Debugging cache issues
- Building search on non-searchable APIs

**Time**: 8-10 min read

---

## Quick Navigation

### By Topic

**Implementation patterns** → [standalone-scripts.md](standalone-scripts.md)

**Architectural theory** → [context-preservation.md](context-preservation.md)

**Specific feature** → [search-caching.md](search-caching.md)

### By Approach

**Scripts/Skills** → [standalone-scripts.md](standalone-scripts.md) + [context-preservation.md](context-preservation.md)

**Search functionality** → [search-caching.md](search-caching.md)

**All approaches** → [context-preservation.md](context-preservation.md)

## When to Read These

### You're implementing...

**Standalone scripts**
→ Start with [standalone-scripts.md](standalone-scripts.md)

**Context-sensitive workflows**
→ Start with [context-preservation.md](context-preservation.md)

**Search/caching features**
→ Start with [search-caching.md](search-caching.md)

### You want to understand...

**Why code is duplicated**
→ [standalone-scripts.md](standalone-scripts.md) - "Code Duplication: A Feature"

**Why MCP loses context**
→ [context-preservation.md](context-preservation.md) - "Context Loss in MCP"

**How search works**
→ [search-caching.md](search-caching.md) - "Building the Cache"

**Token efficiency**
→ [context-preservation.md](context-preservation.md) - "Token Economics"

### You're debugging...

**Script execution issues**
→ [standalone-scripts.md](standalone-scripts.md) - "Common Issues"

**Context problems**
→ [context-preservation.md](context-preservation.md) - "Context Patterns"

**Cache not working**
→ [search-caching.md](search-caching.md) - "Cache Management"

## Learning Path

### For Implementers

1. **Start**: [standalone-scripts.md](standalone-scripts.md)
   - Learn the core pattern
   - Understand PEP 723
   - See implementation examples

2. **Then**: [context-preservation.md](context-preservation.md)
   - Understand the theory
   - Learn optimization strategies
   - See token analysis

3. **Finally**: [search-caching.md](search-caching.md)
   - Add search capability
   - Implement caching
   - Optimize performance

### For Architects

1. **Start**: [context-preservation.md](context-preservation.md)
   - Core architectural principle
   - Understand trade-offs
   - See analysis

2. **Then**: [standalone-scripts.md](standalone-scripts.md)
   - Implementation strategy
   - Code organization
   - Duplication rationale

3. **Reference**: [search-caching.md](search-caching.md)
   - Feature-specific details
   - As needed

### For Curious Readers

Read in any order based on interest. Each document is self-contained.

## Related Documentation

**For practical guidance:**
→ [../guides/best-practices.md](../guides/best-practices.md)

**For approach details:**
→ [../approaches/README.md](../approaches/README.md)

**For quick reference:**
→ [../reference/README.md](../reference/README.md)

**For conceptual overview:**
→ [../overview/README.md](../overview/README.md)

## Topics NOT Covered Here

These deep dives focus on patterns and architecture. For other topics:

**API endpoints** → [../reference/api-details.md](../reference/api-details.md)

**Quick decisions** → [../guides/decision-guide.md](../guides/decision-guide.md)

**Getting started** → [../overview/quick-start.md](../overview/quick-start.md)

**Comparison tables** → [../reference/trade-off-comparison.md](../reference/trade-off-comparison.md)

---

**Navigation**: [← Back to docs root](../README.md) | [↑ To top](#deep-dives-in-depth-technical-explorations)
