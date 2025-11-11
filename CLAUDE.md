# Beyond-MCP: Context for Claude Code

> This file is automatically loaded by Claude Code. It provides essential context about this repository using progressive disclosure.

## Project Overview

**Purpose**: Demonstrate 4 different approaches to building AI toolsets, comparing trade-offs between context preservation, portability, and complexity.

**Core Insight**: MCP Servers aren't always the best choice. Context preservation matters at scale.

## The 4 Approaches (Implemented)

All 4 approaches implement **identical functionality** (Kalshi prediction market access):

1. **MCP Server** (`apps/1_mcp_server/`)
   - Standard MCP protocol
   - ❌ Context lost every call
   - ✅ Works with any MCP client

2. **CLI** (`apps/2_cli/`)
   - Command-line interface
   - 😐 Partial context preservation
   - ✅ Human + AI use

3. **File System Scripts** (`apps/3_file_system_scripts/`)
   - Standalone Python scripts
   - ✅ Excellent context preservation
   - ✅ Progressive disclosure by design

4. **Skills** (`apps/4_skill/`)
   - Claude Code agent skills
   - ✅✅ Best context + auto-discovery
   - ⚠️ Claude Code specific

## Quick Selection Guide

**User asks about external tools** → MCP Server

**User building new tool** → CLI (most cases)

**User needs context efficiency** → Scripts or Skills

**User using Claude Code** → Skills

## Documentation Structure (Progressive Disclosure)

**Entry point**: `docs/README.md` - Lightweight navigation map

**Categories**:
- `docs/overview/` - Core concepts (2-3 min read)
- `docs/approaches/` - Detailed approach docs (15 min total)
- `docs/guides/` - Practical guidance (20 min total)
- `docs/reference/` - Quick lookups (reference)
- `docs/deep-dives/` - Technical deep dives (30+ min each)

**Pattern**: Read category README first, then specific documents as needed.

## Key Files for Common Tasks

### Understanding the project
→ Read `docs/overview/README.md` (2 min)

### Choosing an approach
→ Read `docs/guides/decision-guide.md` (3 min)

### Implementation details
→ Read `docs/approaches/[approach-name].md` (5 min each)

### Best practices
→ Read `docs/guides/best-practices.md` (8 min)

### Quick reference
→ Read `docs/reference/cheat-sheet.md` (1 min)

### Deep technical details
→ Read `docs/deep-dives/[topic].md` (10-30 min)

## Project Structure

```
beyond-mcp/
├── apps/
│   ├── 1_mcp_server/          # Approach 1: MCP Server
│   ├── 2_cli/                  # Approach 2: CLI
│   ├── 3_file_system_scripts/  # Approach 3: Scripts
│   └── 4_skill/                # Approach 4: Skills
│
├── docs/                       # ⭐ LLM-optimized documentation
│   ├── README.md               # Start here (navigation hub)
│   ├── overview/               # Core concepts
│   ├── approaches/             # Detailed approach docs
│   ├── guides/                 # Practical guidance
│   ├── reference/              # Quick lookups
│   └── deep-dives/             # Technical deep dives
│
├── .kalshi_cache/             # Shared cache directory
├── README.md                   # Main project README
└── CLAUDE.md                   # This file (auto-loaded)
```

## Important Context: Progressive Disclosure Pattern

This repository **intentionally** uses progressive disclosure:

- **Don't** load all documentation upfront
- **Do** start with `docs/README.md`
- **Do** navigate to specific categories as needed
- **Do** load specific documents only when relevant

**Reason**: Minimize token consumption while maximizing information access.

## Implementation Patterns to Note

### 1. Code Duplication (Scripts/Skills)

**Intentional**: Each script embeds HTTP client (~50 lines duplicated)

**Why**: Context efficiency > code DRY
- AI reads one file (200-300 tokens)
- Not import chain (1000+ tokens)

### 2. Caching Strategy

**Location**: `.kalshi_cache/` at project root

**Pattern**: Build once (2-5 min), use forever (instant)

**TTL**: 6 hours

**Shared by**: CLI, Scripts, Skills

### 3. Path Resolution

**Pattern**: Absolute paths via `Path(__file__).resolve()`

**Why**: Works from any working directory

**Example**:
```python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = PROJECT_ROOT / ".kalshi_cache"
```

### 4. Inline Dependencies (PEP 723)

**Pattern**: Scripts declare dependencies in file

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["httpx"]
# ///
```

**Benefit**: No virtual environment or pip install needed

## Common User Questions

### "Which approach should I use?"

→ Direct to `docs/guides/decision-guide.md`

3-question decision tree provides answer.

### "How do I implement [specific approach]?"

→ Direct to `docs/approaches/[approach].md`

Each approach has dedicated documentation.

### "Why is code duplicated in scripts?"

→ Direct to `docs/deep-dives/standalone-scripts.md`

Section: "Code Duplication: A Feature, Not a Bug"

### "How does caching work?"

→ Direct to `docs/deep-dives/search-caching.md`

Complete implementation details.

### "What are best practices?"

→ Direct to `docs/guides/best-practices.md`

10 core principles with examples.

## Working with This Repository

### Running Examples

Each approach has a README with usage examples:
- `apps/1_mcp_server/README.md`
- `apps/2_cli/README.md`
- `apps/3_file_system_scripts/README.md`
- `apps/4_skill/README.md`

### Testing

Standard pytest in each approach directory.

### Adding Features

Follow the approach's pattern:
- MCP: Add tool to `server.py`
- CLI: Add command to `cli.py`
- Scripts: Add new script file
- Skills: Add new script + update SKILL.md

## Documentation Philosophy

This documentation is designed for **progressive disclosure**:

1. **Lightweight entry** - This file + `docs/README.md`
2. **Category navigation** - Each category has README index
3. **Specific documents** - Load only what's needed
4. **Deep dives** - Optional, for deep understanding

**Token efficiency**: Start with ~1000 tokens (this file + docs README), navigate to specific documents (~500-2000 tokens each) as needed.

**Traditional documentation**: Load everything upfront (~10,000+ tokens)

**Savings**: 80-90% fewer tokens for typical tasks

## Key Takeaways

1. **No "best" approach** - Trade-offs depend on use case
2. **Context preservation** - Critical at scale
3. **Progressive disclosure** - Load only what's needed
4. **Code duplication** - Sometimes optimal for AI
5. **Documentation structure** - Designed for LLM navigation

## Next Steps for Users

**First-time visitors**: Start with `docs/README.md`

**Specific question**: Navigate to relevant category

**Implementation**: Read approach-specific doc

**Deep understanding**: Read deep-dives

---

**This file optimizes your context window. Navigate progressively to minimize token consumption.**
