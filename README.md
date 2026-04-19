# LLM Council

Ask three top AI models in parallel, get one synthesized answer. Built for high-impact decisions where a single model can be wrong in expensive ways.

---

## What it does

You send one question. Three models answer it independently. A fourth step merges the answers into a single recommendation that highlights agreements, disagreements, and trade-offs.

Works as:
- A **CLI tool** for quick one-off consultations
- A **project-aware agent** that reads your codebase first
- An **MCP server** that plugs directly into Claude Code

---

## Why use it

- **Blind spots get smaller.** Different model families are wrong about different things.
- **Disagreement is a signal.** When the council splits, you learn where the real trade-offs are.
- **Synthesis beats voting.** The aggregator explains the why, not just the what.

Not a silver bullet. Good for architecture choices, security reviews, hard bugs. Overkill for renaming a variable.

---

## The council

| Provider | Model | Role |
|----------|-------|------|
| OpenAI | `gpt-5.4` | Deep reasoning, complex logic |
| Anthropic | `claude-opus-4-7` | Synthesis, nuance, aggregation |
| Google | `gemini-3-pro-preview` | Breadth, creative solutions |

Claude Opus 4.7 also acts as the aggregator that merges the three responses.

---

## Quick start

```bash
git clone https://github.com/retolutz/llm-council.git
cd llm-council
pip install -r requirements.txt
cp .env.example .env
# Open .env and add your three API keys
```

First consultation:

```bash
python council_agent.py ask "Should we split this monolith now or later?"
```

---

## How to use it

### Option 1 — Quick CLI

For one-off questions. Fastest to get started.

```bash
# General question
python council_agent.py ask "Redis vs Memcached for a high-traffic API?"

# Code review
python council_agent.py review src/auth.py --focus security

# Architecture decision
python council_agent.py architect "Microservices or modular monolith for a 4-person team?"

# Debug help
python council_agent.py debug "App crashes on login, memory spikes to 4GB"

# Security audit
python council_agent.py security src/api/ --context "Public-facing REST API"

# Refactor suggestions
python council_agent.py refactor legacy/old_service.py --goals "modernize, add tests"

# Interactive session
python council_agent.py interactive

# Check which models are configured
python council_agent.py status
```

### Option 2 — Project-aware council

The council reads your codebase before answering. Slower, better for non-trivial changes.

```bash
# Interactive: council asks clarifying questions first
python project_council.py

# With a specific task
python project_council.py --task "Add JWT authentication with refresh tokens"

# Skip clarifying questions
python project_council.py ask "How should I structure the API layer?" --quick

# Just analyze the project structure
python project_council.py --analyze
```

What happens under the hood:

```
1. Detect language, framework, project structure
2. Ask up to 5 clarifying questions per model, deduplicated
3. Read the files that matter for your question
4. Send all three models the same context
5. Aggregate into one recommendation
```

### Option 3 — Claude Code integration (MCP)

Make the council available as tools inside Claude Code. Once set up, any Claude Code session can call `council_ask`, `council_review`, `council_debug`, `council_architecture`, `council_security`, `council_refactor`.

**Global install (all projects):**

```bash
claude mcp add council python /path/to/llm-council/mcp_council_server.py \
  --scope user \
  -e "OPENAI_API_KEY=sk-..." \
  -e "ANTHROPIC_API_KEY=sk-ant-..." \
  -e "GOOGLE_API_KEY=AIza..."
```

**Per-project install** - drop this in your project root as `.mcp.json`:

```json
{
  "mcpServers": {
    "council": {
      "command": "python",
      "args": ["/path/to/llm-council/mcp_council_server.py"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "GOOGLE_API_KEY": "AIza..."
      }
    }
  }
}
```

Restart Claude Code. Then in any session:

> "Ask the council to review this authentication code."
> "Get the council's opinion on GraphQL vs REST for our use case."
> "Have the council help debug this connection timeout."

---

## Council types

| Type | Use case |
|------|----------|
| `ask` | General questions, research, planning |
| `review` | Code quality, bugs, best practices |
| `architecture` | System design, tech stack choices |
| `debug` | Root cause analysis for complex issues |
| `security` | OWASP-style audits, auth patterns |
| `refactor` | Modernization, reducing technical debt |

---

## When to use the council

**Yes:**
- Architecture or framework choices you will live with for months
- Security-critical code before it ships
- Complex bugs where the root cause is unclear
- Decisions where being wrong is expensive

**No:**
- Simple refactors or renames
- Time-sensitive production fixes
- Trivia a search engine answers
- Budget-constrained routine work

---

## Cost per consultation

Three model calls plus one aggregation. Rough range:

| Step | Cost |
|------|------|
| GPT-5.4 | $0.10 - $0.60 |
| Claude Opus 4.7 | $0.10 - $0.30 |
| Gemini 3 Pro | $0.05 - $0.15 |
| Aggregation (Opus 4.7) | $0.05 - $0.20 |
| **Total** | **$0.30 - $1.25** |

Rule of thumb: if being wrong costs you less than 15 minutes of work, skip the council.

---

## Requirements

- Python 3.9+
- At least one API key (all three recommended)
- For Claude Code integration: Claude Code CLI installed

Dependencies:

```
openai>=1.40.0
anthropic>=0.40.0
google-genai>=1.0.0
rich>=13.7.0
click>=8.1.7
python-dotenv>=1.0.0
mcp>=1.0.0
```

---

## Python API

```python
from council_agent import CouncilAgent

agent = CouncilAgent()
result = agent.consult(
    task="Review this code for security issues",
    context=open("api.py").read(),
    council_type="security",
    show_individual=True,
)
print(result["synthesis"])
```

```python
from project_council import ProjectCouncil

council = ProjectCouncil("/path/to/project")
council.analyze_project()

questions = council.generate_clarifying_questions("Add authentication")
# answer questions, then:
result = council.consult_council(
    task="Add JWT authentication",
    answers={"method": "JWT with refresh tokens"},
    relevant_code={"auth.py": "...code..."},
    council_type="implement",
)
```

---

## Project layout

```
llm-council/
├── council_agent.py         CLI for quick consultations
├── project_council.py       Project-aware interactive agent
├── mcp_council_server.py    MCP server for Claude Code
├── council.py               Core multi-model library
├── enhancer.py              Single-model prompt enhancer
├── strategies.py            Prompt enhancement strategies
├── cli.py                   CLI entry point
├── requirements.txt
├── setup.py
└── .env.example
```

---

## Updating model versions

Model IDs live in `mcp_council_server.py`. When a provider ships a new flagship model, update the four `model=` lines - three for the members, one for the aggregator. Keep the aggregator on whichever model is strongest at synthesis; Opus has been reliable for that role.

---

## License

MIT
