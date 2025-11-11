# Quick Reference Cheat Sheet 📋

One-page reference for choosing and building AI tools.

---

## Decision Tree (30 seconds)

```
Did YOU build the tool?
├─ NO → MCP Server 🎁
└─ YES → Does context matter A LOT?
    ├─ NO → CLI 🛠️
    └─ YES → Using Claude Code?
        ├─ YES → Skills 🎯
        └─ NO → Scripts 📁
```

---

## Comparison Table

| Feature | MCP 🎁 | CLI 🛠️ | Scripts 📁 | Skills 🎯 |
|---------|--------|---------|-----------|----------|
| **AI Memory** | ❌ Poor | 😐 Okay | ✅ Good | ✅✅ Best |
| **Works Everywhere** | ✅✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| **Auto-Discovery** | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Easy to Share** | ✅ Yes | 😐 Medium | ✅ Yes | ✅ Yes |
| **Setup Difficulty** | 😐 Medium | 🟢 Easy | 🟢 Easy | 🟢 Easy |
| **Context Usage** | ❌ High | 😐 Medium | ✅ Low | ✅✅ Lowest |
| **For Humans Too** | ❌ No | ✅✅ Yes | 😐 Kinda | 😐 Kinda |

---

## When to Use What

### Use MCP Server 🎁 when:
- ✅ Tool built by someone else
- ✅ Need universal compatibility
- ✅ Managing multiple agents at scale
- ✅ Standardization matters

### Use CLI 🛠️ when:
- ✅ Building a new tool
- ✅ Both humans and AI will use it
- ✅ Want control and flexibility
- ✅ Default choice for most projects

### Use Scripts 📁 when:
- ✅ Context efficiency critical
- ✅ Need portability (any AI)
- ✅ Have many tools (10+)
- ✅ Want independent tools

### Use Skills 🎯 when:
- ✅ Using Claude Code specifically
- ✅ Want auto-discovery
- ✅ Context efficiency critical
- ✅ Team collaboration via git

---

## Best Practices Checklist

Building an AI tool? Check these:

- [ ] **Progressive Disclosure**: Does AI only load what it needs?
- [ ] **Prime Prompt**: Did you create instructions for AI?
- [ ] **Help Flags**: Does `--help` explain usage?
- [ ] **Dual Output**: Human-readable AND JSON modes?
- [ ] **Smart Caching**: Are expensive operations cached?
- [ ] **Self-Contained**: Can each part work independently?
- [ ] **Local Docs**: Is documentation easily accessible?
- [ ] **Context-First**: Did you optimize for AI memory?

---

## Common Mistakes

### ❌ DON'T:
- Use MCP for everything (context loss!)
- Make AI read all code (use `--help` instead)
- Build giant monolithic tools
- Forget about caching
- Ignore context consumption

### ✅ DO:
- Choose based on needs
- Use progressive disclosure
- Cache expensive operations
- Provide both human & JSON output
- Think about AI memory

---

## Code Snippets

### Dual Output Mode
```python
@click.option('--json', is_flag=True)
def my_command(json):
    data = get_data()
    if json:
        print(json.dumps(data))  # For AI
    else:
        print_pretty(data)        # For humans
```

### Self-Contained Script
```python
# /// script
# dependencies = [
#     "httpx",
#     "click",
# ]
# ///

# Rest of your script...
```

### Smart Caching
```python
CACHE_TTL = 6 * 3600  # 6 hours
cache_path = Path(".cache/data.pkl")

if cache_path.exists() and not is_expired(cache_path):
    return load_cache(cache_path)
else:
    data = expensive_operation()
    save_cache(cache_path, data)
    return data
```

### Prime Prompt Pattern
```markdown
# Prime Prompt for AI

When using these tools:
1. Run `tool --help` to see available commands
2. DON'T read the implementation code
3. Use `--json` flag for machine-readable output
4. Available commands: list, search, get, update
```

---

## Quick Stats

**Author's Recommendations:**

For external tools:
- 80% → MCP
- 15% → CLI
- 5% → Scripts/Skills

For new tools:
- 80% → CLI
- 10% → MCP
- 10% → Scripts/Skills

---

## The One Thing to Remember

**Context is king! 👑**

Every decision should consider:
*"How does this affect AI's ability to remember and understand?"*

---

## Resources

- [Full Overview](eli5-overview.md)
- [Detailed Comparison](eli5-four-approaches.md)
- [Decision Guide](eli5-decision-guide.md)
- [Best Practices](eli5-best-practices.md)

---

**Still unsure? Start with CLI 🛠️**
It's the safe, flexible default choice!
