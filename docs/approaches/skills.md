# Approach 4: Skills (Claude Code Agent Skills)

> **Claude Code Agent Skills with embedded scripts**

## Overview

The Skills approach wraps standalone scripts (same as Approach #3) in Claude Code's agent skill system. This combines the context efficiency of scripts with automatic discovery and invocation.

## Architecture

```
Claude (detects trigger) → Loads SKILL.md → Runs scripts → Kalshi API
                          [auto-discovery]  [context preserved]
```

**Location**: `apps/4_skill/.claude/skills/kalshi-markets/`

## Key Characteristics

### ✅ Strengths

- **Model-invoked** - Claude autonomously decides when to use
- **Progressive disclosure** - Same scripts as approach #3 (~200-300 lines each)
- **Team sharing** - Commit to git for team access
- **Discovery** - Description triggers automatic activation
- **Context preservation** - Agent reads only what's needed
- **Best of both worlds** - Auto-discovery + efficiency

### ⚠️ Trade-offs

- **Claude Code specific** - Only works in Claude Code
- **Learning curve** - Requires understanding Skill system
- **Less portable** - Tied to Claude Code ecosystem

## Implementation Details

### Structure

```
.claude/skills/kalshi-markets/
├── SKILL.md                    # Skill manifest & instructions
└── scripts/                    # Same 10 scripts from approach #3
    ├── status.py
    ├── markets.py
    ├── market.py
    ├── orderbook.py
    ├── trades.py
    ├── search.py
    ├── events.py
    ├── event.py
    ├── series_list.py
    └── series.py
```

### SKILL.md Manifest

The `SKILL.md` file tells Claude Code when and how to use this skill:

```markdown
# Kalshi Markets Skill

## Description
Access Kalshi prediction market data including events, markets, series,
orderbooks, and trades. Includes keyword search across all markets.

## Activation Criteria
- User asks about Kalshi prediction markets
- User wants to search or browse markets
- User needs event or series information
- Keywords: "kalshi", "prediction market", "betting market"

## Available Scripts
- status.py - Exchange operational status
- search.py - Keyword search across all markets
- markets.py - Browse markets with filters
- ...
```

### How Auto-Discovery Works

1. **User query** mentions "kalshi" or "prediction markets"
2. **Claude Code** scans SKILL.md descriptions
3. **Skill matches** activation criteria
4. **Claude loads** SKILL.md instructions
5. **Claude executes** appropriate script
6. **Context preserved** - only loaded one skill + one script

## Progressive Disclosure Layers

Skills implement **three-tier progressive disclosure**:

### Layer 1: Metadata (Always Loaded)
- Skill name: "kalshi-markets"
- Description: Brief summary
- Activation criteria: Keywords

**Cost**: ~50-100 tokens

### Layer 2: Instructions (Loaded When Activated)
- SKILL.md content
- Available scripts
- Usage examples

**Cost**: ~200-300 tokens

### Layer 3: Scripts (Loaded On Demand)
- Individual script files
- Only what's needed

**Cost**: ~200-300 tokens per script

**Total for one operation**: ~500-700 tokens vs. 1500+ for MCP

## How It Works

### Automatic Activation

```
User: "What's the status of Kalshi exchange?"

Claude (internal):
  1. Detects "Kalshi" keyword
  2. Scans skills, finds kalshi-markets
  3. Loads SKILL.md
  4. Reads scripts/status.py
  5. Executes: uv run status.py

Claude: "The Kalshi exchange is currently active and trading is enabled."
```

**No prime prompt needed** - Claude discovers and uses automatically.

### Manual Activation

You can also explicitly invoke:

```
User: "kalshi markets: search for AI events"

Claude:
  - Loads kalshi-markets skill
  - Runs scripts/search.py with "AI" query
  - Returns results
```

## Context Efficiency

### Comparison: Same Query, Different Approaches

**Query**: "Get Kalshi exchange status, then search for AI markets"

**MCP Server**:
```
Load: 15 tool definitions (1500 tokens)
Call 1: get_status (1500 tokens)
Call 2: search (1500 tokens)
Total: 4500 tokens
```

**CLI**:
```
Load: CLI help (800 tokens)
Call 1: kalshi status (100 tokens)
Call 2: kalshi search (100 tokens)
Total: 1000 tokens
```

**Scripts**:
```
Load: Nothing (0 tokens)
Call 1: status.py (250 tokens)
Call 2: search.py (300 tokens)
Total: 550 tokens
```

**Skills**:
```
Load: SKILL.md (200 tokens)
Call 1: status.py (250 tokens)
Call 2: search.py (300 tokens)
Total: 750 tokens
```

**Skills save 83% tokens vs. MCP, 25% vs. CLI**

## Team Collaboration via Git

### Sharing Skills

```bash
# Developer 1 creates skill
cd apps/4_skill/.claude/skills/
mkdir my-team-skill
# ... create SKILL.md and scripts ...

git add .claude/skills/my-team-skill
git commit -m "Add my-team-skill"
git push

# Developer 2 uses skill
git pull
claude  # Skill automatically discovered!
```

**Skills are just files** - version control works perfectly.

## Usage

### Setup

```bash
cd apps/4_skill/

# Skills are discovered automatically
claude
```

### Example Interactions

```
# Auto-discovered
"What's the Kalshi exchange status?"

# Explicit invocation
"kalshi markets: Get exchange status"
"kalshi markets: search for events about 'best ai'"
"kalshi markets: list markets with limit 10"
```

### First Search Note

First search builds cache (2-5 min), then instant. Same caching as Scripts approach.

## When to Use Skills

### ✅ Choose Skills if:

1. **Using Claude Code** - Designed specifically for it
2. **Want auto-discovery** - No prime prompts needed
3. **Team collaboration** - Git-based sharing
4. **Context critical** - Maximum efficiency needed
5. **Building reusable capabilities** - Not one-offs

### ❌ Avoid Skills if:

1. **Not using Claude Code** - Won't work elsewhere
2. **Need portability** - Use Scripts instead
3. **Using multiple AI clients** - Use MCP
4. **Humans need CLI** - Build CLI instead

## Real-World Fit

### Ideal For:
- Claude Code teams
- Shared team capabilities
- Auto-discovered tools
- Context-sensitive operations
- Frequently used workflows

### Not Ideal For:
- Non-Claude Code environments
- One-off scripts
- Multi-client deployments
- Standalone tools

## Comparison to Other Approaches

| Aspect | MCP Server | CLI | Scripts | **Skills** |
|--------|-----------|-----|---------|------------|
| Context preservation | ❌ Poor | 😐 Medium | ✅ Excellent | **✅ Excellent** |
| Token efficiency | ❌ Poor | 😐 Medium | ✅ Excellent | **✅ Excellent** |
| Auto-discovery | ✅ Yes | ❌ No | ❌ No | **✅ Yes** |
| Team sharing | 😐 Medium | 😐 Medium | ❌ Manual | **✅ Easy (git)** |
| Portability | ✅ High | 😐 Medium | ✅ High | **❌ Low** |
| Claude Code only | ❌ No | ❌ No | ❌ No | **✅ Yes** |

## Skills vs. Scripts

**Scripts** and **Skills** use the same underlying pattern (standalone Python files).

**Key difference**: Skills add auto-discovery via `SKILL.md`

### When to upgrade Scripts → Skills:

- Team needs automatic discovery
- Building for Claude Code specifically
- Want git-based sharing
- Skills are "part of the team"

### When to keep Scripts:

- Need portability beyond Claude Code
- One-off utilities
- Don't need auto-discovery
- Want maximum simplicity

## Migration Path

**Moving to Skills:**

- **From Scripts**: Add SKILL.md wrapper (scripts are identical!)
- **From CLI**: Break into scripts, add SKILL.md
- **From MCP**: Extract logic → scripts → wrap in SKILL.md

## Skill Development Best Practices

### 1. Clear Activation Criteria

```markdown
## Activation Criteria
- Specific keywords: "kalshi", "prediction market"
- User intent: searching markets, checking status
- Related domains: political betting, event trading
```

### 2. Concise Instructions

Keep SKILL.md focused:
- What the skill does (2-3 sentences)
- When to use it (bullet points)
- Available operations (list)
- Example usage (1-2 examples)

### 3. Organized Scripts

```
.claude/skills/my-skill/
├── SKILL.md              # Manifest
├── scripts/              # Standalone scripts
│   ├── common/           # Shared utilities (optional)
│   └── *.py              # Individual operations
└── README.md             # Documentation (optional)
```

### 4. Progressive Disclosure

- Each script does ONE thing
- Keep scripts 200-300 lines
- Embed dependencies (PEP 723)
- No complex imports

## Related Documentation

- [Scripts approach](scripts.md) - Same pattern without auto-discovery
- [Standalone Scripts Deep Dive](../deep-dives/standalone-scripts.md) - Implementation details
- [Best Practices](../guides/best-practices.md) - Progressive disclosure patterns
- [Claude Code Skills Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)

## Code Location

```
apps/4_skill/
└── .claude/skills/kalshi-markets/
    ├── SKILL.md                # Skill manifest
    └── scripts/                # Same 10 scripts as approach #3
        ├── status.py
        ├── markets.py
        ├── market.py
        ├── orderbook.py
        ├── trades.py
        ├── search.py
        ├── events.py
        ├── event.py
        ├── series_list.py
        └── series.py
```

---

**Navigation**: [← Back to approaches](README.md) | [↑ Docs root](../README.md)
