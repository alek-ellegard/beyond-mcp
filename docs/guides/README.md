# Guides: Practical Guidance for Building AI Tools

> **Progressive Disclosure**: This is a category index. Read this for an overview, then navigate to specific guides as needed.

## Overview

This category provides practical, actionable guidance for building AI tools. Whether you're choosing an approach, implementing best practices, or learning from examples - these guides will help.

## Guides in This Category

### [decision-guide.md](decision-guide.md) ⭐
**Choose the right approach for your use case**

Quick decision tree to help you select between MCP Server, CLI, Scripts, or Skills based on your specific needs.

**Read this if:**
- You're starting a new project
- You're unsure which approach to use
- You want to understand trade-offs quickly

**Time**: 3 min read

---

### [best-practices.md](best-practices.md) ⭐⭐
**Build better AI tools with proven patterns**

10 core principles for building AI tools that are context-efficient, discoverable, and maintainable. Learn patterns like progressive disclosure, prime prompts, and smart caching.

**Read this if:**
- You're implementing any of the 4 approaches
- You want to optimize for context preservation
- You're building tools at scale

**Time**: 8 min read

---

### [examples-walkthrough.md](examples-walkthrough.md) ⭐⭐⭐
**Real code examples from this repository**

Detailed walkthrough of actual implementations in this repo. See how the patterns and best practices are applied in production code.

**Read this if:**
- You learn best from code examples
- You want to see patterns in practice
- You're implementing something similar

**Time**: 12 min read

## Quick Decision Framework

### I need to...

**Choose an approach** → [decision-guide.md](decision-guide.md)

**Optimize my implementation** → [best-practices.md](best-practices.md)

**See real code** → [examples-walkthrough.md](examples-walkthrough.md)

**Understand approaches deeply** → [../approaches/README.md](../approaches/README.md)

## Key Concepts Covered

### Decision Guide
- 3-question decision tree
- Real-world examples
- Author's recommendations
- Special situations
- The golden rule

### Best Practices
1. Progressive disclosure
2. Prime prompts
3. Dual output modes
4. Smart caching
5. Self-contained scripts
6. Strategic code duplication
7. Single source of truth
8. Help flags
9. Local docs for AI
10. Context-first thinking

### Examples Walkthrough
- MCP Server wrapper pattern
- CLI command structure
- Script independence pattern
- Skill manifest design
- Cache implementation
- Path resolution
- Error handling

## Learning Path

### For Beginners

1. **Start**: [decision-guide.md](decision-guide.md) - Choose your approach
2. **Then**: [best-practices.md](best-practices.md) - Learn the patterns
3. **Finally**: [examples-walkthrough.md](examples-walkthrough.md) - See it in action

### For Experienced Developers

1. **Start**: [best-practices.md](best-practices.md) - Core principles
2. **Then**: [examples-walkthrough.md](examples-walkthrough.md) - Implementation details
3. **Reference**: [decision-guide.md](decision-guide.md) - Quick lookups

### For Specific Tasks

**Choosing between approaches:**
→ [decision-guide.md](decision-guide.md) only

**Optimizing existing implementation:**
→ [best-practices.md](best-practices.md) only

**Understanding the code:**
→ [examples-walkthrough.md](examples-walkthrough.md) only

## Related Documentation

**For conceptual understanding:**
→ [../overview/README.md](../overview/README.md)

**For approach-specific details:**
→ [../approaches/README.md](../approaches/README.md)

**For quick reference:**
→ [../reference/cheat-sheet.md](../reference/cheat-sheet.md)

**For deep dives:**
→ [../deep-dives/README.md](../deep-dives/README.md)

## Common Questions

### "Which approach should I use?"
→ Start with [decision-guide.md](decision-guide.md)

### "How do I optimize for context?"
→ Read [best-practices.md](best-practices.md) - especially "Progressive Disclosure" and "Context is King"

### "How is this actually implemented?"
→ Check [examples-walkthrough.md](examples-walkthrough.md)

### "What's the single most important thing?"
→ **Context preservation**. Read "Context is King" in [best-practices.md](best-practices.md)

---

**Navigation**: [← Back to docs root](../README.md) | [Next: Reference →](../reference/README.md)
