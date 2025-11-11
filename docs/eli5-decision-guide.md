# When to Use What? (Simple Decision Guide)

## The Fast Answer

Answer these 3 questions:

### Question 1: Did YOU make the tool?

- **NO** → Use **MCP Server** 🎁 (just use it as-is!)
- **YES** → Go to Question 2

### Question 2: Does AI memory/context matter A LOT?

- **NO** → Use **CLI** 🛠️ (simple and good!)
- **YES** → Go to Question 3

### Question 3: Do you use Claude Code?

- **YES** → Use **Skills** 🎯 (best for Claude Code!)
- **NO** → Use **Scripts** 📁 (portable to any AI!)

---

## Real-World Examples

### Example 1: "I want to use GitHub with my AI"

- Did you make GitHub? → **NO**
- **Answer: Use MCP Server** 🎁
- Why: Someone else built it, just use the standard way!

### Example 2: "I'm building a weather checker tool"

- Did you make it? → **YES** (you're building it)
- Does context matter a lot? → **NO** (weather is simple, one-off queries)
- **Answer: Use CLI** 🛠️
- Why: You control it, and it's simple enough!

### Example 3: "I'm building a complex research tool with many steps"

- Did you make it? → **YES**
- Does context matter a lot? → **YES** (multi-turn conversations)
- Do you use Claude Code? → **YES**
- **Answer: Use Skills** 🎯
- Why: Best context preservation for Claude Code!

### Example 4: "I'm building tools for a team that uses different AIs"

- Did you make it? → **YES**
- Does context matter a lot? → **YES**
- Do you use Claude Code? → **NO** (team uses different AIs)
- **Answer: Use Scripts** 📁
- Why: Portable and efficient!

---

## The Author's Recommendations

### For EXISTING Tools (tools others built):

```
80% → MCP Server 🎁
15% → CLI 🛠️ (if you need to modify it)
5%  → Scripts/Skills 📁🎯 (if context is critical)
```

### For NEW Tools (you're building):

```
80% → CLI 🛠️
10% → MCP Server 🎁 (if managing many agents)
10% → Scripts/Skills 📁🎯 (if context is critical)
```

---

## Special Situations

### "I'm not sure yet..."
→ Start with **CLI** 🛠️
→ You can always convert it later!

### "I need to share with many people"
→ **MCP Server** 🎁 or **Scripts** 📁
→ Both are easy to share!

### "I have LOTS of tools (like 20+)"
→ **Scripts** 📁 or **Skills** 🎯
→ Progressive disclosure = AI only loads what it needs!

### "AI keeps running out of memory/context"
→ **Scripts** 📁 or **Skills** 🎯
→ These use way less AI "thinking power"!

### "I want AI to find tools automatically"
→ **Skills** 🎯 (if Claude Code)
→ **MCP Server** 🎁 (if other AIs)

---

## The Golden Rule

**When in doubt, keep it simple!**

- External tool? → MCP 🎁
- Building new? → CLI 🛠️
- Context problems? → Scripts/Skills 📁🎯

Don't overthink it! You can always change later.
