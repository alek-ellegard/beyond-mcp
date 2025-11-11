# Best Practices (Explained Simply)

These are the smart tricks this repo teaches us!

---

## 1. Progressive Disclosure 📚

**Kid version:**
Instead of giving AI a whole encyclopedia, give it just the one page it needs!

**How it works:**
- BAD: AI reads all 10 tools (2,374 lines of code) 😰
- GOOD: AI reads only 1 tool (200 lines of code) 😊

**Why it matters:**
- Saves AI "thinking power" (tokens = money!)
- AI stays focused
- Conversations work better

**How to do it:**
- Use separate files for each tool
- Let AI read only what it needs
- Don't make AI read everything upfront

---

## 2. Prime Prompts 🎯

**Kid version:**
Give AI a map so it doesn't get lost!

**How it works:**
Create a special instruction file that tells AI:
- "Use `--help` to learn about tools"
- "DON'T read all the code!"
- "Here's how to use this tool..."

**Why it matters:**
- AI learns the right way to use things
- Prevents AI from wasting time
- Like giving someone directions instead of making them explore

**Example:**
```
❌ AI reads 500 lines of code to understand a tool
✅ AI runs `tool --help` and reads 20 lines
```

---

## 3. Dual Output Modes 🎭

**Kid version:**
Make tools speak two languages - one for humans, one for robots!

**How it works:**
```bash
my-tool status           # Pretty output for humans 👨
my-tool status --json    # Data for AI 🤖
```

**Why it matters:**
- Humans get pretty, readable output
- AI gets clean, structured data
- One tool works for everyone!

---

## 4. Smart Caching 💾

**Kid version:**
Remember the answer instead of asking again and again!

**How it works:**
- First time: Takes 2-5 minutes (downloads everything)
- After that: Instant! (uses saved copy)
- Refreshes automatically every 6 hours

**Why it matters:**
- Super fast after first use
- Saves API calls
- Works even if API is slow

**Real example from this repo:**
The search tool would be super slow without caching. With caching? Instant!

---

## 5. Self-Contained Scripts 🎒

**Kid version:**
Each tool carries its own backpack!

**How it works:**
Each script file includes:
- Its own code
- Its own list of what it needs
- Everything to work alone

**Why it matters:**
- No dependencies on other files
- Easy to share (just copy one file!)
- AI only loads what it needs

**Code example:**
```python
# /// script
# dependencies = [
#     "httpx",
#     "click",
# ]
# ///
```

---

## 6. Don't Repeat Yourself... Or DO! 🔄

**Kid version:**
Sometimes copying is GOOD, not bad!

**Traditional advice:**
"Never repeat code!" (DRY - Don't Repeat Yourself)

**This repo's insight:**
"Sometimes repeating code helps AI!"

**Why?**
- Each script is independent
- AI only reads one script (not all shared code)
- Copying 50 lines is okay if it saves reading 1,000 lines!

**When to repeat:**
- When it makes tools independent
- When it reduces AI context
- When it makes sharing easier

**When NOT to repeat:**
- Within the same file
- When it creates maintenance nightmares
- When the shared code is really complex

---

## 7. Single Source of Truth 📍

**Kid version:**
Don't build the same thing twice!

**How it works in this repo:**
- CLI does the real work (talks to API)
- MCP Server just calls the CLI
- One place to fix bugs!

**Why it matters:**
- Fix a bug once, everywhere is fixed
- Less code to maintain
- Tested in one place = trusted everywhere

---

## 8. Help Flags Are Your Friend 🚩

**Kid version:**
Every tool should explain itself!

**How it works:**
```bash
my-tool --help           # Shows how to use it
my-tool search --help    # Shows how to use 'search'
```

**Why it matters:**
- AI can learn by asking
- No need to read code
- Self-documenting

**This is huge for AI!**
- AI runs `--help` (reads 20 lines)
- Instead of reading code (500 lines)
- 25x more efficient!

---

## 9. Local Docs for AI 📖

**Kid version:**
Keep a cheat sheet nearby!

**How it works:**
- Download API docs once
- Save as markdown files
- AI reads local copy (fast!)

**Why it matters:**
- No internet needed after first download
- Faster than web fetches
- Version controlled (know what AI is reading)

**In this repo:**
`ai_docs/` folder has saved documentation

---

## 10. Context is King 👑

**Kid version:**
The most important thing is helping AI remember!

**The Big Idea:**
Every decision should ask:
- "Will this help AI remember our conversation?"
- "Will this use less AI thinking power?"
- "Will this make AI more effective?"

**Examples:**
- ✅ Separate scripts = less context per tool
- ✅ Prime prompts = AI knows what to do
- ✅ Caching = AI gets fast results
- ❌ Giant monolithic tool = AI reads everything
- ❌ No documentation = AI reads all code

---

## The Core Philosophy

**Traditional software engineering:**
"Build one perfect, reusable, efficient system"

**AI tooling engineering:**
"Build tools that AI can understand and use efficiently"

**These are different goals!**

Sometimes the "right" way for traditional code is the "wrong" way for AI tools.

**Example:**
- Traditional: Share code, avoid duplication
- AI tools: Sometimes duplicate code to reduce context

---

## Quick Reference

When building AI tools, ask yourself:

1. **Context:** How much does AI need to read?
2. **Memory:** Will AI remember our conversation?
3. **Discovery:** How does AI know this exists?
4. **Documentation:** Can AI learn without reading code?
5. **Independence:** Can tools work alone?
6. **Output:** Does it work for humans AND AI?
7. **Caching:** Are we saving expensive operations?

If you follow these principles, you'll build great AI tools! 🎉
