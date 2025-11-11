# Trade-off Comparison Matrix

> Detailed comparison of all 4 approaches across multiple dimensions

## Complete Comparison Table

| Dimension | MCP Server | CLI | Scripts | Skills |
|-----------|-----------|-----|---------|--------|
| **Context Window Consumption** | High (~1500 tokens/call) | Medium (~800 initial + 100/call) | Low (~250-300/script) | Low (~200 skill + 250-300/script) |
| **Context Preservation** | ❌ Lost every call | 😐 Partial | ✅ Excellent | ✅ Excellent |
| **Agent-Invoked** | ✅ Yes (auto) | ❌ No (manual) | ❌ No (manual) | ✅ Yes (auto) |
| **Auto-Discovery** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Customizable** | ❌ No* | ✅ Yes | ✅ Yes | ✅ Yes |
| **Portability** | 😐 Medium (MCP clients) | 😐 Medium (needs install) | ✅ High (just Python) | ❌ Low (Claude Code only) |
| **Composability** | ✅ Yes (MCP Prompts) | ✅ Yes (local prompts) | ✅ Yes (local prompts) | ✅ Yes (SKILL.md) |
| **Simplicity** | ✅ High (for consumers) | 😐 Medium | 😐 Medium | 😐 Medium |
| **Engineering Investment** | Low (use external)<br>Medium (build custom) | Medium | Medium | Low (use external)<br>Medium (build custom) |
| **Feature Set** | Full MCP features** | Whatever you build | Whatever you build | Whatever you build |
| **Code Duplication** | ✅ None | ✅ None | ❌ High (intentional) | ❌ High (intentional) |
| **Shared State** | ❌ None (stateless) | ✅ Possible | ⚠️ Manual (cache dir) | ⚠️ Manual (cache dir) |
| **Human Usability** | ❌ No direct use | ✅ Excellent | 😐 Basic | ❌ No direct use |
| **Team Collaboration** | 😐 Config sharing | 😐 Install required | ✅ Easy (copy files) | ✅ Easy (git) |
| **Dependency Management** | Via project | Via uv/pip | PEP 723 inline | PEP 723 inline |
| **Testing** | Standard pytest | Standard pytest | Isolated testing | Isolated testing |
| **Documentation** | MCP protocol | --help flags | Docstrings | SKILL.md |

*Unless you own/fork the server

**Tools, Resources, Prompts, Elicitation, Completion, Sampling, Logging, Auth, etc.

## Token Consumption Analysis

### Scenario: 3 Operations

**Task**: Get status, search markets, get specific market

| Approach | Load | Op 1 | Op 2 | Op 3 | Total |
|----------|------|------|------|------|-------|
| MCP Server | 1500 | 1500 | 1500 | 1500 | **6000** |
| CLI | 800 | 100 | 100 | 100 | **1100** |
| Scripts | 0 | 250 | 300 | 250 | **800** |
| Skills | 200 | 250 | 300 | 250 | **1000** |

**Savings vs. MCP:**
- CLI: 82% fewer tokens
- Scripts: 87% fewer tokens
- Skills: 83% fewer tokens

## Context Preservation Comparison

### Multi-Turn Conversation Example

**Scenario**: User asks 3 related questions

#### MCP Server
```
User: "Get Kalshi status"
MCP: [Loads 1500 tokens, makes call, LOSES CONTEXT]

User: "Search for AI markets"
MCP: [Loads 1500 tokens again, makes call, LOSES CONTEXT]

User: "Get details on the first one"
MCP: [Doesn't remember "first one", needs clarification]
```

#### CLI
```
User: "Get Kalshi status"
CLI: [Loads 800 tokens once, makes call, PRESERVES HELP TEXT]

User: "Search for AI markets"
CLI: [Uses 100 tokens, already knows CLI, PRESERVES CONTEXT]

User: "Get details on the first one"
CLI: [Can reference previous results if in context]
```

#### Scripts/Skills
```
User: "Get Kalshi status"
Scripts: [Loads 250 tokens, makes call, PRESERVES FULL CONTEXT]

User: "Search for AI markets"
Scripts: [Loads 300 tokens, PRESERVES ALL PREVIOUS]

User: "Get details on the first one"
Scripts: [Easy reference, full conversation context maintained]
```

## Portability Analysis

### Works With...

| Approach | Claude Code | Claude Desktop | ChatGPT | Other LLMs | Human CLI |
|----------|------------|----------------|---------|------------|-----------|
| MCP Server | ✅ Yes | ✅ Yes | ⚠️ If supported | ⚠️ If supported | ❌ No |
| CLI | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| Scripts | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ⚠️ Basic |
| Skills | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |

### Deployment Complexity

| Approach | Setup Steps | Dependencies | Configuration |
|----------|------------|--------------|---------------|
| MCP Server | 2 steps | MCP client + server | .mcp.json |
| CLI | 2-3 steps | uv + packages | None or minimal |
| Scripts | 1 step | uv only | None |
| Skills | 1-2 steps | Claude Code + uv | .claude/skills/ |

## Customization Comparison

### Modification Difficulty

| Change Type | MCP Server | CLI | Scripts | Skills |
|-------------|-----------|-----|---------|--------|
| Add new operation | ❌ Hard* | ✅ Easy | ✅ Easy | ✅ Easy |
| Modify existing | ❌ Hard* | ✅ Easy | ✅ Easy | ✅ Easy |
| Change behavior | ❌ Hard* | ✅ Easy | ✅ Easy | ✅ Easy |
| Add caching | ❌ Hard* | ✅ Medium | ✅ Medium | ✅ Medium |
| Change output format | ❌ Hard* | ✅ Easy | ✅ Easy | ✅ Easy |

*Unless you own the server

### Extension Patterns

**MCP Server:**
- Fork and modify (if open source)
- Request features from maintainer
- Build wrapper/proxy

**CLI:**
- Add command to CLI
- Modify existing command
- Add flags/options

**Scripts:**
- Add new script file
- Modify individual script
- Zero impact on other scripts

**Skills:**
- Add new script
- Update SKILL.md
- Modify activation criteria

## Real-World Use Case Fit

### External Tool Integration

| Scenario | Best Approach | Why |
|----------|--------------|-----|
| GitHub API | MCP Server | Standard, maintained, works everywhere |
| Slack API | MCP Server | External, can't customize deeply |
| AWS API | MCP Server or CLI | Depends on customization needs |
| Internal DB | CLI or Scripts | Full control, custom logic |

### New Tool Development

| Scenario | Best Approach | Why |
|----------|--------------|-----|
| Weather API | CLI | Simple, dual-purpose |
| Research tool | Scripts or Skills | Complex, context-heavy |
| Data pipeline | CLI | Human + AI use |
| Team utility | Skills (if Claude Code) or CLI | Collaboration + discovery |

### Team Collaboration

| Scenario | Best Approach | Why |
|----------|--------------|-----|
| Standardized ops | MCP Server | Everyone uses same way |
| Claude Code team | Skills | Git-based sharing |
| Mixed AI clients | CLI or Scripts | Portable |
| DevOps automation | CLI | Human + AI + scripts |

## Performance Characteristics

### Speed (Latency)

| Approach | Overhead | First Call | Subsequent Calls |
|----------|----------|-----------|------------------|
| MCP Server | High (protocol + subprocess) | Slow | Slow |
| CLI | Medium (subprocess) | Fast | Fast |
| Scripts | Low (direct exec) | Fast | Fast |
| Skills | Low + discovery | Medium (load skill) | Fast |

### Memory Usage

| Approach | AI Context | System Memory |
|----------|-----------|---------------|
| MCP Server | High (full tool defs) | Medium (server + CLI) |
| CLI | Medium (help text) | Low (just CLI) |
| Scripts | Low (one script) | Very Low (script only) |
| Skills | Low (skill + script) | Very Low (script only) |

## Maintenance Burden

### Long-Term Maintenance

| Aspect | MCP Server | CLI | Scripts | Skills |
|--------|-----------|-----|---------|--------|
| Dependency updates | ❌ Hard* | 😐 Medium | ✅ Easy | ✅ Easy |
| Bug fixes | ❌ Hard* | ✅ Easy | ✅ Easy | ✅ Easy |
| Breaking changes | ❌ Hard* | 😐 Medium | ✅ Isolated | ✅ Isolated |
| Documentation | 😐 External | ✅ Self-contained | ✅ Self-contained | ✅ SKILL.md |
| Testing | ❌ Hard* | ✅ Standard | ✅ Easy (isolated) | ✅ Easy (isolated) |

*Unless you own the server

## Decision Matrix

### Choose MCP Server if:

- ✅ External tool (don't control)
- ✅ Need wide compatibility
- ✅ Standardization important
- ✅ Context loss acceptable
- ❌ Don't need customization

### Choose CLI if:

- ✅ Building new tool
- ✅ Humans + AI will use it
- ✅ Need some control
- ✅ Moderate context needs
- ❌ Don't need maximum efficiency

### Choose Scripts if:

- ✅ Context preservation critical
- ✅ Many independent operations
- ✅ Need portability
- ✅ Okay with code duplication
- ❌ Not using Claude Code

### Choose Skills if:

- ✅ Using Claude Code
- ✅ Want auto-discovery
- ✅ Team collaboration via git
- ✅ Context critical
- ❌ Okay with Claude Code lock-in

## Migration Paths

### Upgrade Paths (Increasing Context Efficiency)

```
MCP Server → CLI → Scripts → Skills (if Claude Code)
```

### Downgrade Paths (Increasing Portability)

```
Skills → Scripts → CLI → MCP Server
```

### Lateral Moves

- **MCP ↔ CLI**: Change wrapper vs. direct approach
- **Scripts ↔ Skills**: Add/remove SKILL.md wrapper
- **CLI ↔ Scripts**: Break monolith vs. unify

## Summary Recommendations

### By Project Type

| Project Type | Recommended Approach |
|-------------|---------------------|
| External tool integration | MCP Server (80%), CLI (20%) |
| New API wrapper | CLI (80%), Scripts/Skills (20%) |
| Research tools | Scripts or Skills (depends on AI) |
| Team utilities | Skills (Claude Code) or CLI (mixed) |
| Data pipelines | CLI (human + AI) |
| One-off scripts | Scripts (portable) |

### By Team Size

| Team Size | Recommended Approach |
|-----------|---------------------|
| Solo developer | Whatever fits (Scripts for simplicity) |
| Small team (2-5) | Skills (if Claude Code) or CLI |
| Medium team (6-20) | CLI or MCP Server (standardization) |
| Large org (20+) | MCP Server (governance) |

### By Context Needs

| Context Importance | Recommended Approach |
|-------------------|---------------------|
| Low (simple queries) | MCP Server or CLI |
| Medium (some state) | CLI |
| High (conversations) | Scripts or Skills |
| Critical (complex workflows) | Skills (best) |

---

**Navigation**: [← Back to reference](README.md) | [↑ Docs root](../README.md)
