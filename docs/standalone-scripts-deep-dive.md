# Standalone Scripts Deep Dive 🎯

The `uv` standalone script pattern with inline dependencies - explained simply.

---

## The Basic Pattern

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "httpx",
#     "click",
# ]
# ///

import httpx
import click

# Your entire script here...
# Everything it needs is in THIS file
```

**Run it:** `uv run my_script.py`

That's it! No setup, no installation, just run.

---

## Why It's Powerful

### Traditional Approach (BAD for AI)

```
project/
├── requirements.txt          # Dependencies here
├── src/
│   ├── __init__.py
│   ├── client.py            # HTTP client here
│   ├── formatting.py        # Formatters here
│   └── utils.py             # Utils here
└── scripts/
    └── status.py            # Script here
```

**AI needs to read:** 5+ files (maybe 800+ lines of code)

**To understand:** One simple status check

**Context used:** HIGH 😰

---

### Standalone Script Approach (GOOD for AI)

```
scripts/
└── status.py                # Everything in ONE file
```

**AI needs to read:** 1 file (157 lines of code)

**To understand:** One simple status check

**Context used:** LOW 😊

---

## Real Example from beyond-mcp

### status.py - Complete and Self-Contained

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "httpx",
#     "click",
# ]
# ///

# 1. Has its own HTTP client
class KalshiClient:
    """Minimal HTTP client - just what we need"""
    def __init__(self):
        self.client = httpx.Client(...)

    def get_exchange_status(self):
        # Makes API call
        ...

# 2. Has its own formatters
def format_status(data):
    """Format for human reading"""
    ...

# 3. Has its own CLI
@click.command()
@click.option('--json', is_flag=True)
def main(output_json: bool):
    """Complete CLI interface"""
    ...

# 4. Runs standalone
if __name__ == "__main__":
    main()
```

**Total lines:** 157

**Dependencies:** Declared inline

**Can run:** Anywhere with `uv`

---

## The Trade-off

### What You Give Up

- ❌ Some code duplication (HTTP client in each script)
- ❌ DRY principle (Don't Repeat Yourself)
- ❌ Shared utilities

### What You Gain

- ✅ **Context efficiency**: AI only reads what it needs
- ✅ **Independence**: Each script works alone
- ✅ **Portability**: Copy one file, works anywhere
- ✅ **Progressive disclosure**: Load only what you need
- ✅ **Zero setup**: No installation needed
- ✅ **Self-documenting**: Everything in one place

---

## The Numbers

From the beyond-mcp repo:

### Traditional CLI Approach
- **Total code:** ~2,374 lines across multiple files
- **AI must read:** Most of it to understand one command
- **Context tokens:** HIGH

### Standalone Scripts Approach
- **Total code:** ~2,400 lines (similar!)
- **AI must read:** 200-300 lines for one command
- **Context tokens:** ~85% LESS

**Same functionality, 85% less context! 🎉**

---

## How uv Makes It Work

### What happens when you run `uv run status.py`:

1. **Reads the script**: Sees the `# /// script` block
2. **Parses dependencies**: `httpx`, `click`
3. **Creates ephemeral env**: Temporary virtual environment
4. **Installs dependencies**: Only if not cached
5. **Runs the script**: With all deps available
6. **Cleans up**: Env is temporary (or cached for next time)

**Result:** It "just works" - no `pip install`, no setup!

---

## Code Duplication is GOOD?! 🤯

### Traditional Software Engineering

**Rule:** "Don't Repeat Yourself (DRY)"

**Reason:** Easier to maintain, fix bugs in one place

**Makes sense for:** Traditional applications

---

### AI Tool Engineering

**New Rule:** "Context Efficiency > DRY"

**Reason:** AI reading 1,000 lines costs more than maintaining duplicate code

**Makes sense for:** AI-facing tools

---

### The Calculation

**Scenario:** You have an HTTP client (50 lines of code)

**Option 1: Shared client (DRY)**
- ✅ Maintain in one place
- ❌ AI reads 50 lines + all utilities + all tools = 2,000 lines
- Cost: HIGH context

**Option 2: Duplicate client (Copy)**
- ❌ Maintain in 10 places
- ✅ AI reads 50 lines + one tool = 250 lines
- Cost: LOW context

**If AI runs 1,000 times per day:**
- Shared: 2,000 lines × 1,000 = 2,000,000 tokens
- Duplicate: 250 lines × 1,000 = 250,000 tokens

**Savings:** 1,750,000 tokens (87.5% reduction!)

**Is it worth duplicating 50 lines of code?** YES! 🎯

---

## Real Script Examples

Let's look at actual file sizes from beyond-mcp:

```
scripts/
├── status.py         157 lines  (check exchange status)
├── markets.py        254 lines  (list all markets)
├── market.py         219 lines  (get one market)
├── orderbook.py      205 lines  (market orderbook)
├── trades.py         233 lines  (recent trades)
├── search.py         465 lines  (cached search - most complex!)
├── events.py         226 lines  (list events)
├── event.py          205 lines  (get one event)
├── series_list.py    214 lines  (browse series)
└── series.py         196 lines  (series details)
```

Each script:
- Works independently
- Has inline dependencies
- Includes its own client code
- Has its own formatters
- Provides dual output (human/JSON)

**AI's perspective:**
- Want market data? Read `markets.py` (254 lines) ✅
- Want to search? Read `search.py` (465 lines) ✅
- Want both? Read both (719 lines) ✅

**Not:** Read everything (2,374 lines) ❌

---

## The Pattern in Practice

### Structure of Each Script

```python
#!/usr/bin/env python3
# /// script
# dependencies = ["httpx", "click"]
# ///

"""
Documentation here
What it does, how to use it
"""

# 1. CONFIGURATION
API_BASE_URL = "..."
TIMEOUT = 30.0

# 2. CLIENT CODE (duplicated, but that's OK!)
class Client:
    def __init__(self): ...
    def make_request(self): ...

# 3. BUSINESS LOGIC
def process_data(raw_data): ...

# 4. FORMATTING
def format_human(data): ...

# 5. CLI INTERFACE
@click.command()
@click.option('--json', is_flag=True)
def main(output_json): ...

# 6. ENTRY POINT
if __name__ == "__main__":
    main()
```

---

## When to Use This Pattern

### ✅ Use standalone scripts when:

- Building AI-facing tools
- Context efficiency matters
- Have multiple distinct operations (5+ commands)
- Each operation is fairly independent
- Want maximum portability
- Team shares tools via git

### ❌ Don't use standalone scripts when:

- Building a single monolithic tool
- Tight coupling between operations
- Only 2-3 simple commands
- Need complex shared state
- Traditional app with users (not AI)

---

## How to Build Your Own

### Step 1: Create the script

```bash
touch my_tool.py
chmod +x my_tool.py
```

### Step 2: Add the header

```python
#!/usr/bin/env python3
# /// script
# dependencies = [
#     "httpx",      # For HTTP requests
#     "click",      # For CLI
# ]
# ///
```

### Step 3: Write self-contained code

- Include all the logic you need
- Don't import from other local files
- Copy small utilities if needed

### Step 4: Run it!

```bash
uv run my_tool.py
```

---

## Advanced: Caching

Look at `search.py` for an advanced example:

```python
# /// script
# dependencies = [
#     "httpx",
#     "click",
#     "pandas",     # For smart caching!
# ]
# ///

CACHE_DIR = Path(".kalshi_cache")
CACHE_TTL = 6 * 3600  # 6 hours

def build_cache():
    """Download all data once, search locally forever"""
    # Download ~7,000 markets (takes 2-5 min)
    # Save as pandas DataFrame
    # Future searches = instant!
```

**First run:** 2-5 minutes (builds cache)

**Every other run:** Instant! (reads cache)

**Cache expiry:** 6 hours (auto-refresh)

This turns a slow operation into a fast one - critical for AI tools!

---

## Comparison with Other Approaches

### vs MCP Server

| Aspect | MCP | Standalone Scripts |
|--------|-----|-------------------|
| **Context preservation** | ❌ Poor | ✅ Good |
| **Portability** | 😐 MCP clients | ✅ Anywhere |
| **Setup** | Medium | Zero |
| **Auto-discovery** | ✅ Yes | ❌ No |

### vs CLI

| Aspect | CLI | Standalone Scripts |
|--------|-----|-------------------|
| **Context efficiency** | 😐 Medium | ✅ Best |
| **Code organization** | ✅ Better | 😐 Duplicated |
| **Human-friendly** | ✅ Better | 😐 OK |
| **AI-friendly** | 😐 Good | ✅ Best |

### vs Skills

Skills ARE standalone scripts + auto-discovery for Claude Code!

---

## Key Takeaways

1. **Inline dependencies** = Zero setup, just run
2. **Self-contained** = AI reads less, costs less
3. **Code duplication** = OK when it saves context
4. **Progressive disclosure** = Load only what you need
5. **PEP 723** = Standard, works everywhere

The `uv` + inline dependencies pattern is perfect for AI tools where context efficiency matters more than traditional engineering principles.

---

## Try It Yourself!

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Copy any script from `apps/3_file_system_scripts/scripts/`
3. Run it: `uv run status.py`
4. Modify it - everything you need is right there!

No virtual env, no pip install, no setup. Just code and run. 🚀
