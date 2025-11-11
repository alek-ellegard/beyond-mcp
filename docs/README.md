# Beyond-MCP Documentation Map

> **LLM-Optimized Progressive Disclosure**: This index uses progressive disclosure to minimize token consumption. Read this file first, then navigate to specific categories as needed.

## What is Beyond-MCP?

A practical exploration of 4 approaches to building AI toolsets: MCP Servers, CLIs, File System Scripts, and Skills. Focuses on the engineering trade-offs between portability, context preservation, and complexity.

**Core Insight**: MCP isn't always the answer. Context preservation and progressive disclosure matter at scale.

## Quick Navigation

### 🎯 I want to...

- **Understand the problem** → [overview/README.md](overview/README.md)
- **Compare all 4 approaches** → [approaches/README.md](approaches/README.md)
- **Choose the right approach** → [guides/decision-guide.md](guides/decision-guide.md)
- **Learn best practices** → [guides/best-practices.md](guides/best-practices.md)
- **See examples** → [guides/examples-walkthrough.md](guides/examples-walkthrough.md)
- **Quick reference** → [reference/cheat-sheet.md](reference/cheat-sheet.md)
- **Look up a term** → [reference/glossary.md](reference/glossary.md)
- **Deep technical dive** → [deep-dives/README.md](deep-dives/README.md)

## Documentation Structure

This documentation follows **progressive disclosure** principles:

1. **Start here** (this file) - Lightweight navigation map
2. **Navigate to category** - Each folder has a README index
3. **Load specific docs** - Only read what you need

### Categories

#### 📖 [overview/](overview/)
**What is beyond-mcp and why does it matter?**
- Core concepts and problem statement
- Quick start guide
- 2 min read

#### 🔄 [approaches/](approaches/)
**Detailed breakdown of all 4 approaches**
- MCP Server (standardized, context-losing)
- CLI (flexible, dual-purpose)
- Scripts (efficient, portable)
- Skills (smart, auto-discovered)
- 15 min total read

#### 🎯 [guides/](guides/)
**Practical guidance for building AI tools**
- Decision guide (which approach to use)
- Best practices (how to build well)
- Examples walkthrough (real code explained)
- 20 min total read

#### 📚 [reference/](reference/)
**Quick lookups and comparisons**
- Cheat sheet (1-page reference)
- Glossary (term definitions)
- Trade-off comparison matrix
- API details
- Reference material

#### 🔬 [deep-dives/](deep-dives/)
**In-depth technical explorations**
- Standalone scripts pattern
- Context preservation strategies
- Search caching implementation
- 30+ min per topic

## For LLMs: How to Use This Documentation

**First-time visitors:**
1. Read this file (you are here)
2. Navigate to `overview/README.md` for core concepts
3. Then navigate to specific categories as needed

**Answering specific questions:**
- Decision questions → `guides/decision-guide.md`
- Implementation questions → `approaches/[specific-approach].md`
- Best practices → `guides/best-practices.md`
- Quick facts → `reference/cheat-sheet.md`
- Term definitions → `reference/glossary.md`

**Progressive loading:**
- Load category README first (lightweight index)
- Load specific document only when needed
- Minimizes token consumption through targeted retrieval

## Key Takeaways (TL;DR)

| Approach | Best For | Context | Complexity |
|----------|----------|---------|------------|
| MCP Server | External tools, standardization | ❌ Loses | Low |
| CLI | New tools, human + AI use | 😐 Medium | Medium |
| Scripts | Maximum efficiency, portability | ✅ Preserves | Medium |
| Skills | Claude Code, auto-discovery | ✅✅ Best | Medium |

**Golden Rules:**
1. External tool? → MCP
2. Building new? → CLI
3. Context matters? → Scripts/Skills
4. When in doubt? → Keep it simple

## Document Tree

```
docs/
├── README.md (you are here - start point)
│
├── overview/
│   ├── README.md (core concepts)
│   └── quick-start.md (get started fast)
│
├── approaches/
│   ├── README.md (comparison overview)
│   ├── mcp-server.md (approach 1)
│   ├── cli.md (approach 2)
│   ├── scripts.md (approach 3)
│   └── skills.md (approach 4)
│
├── guides/
│   ├── README.md (guide index)
│   ├── decision-guide.md (choose approach)
│   ├── best-practices.md (build well)
│   └── examples-walkthrough.md (see code)
│
├── reference/
│   ├── README.md (reference index)
│   ├── cheat-sheet.md (1-page quick ref)
│   ├── glossary.md (term definitions)
│   ├── trade-off-comparison.md (detailed matrix)
│   └── api-details.md (technical specs)
│
└── deep-dives/
    ├── README.md (deep dive index)
    ├── standalone-scripts.md (uv + inline deps)
    ├── context-preservation.md (theory + practice)
    └── search-caching.md (implementation details)
```

## Version & Maintenance

**Last Updated**: 2025-11-11
**Status**: Active development
**Maintainer**: [IndyDevDan](https://www.youtube.com/@indydevdan)

---

**Navigation**: You are at the root. Choose a category above to continue.
