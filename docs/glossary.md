# Simple Glossary 📖

Confusing terms explained like you're 5!

---

## Core Concepts

### MCP (Model Context Protocol)
**Kid version:** A standard way for AI to use tools (like USB ports for computers)

**What it means:** A protocol that lets AI agents discover and use tools. Works everywhere, but AI forgets context between uses.

**Example:** Like a vending machine - you can use any vending machine the same way, but it doesn't remember you.

---

### Context
**Kid version:** What the AI remembers from your conversation

**What it means:** All the information AI keeps in its "memory" during a conversation. More context = AI remembers more, but costs more.

**Example:** Like your short-term memory - you can only remember so many things at once!

**Why it matters:**
- Too much context = expensive and slow
- Too little context = AI forgets important stuff
- Balance is key!

---

### Progressive Disclosure
**Kid version:** Only show what's needed, when it's needed

**What it means:** Instead of loading everything at once, load only what AI needs for the current task.

**Example:**
- ❌ Bringing entire library to read one book
- ✅ Bringing just the one book you need

**In practice:**
- Bad: AI reads all 10 tools (2,374 lines)
- Good: AI reads 1 tool (200 lines)

---

### Token
**Kid version:** Units of "thinking power" that AI uses (and you pay for!)

**What it means:** AI processes text in chunks called tokens. More tokens = more expensive. 1 token ≈ 4 characters.

**Example:** The word "hamburger" is about 3 tokens.

**Why it matters:** Every word AI reads or writes costs tokens. Efficient tools use fewer tokens!

---

### Caching
**Kid version:** Remembering the answer so you don't have to ask again

**What it means:** Saving results from expensive operations so you can reuse them quickly.

**Example:**
- First time: "What's 123 × 456?" (takes time to calculate)
- Second time: "I remember! It's 56,088!" (instant)

**In this repo:** Search tool caches all markets once, then searches are instant.

---

### Prime Prompt
**Kid version:** Instructions you give AI on how to use something

**What it means:** A document that teaches AI the right way to use your tools before it starts working.

**Example:**
```
"Hey AI, when you want to use this tool:
1. Run --help first
2. Don't read the code
3. Use --json for data"
```

**Why it matters:** Prevents AI from doing inefficient things like reading all your code!

---

### CLI (Command Line Interface)
**Kid version:** A tool you type commands into (like a text-based app)

**What it means:** Programs you run by typing commands in a terminal, like `git status` or `ls`.

**Example:**
```bash
my-tool search "something"  # Run a command
my-tool --help              # Get help
```

**Why useful:** Both humans AND AI can use it!

---

### Self-Contained
**Kid version:** Has everything it needs built-in

**What it means:** A script that doesn't depend on other files - it has all its own code.

**Example:**
- ❌ Needs `shared_utils.py` to work
- ✅ Has everything it needs inside

**Trade-off:** Some code duplication, but AI only reads one file!

---

### Dual Output Mode
**Kid version:** Speaking two languages - one for people, one for robots

**What it means:** Tools that can show results in two ways:
1. Pretty format for humans
2. JSON format for AI/machines

**Example:**
```bash
tool status         # Pretty table for humans
tool status --json  # Clean data for AI
```

---

## Technical Terms

### API (Application Programming Interface)
**Kid version:** A way for programs to talk to each other

**What it means:** Rules for how software can request and exchange data.

**Example:** Kalshi API lets you get market data by sending requests.

---

### JSON
**Kid version:** A way to organize data that machines understand perfectly

**What it means:** A standard format for structured data. Looks like this:
```json
{
  "name": "Alice",
  "age": 10,
  "likes": ["ice cream", "robots"]
}
```

**Why AI loves it:** Clear structure, easy to parse, no ambiguity!

---

### Subprocess
**Kid version:** Starting one program from inside another program

**What it means:** When a program runs another program and waits for results.

**Example:** MCP Server runs CLI commands using subprocess - it's like a wrapper!

---

### TTL (Time To Live)
**Kid version:** How long before something expires

**What it means:** How long cached data stays fresh before you fetch new data.

**Example:** "Cache TTL = 6 hours" means cached data expires after 6 hours.

---

### Dependencies
**Kid version:** Other things a program needs to work

**What it means:** External libraries or packages your code relies on.

**Example:**
```python
# This script needs these:
dependencies = ["httpx", "click"]
```

---

## Approaches in This Repo

### MCP Server
**Kid version:** The standard, works-everywhere way

**What it is:** A server that exposes tools using MCP protocol. AI can discover and use them automatically.

**Trade-off:** Universal compatibility, but context loss.

---

### CLI (in this context)
**Kid version:** The flexible, works-for-everyone way

**What it is:** Command-line tools that both humans and AI can use directly.

**Trade-off:** Requires telling AI about it, but versatile and efficient.

---

### File System Scripts
**Kid version:** Individual, independent tools

**What it is:** Separate Python scripts, each doing one job, living in folders.

**Trade-off:** Amazing context efficiency, but AI needs to know they exist.

---

### Skills (Claude Code)
**Kid version:** Smart tools that Claude finds automatically

**What it is:** Like File System Scripts, but Claude Code discovers them automatically via descriptions.

**Trade-off:** Best for Claude Code users, but not portable to other AIs.

---

## Best Practice Terms

### DRY (Don't Repeat Yourself)
**Kid version:** Traditional rule: never copy code

**What it means:** Share code instead of duplicating it.

**This repo's twist:** Sometimes repeating code is GOOD for AI tools! Context efficiency matters more than code reuse.

---

### Single Source of Truth
**Kid version:** One place where the "real" work happens

**What it means:** Don't implement the same logic twice - have one authoritative version.

**Example in this repo:** CLI does the real work, MCP just calls the CLI.

---

### Portability
**Kid version:** Works in many places

**What it means:** Can be used across different systems, platforms, or AI agents.

**Example:**
- ✅ Scripts = portable (any AI can use)
- ❌ Skills = not portable (only Claude Code)

---

## Context-Related Terms

### Context Loss
**Kid version:** AI forgetting what you talked about

**What it means:** When AI can't access previous conversation info.

**Where it happens:** MCP Servers cause context loss on every tool call.

---

### Context Preservation
**Kid version:** AI remembering your conversation

**What it means:** Keeping conversation history so AI can reference earlier information.

**Best for this:** Scripts and Skills.

---

### Context Window
**Kid version:** How much AI can remember at once

**What it means:** The maximum amount of text/tokens AI can process in one go.

**Example:** Like your brain can only juggle 7 things at once - AI has limits too!

---

## Quick Reference

| Term | ELI5 | Why It Matters |
|------|------|----------------|
| **Context** | AI's memory | Costs money |
| **Tokens** | Thinking units | You pay for them |
| **Caching** | Remembering answers | Speed + savings |
| **Progressive Disclosure** | Show only what's needed | Efficiency |
| **Prime Prompt** | Instructions for AI | Prevents waste |
| **MCP** | Standard tool system | Works everywhere |
| **CLI** | Text commands | Humans + AI use it |

---

## Still Confused?

That's okay! The important concepts are:

1. **Context** = What AI remembers (costs money)
2. **MCP** = Standard way (loses context)
3. **Alternatives** = Keep more context
4. **Trade-offs** = Choose what fits your needs

Everything else is details! 😊
