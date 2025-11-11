# Context Preservation: Theory and Practice

> Why context matters, how approaches differ, and strategies for optimization

## What is Context?

In the context of AI agents, "context" refers to the information an LLM maintains across interactions:

- **Conversation history**: Previous messages and responses
- **Tool definitions**: Available operations and their parameters
- **Execution results**: Outputs from previous tool calls
- **Working memory**: Intermediate state and decisions

**Context is memory** - and memory is critical for effective AI assistance.

## Why Context Preservation Matters

### Example: Multi-Turn Workflow

**With Context Preservation:**
```
User: "Get the Kalshi exchange status"
AI: [Checks status, remembers result] "Exchange is active, trading enabled"

User: "Search for markets about AI"
AI: [Searches, remembers both status and search]
    "Found 15 AI-related markets. The exchange is active."

User: "Get details on the first one"
AI: [Remembers "first one" = first search result]
    "The first market is: [details]"
```

**Without Context Preservation (MCP):**
```
User: "Get the Kalshi exchange status"
AI: [Checks status] "Exchange is active, trading enabled"
    [CONTEXT LOST]

User: "Search for markets about AI"
AI: [Searches] "Found 15 AI-related markets"
    [CONTEXT LOST - doesn't remember status check]

User: "Get details on the first one"
AI: [Confused] "Which market? Can you provide the ticker?"
    [CONTEXT LOST - doesn't remember search results]
```

## Context Loss in MCP Protocol

### How MCP Works

```
1. LLM sends tool request to MCP server
2. Server executes tool
3. Server returns result
4. LLM receives result
5. LLM continues... but without previous tool context
```

### Why Context is Lost

MCP protocol is **stateless by design**:

- Each tool call is independent
- Server doesn't maintain conversation state
- Client (LLM) doesn't preserve tool execution context
- Tool definitions are reloaded on each call

**Trade-off**: Standardization vs. Context

MCP prioritizes **portability and standardization** over **context preservation**.

### Token Cost

Every MCP tool call requires:

```
Current context:
  - Full conversation history: ~1000-2000 tokens
  - All tool definitions: ~1500 tokens
  - Request/response: ~100-500 tokens

Total per call: ~2600-4000 tokens
```

With 10 tool calls: **26,000-40,000 tokens** consumed just for tool overhead.

## Context Preservation Strategies

### Strategy 1: Reduce Initial Load (CLI)

**Pattern**: Load tool help once, reuse across calls

```
Initial load:
  - Tool help text: ~800 tokens
  - Conversation: ~500 tokens
  Total: ~1300 tokens

Subsequent calls:
  - Just command output: ~100-200 tokens

3 calls total: 1300 + 100 + 100 + 100 = ~1600 tokens
```

**Savings**: 60-75% vs. MCP

**Limitation**: Still loads full help text initially

---

### Strategy 2: Progressive Disclosure (Scripts)

**Pattern**: Load only what's needed, when needed

```
Call 1 (status):
  - Read status.py: ~250 tokens
  - Execute and get result: ~50 tokens
  Total: ~300 tokens

Call 2 (search):
  - Read search.py: ~300 tokens
  - Execute and get result: ~100 tokens
  Total: ~400 tokens

Call 3 (market):
  - Read market.py: ~250 tokens
  - Execute and get result: ~75 tokens
  Total: ~325 tokens

3 calls total: 300 + 400 + 325 = ~1025 tokens
```

**Savings**: 75-85% vs. MCP, 35-40% vs. CLI

**Key insight**: Each script is independent, no cumulative loading

---

### Strategy 3: Auto-Discovery + Progressive Disclosure (Skills)

**Pattern**: Automatic activation with minimal metadata load

```
Initial (before activation):
  - Skill metadata: ~50 tokens (just name + description)

On activation:
  - SKILL.md: ~200 tokens
  - Script 1: ~250 tokens
  Total: ~450 tokens

Subsequent calls:
  - Script 2: ~300 tokens
  - Script 3: ~250 tokens

3 calls total: 450 + 300 + 250 = ~1000 tokens
```

**Savings**: Similar to Scripts, with auto-discovery bonus

**Benefit**: No manual prime prompt needed

## Token Economics

### Cost Per Operation by Approach

| Approach | Initial | Op 1 | Op 2 | Op 3 | Total | % of MCP |
|----------|---------|------|------|------|-------|----------|
| MCP | 1500 | 1500 | 1500 | 1500 | 6000 | 100% |
| CLI | 800 | 100 | 100 | 100 | 1100 | 18% |
| Scripts | 0 | 250 | 300 | 250 | 800 | 13% |
| Skills | 200 | 250 | 300 | 250 | 1000 | 17% |

### At Scale (30 operations)

| Approach | Token Cost | Cost at $0.003/1K* |
|----------|-----------|-------------------|
| MCP | 45,000 | $0.135 |
| CLI | 3,500 | $0.011 |
| Scripts | 7,500 | $0.023 |
| Skills | 7,700 | $0.023 |

*Assuming Claude Sonnet input token pricing

**Key insight**: At scale, context preservation = significant cost savings

## Progressive Disclosure: Deep Dive

### The Pattern

```
Metadata Layer (Always Loaded)
    ↓
Instruction Layer (Loaded When Needed)
    ↓
Resource Layer (Loaded On Demand)
```

### Implementation

**Layer 1: Metadata** (~50-100 tokens)
```markdown
# Tool Name
Brief description (1-2 sentences)
Activation keywords: foo, bar, baz
```

**Layer 2: Instructions** (~200-300 tokens)
```markdown
## Available Operations
- operation1 - Brief description
- operation2 - Brief description

## Usage
Basic examples
```

**Layer 3: Resources** (~200-300 tokens each)
```python
# Individual script files
# Loaded only when specific operation needed
```

### Why This Works

1. **Lazy loading**: Don't load what you don't need
2. **Granular access**: Load specific operations, not entire tool
3. **Memory efficiency**: Each layer is independently small
4. **Scalability**: Add operations without loading cost

## Context Window Optimization

### Understanding Context Windows

| Model | Context Window | Typical Usable |
|-------|---------------|----------------|
| Claude Sonnet | 200K tokens | ~150K tokens |
| GPT-4 | 128K tokens | ~100K tokens |
| Claude Haiku | 200K tokens | ~150K tokens |

### Context Consumption Patterns

**MCP Pattern** (fills window quickly):
```
Conversation: 2K
Tool defs: 1.5K per call × 20 calls = 30K
Results: 0.5K × 20 = 10K
Total: 42K tokens (28% of window after 20 ops)
```

**Scripts Pattern** (fills window slowly):
```
Conversation: 2K
Scripts: 0.25K × 20 = 5K
Results: 0.5K × 20 = 10K
Total: 17K tokens (11% of window after 20 ops)
```

**Advantage**: Scripts allow 2.5x more operations before context pressure

### Context Pressure Effects

When context window fills:

1. **Truncation**: Oldest messages dropped
2. **Summarization**: Context compressed (lossy)
3. **Errors**: "Context too long" failures
4. **Performance**: Slower inference on large contexts

**Prevention**: Use context-efficient approaches (Scripts/Skills)

## Multi-Turn Conversation Patterns

### Pattern 1: Sequential Operations

**Example**: Research workflow
```
1. Search for topics → 300 tokens
2. Get details on 5 results → 250 × 5 = 1250 tokens
3. Compare options → 400 tokens
4. Make decision → 200 tokens

Total: 2150 tokens (Scripts/Skills)
vs. 10,500 tokens (MCP)
```

### Pattern 2: Iterative Refinement

**Example**: Data exploration
```
1. Query initial data → 300 tokens
2. "Show me just the top 10" → 250 tokens
3. "Filter by category" → 250 tokens
4. "Sort by date" → 250 tokens

Total: 1050 tokens (Scripts/Skills)
vs. 6000 tokens (MCP)
```

### Pattern 3: Branching Workflows

**Example**: Conditional logic
```
1. Check status → 250 tokens
2. If active:
   → Search markets → 300 tokens
   → Get details → 250 tokens
3. If inactive:
   → Check again later → 250 tokens

Average: ~600-800 tokens (Scripts/Skills)
vs. 4500-6000 tokens (MCP)
```

## Memory vs. Portability Trade-off

### The Fundamental Tension

```
Portability ←→ Context Preservation

MCP          CLI          Scripts          Skills
(Portable)   (Balanced)   (Balanced)       (Efficient)
(Poor ctx)   (Med ctx)    (Good ctx)       (Good ctx)
```

### When Portability Wins

Choose MCP when:
- Multiple AI clients (ChatGPT, Claude, local LLMs)
- External tools you don't control
- Standardization > efficiency
- Simple, stateless operations

### When Context Wins

Choose Scripts/Skills when:
- Single AI client (especially Claude Code)
- Context-sensitive workflows
- High operation frequency
- Multi-turn conversations

### Hybrid Approach

**Pattern**: Use both
- MCP for external tools (can't change)
- Scripts/Skills for custom tools (full control)

```
External tools:
  - GitHub → MCP
  - Slack → MCP

Custom tools:
  - Internal API → Scripts
  - Data analysis → Skills
```

## Best Practices

### 1. Minimize Initial Load

**Bad**:
```markdown
# Load all 50 commands upfront
kalshi help:
  - command1 (details)
  - command2 (details)
  - ...
  - command50 (details)
```

**Good**:
```markdown
# Load index, then specific commands
kalshi help:
  - Use `kalshi <command> --help` for details

# Later, when needed:
kalshi search --help:
  - Specific details for search command
```

### 2. Keep Scripts Focused

**Bad**: One script does everything (~1000 lines)

**Good**: Each script does one thing (~200-300 lines)

```
❌ kalshi.py (1000 lines, does everything)

✅ status.py (200 lines)
✅ search.py (300 lines)
✅ markets.py (250 lines)
```

### 3. Use Caching Strategically

**Pattern**: Cache expensive operations
- First run: Slow (build cache)
- Subsequent: Fast (use cache)
- TTL: Refresh periodically

**Benefit**: Reduce repeated API calls without context overhead

### 4. Embed Dependencies

**Pattern**: Self-contained scripts with inline metadata

```python
# /// script
# dependencies = ["httpx"]
# ///
```

**Benefit**: AI reads one file, not import chain

### 5. Design for Context

**Checklist**:
- [ ] Can AI load just what it needs?
- [ ] Are operations independent?
- [ ] Is state clearly managed?
- [ ] Are dependencies explicit?
- [ ] Does each tool have clear scope?

## Measuring Context Efficiency

### Metrics to Track

1. **Tokens per operation**
   - Measure: Total tokens / number of operations
   - Target: < 500 tokens/op

2. **Context window usage**
   - Measure: % of window consumed after N operations
   - Target: < 50% after 20 operations

3. **Reuse ratio**
   - Measure: Reused context / total context
   - Target: > 70% reuse

4. **Load overhead**
   - Measure: Initial load tokens / operational tokens
   - Target: < 20% overhead

### Example Analysis

**MCP Server**:
```
Operations: 10
Total tokens: 15,000
Per operation: 1,500
Reuse: 0% (loads each time)
Overhead: 100% (all overhead)
```

**Scripts**:
```
Operations: 10
Total tokens: 2,500
Per operation: 250
Reuse: 80% (conversation reused)
Overhead: 10% (minimal)
```

## Common Pitfalls

### Pitfall 1: Over-Optimization

**Problem**: Splitting scripts too granularly

**Solution**: Keep scripts at operation level, not function level

**Right size**: 200-300 lines per script

### Pitfall 2: Shared State Assumptions

**Problem**: Scripts assume context from other scripts

**Solution**: Each script is fully independent

### Pitfall 3: Ignoring Human Use

**Problem**: Optimizing only for AI

**Solution**: Consider dual-purpose (CLI approach) or documentation

### Pitfall 4: Premature Abstraction

**Problem**: Creating shared libraries "for reuse"

**Solution**: Embed common code, optimize for AI context, not code DRY

## Future Considerations

### Long Context Windows (1M+ tokens)

**Trend**: Models with million-token contexts

**Impact**: Context preservation less critical

**Reality**: Cost and latency still favor efficient approaches

### Semantic Caching

**Concept**: LLM providers cache repeated contexts

**Impact**: Reduces some MCP overhead

**Reality**: Still more efficient to not load unnecessarily

### Agentic Memory Systems

**Concept**: External memory for agents

**Impact**: Could help MCP maintain state

**Reality**: Not yet standard; context efficiency still wins

## Related Documentation

- [Standalone Scripts Deep Dive](standalone-scripts.md) - Implementation details
- [Best Practices](../guides/best-practices.md) - Practical guidance
- [Trade-off Comparison](../reference/trade-off-comparison.md) - Detailed metrics

---

**Navigation**: [← Back to deep dives](README.md) | [Next: Search Caching →](search-caching.md)
