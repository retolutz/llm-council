# LLM Council

A powerful multi-model AI system that consults the best LLMs (o3, Claude Opus 4, Gemini 2.5 Pro) in parallel and synthesizes their responses for superior results.

## Why Use a Council?

Single LLMs have blind spots. A council of diverse models provides:
- **Multiple perspectives** on complex problems
- **Cross-validation** of recommendations
- **Synthesis** of the best ideas from each model
- **Higher confidence** for important decisions

## Models

| Provider | Model | Strength |
|----------|-------|----------|
| OpenAI | **o3** | Deep reasoning, complex logic |
| Anthropic | **Claude Opus 4** | Synthesis, nuance, aggregation |
| Google | **Gemini 2.5 Pro** | Broad knowledge, creative solutions |

## Components

| Component | Description |
|-----------|-------------|
| `project_council.py` | **Deep project-aware agent** - Analyzes codebase, asks clarifying questions, reads relevant code |
| `council_agent.py` | **Standalone CLI** - Quick access for code review, debug, security, architecture |
| `mcp_council_server.py` | **MCP Server** - Native Claude Code integration |
| `council.py` | **Core library** - Prompt enhancement with council |

---

## Installation

```bash
git clone https://github.com/retolutz/llm-council.git
cd llm-council
pip install -r requirements.txt
```

## Configuration

```bash
cp .env.example .env
```

Add your API keys:
```
OPENAI_API_KEY=sk-proj-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
```

---

## Usage

### 1. Project Council (Recommended for Complex Tasks)

The most powerful mode. Deeply understands your project before providing recommendations.

```bash
# Interactive mode - council asks questions to understand context
python project_council.py

# With specific task
python project_council.py --task "Add user authentication"

# Quick mode (skip clarifying questions)
python project_council.py ask "How should I structure the API?" --quick

# Just analyze project structure
python project_council.py --analyze

# Check available models
python project_council.py status
```

#### How Project Council Works

```
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 1: PROJECT ANALYSIS                                       │
│  - Detect language/framework (Python, JS, Go, Rust, etc.)        │
│  - Map project structure                                         │
│  - Identify dependencies                                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 2: CLARIFYING QUESTIONS (5 per LLM)                       │
│                                                                  │
│  o3: "What authentication method do you prefer?"                 │
│  Claude: "Are there existing user models to integrate with?"     │
│  Gemini: "Should this support SSO/OAuth providers?"              │
│                                                                  │
│  Questions are deduplicated and presented to user                │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 3: CODE ANALYSIS                                          │
│  - Identify relevant files based on answers                      │
│  - Read and analyze key code sections                            │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│  PHASE 4: COUNCIL DELIBERATION                                   │
│                                                                  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                      │
│  │   o3    │    │ Claude  │    │ Gemini  │                      │
│  │Reasoning│    │Synthesis│    │Creative │                      │
│  └────┬────┘    └────┬────┘    └────┬────┘                      │
│       └──────────────┼──────────────┘                            │
│                      ▼                                           │
│            ┌─────────────────┐                                   │
│            │  Claude Opus 4  │                                   │
│            │   Aggregator    │                                   │
│            └────────┬────────┘                                   │
│                     │                                            │
│                     ▼                                            │
│         PROJECT-AWARE RECOMMENDATION                             │
└──────────────────────────────────────────────────────────────────┘
```

---

### 2. Council Agent CLI

Quick access to council expertise for specific tasks.

```bash
# Code Review
python council_agent.py review path/to/file.py
python council_agent.py review src/auth.py --focus security

# Architecture Decisions
python council_agent.py architect "Should I use microservices or monolith?"
python council_agent.py architect "Redis vs Memcached for caching?" --context "High-traffic web app"

# Debugging Help
python council_agent.py debug "App crashes when user logs in"
python council_agent.py debug "Memory leak in production" --code src/server.py --error "OOM killed"

# Security Audit
python council_agent.py security api/endpoints.py
python council_agent.py security src/ --context "Public-facing REST API"

# Refactoring Suggestions
python council_agent.py refactor legacy/old_code.py --goals "modernize, improve testability"

# General Questions
python council_agent.py ask "What's the best approach for real-time updates?"

# Interactive Mode
python council_agent.py interactive

# Check Status
python council_agent.py status
```

---

### 3. Claude Code Integration (MCP Server)

Integrate the council directly into Claude Code for seamless access.

#### Global Installation (All Projects)

```bash
claude mcp add council python /path/to/llm-council/mcp_council_server.py \
  --scope user \
  -e "OPENAI_API_KEY=sk-..." \
  -e "ANTHROPIC_API_KEY=sk-ant-..." \
  -e "GOOGLE_API_KEY=AIza..."
```

#### Project-Specific Installation

Create `.mcp.json` in your project:

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

#### Available Tools in Claude Code

After setup, you can use these commands in any Claude Code session:

| Command | Example |
|---------|---------|
| Code Review | "Ask the council to review this authentication code" |
| Architecture | "Get the council's opinion on using GraphQL vs REST" |
| Debug | "Have the council help debug this connection timeout" |
| Security | "Run a council security audit on the API endpoints" |
| Refactor | "Ask the council how to refactor this legacy module" |
| General | "What does the council think about this approach?" |

---

### 4. Prompt Enhancement

The original prompt enhancement functionality is also available.

```bash
# Single model (o3)
prompt-enhancer enhance "Write a blog post about AI"

# LLM Council enhancement
prompt-enhancer council "Write a business plan for an AI startup"

# Show all individual responses
prompt-enhancer council -a "Create a marketing strategy"

# Analyze a prompt
prompt-enhancer analyze "Make my website faster"

# List strategies
prompt-enhancer strategies
```

---

## Council Types

| Type | Use Case | Best For |
|------|----------|----------|
| `review` | Code quality, bugs, best practices | PR reviews, code audits |
| `architecture` | System design, tech decisions | New features, migrations |
| `debug` | Root cause analysis, fix suggestions | Production issues, complex bugs |
| `security` | Vulnerability assessment, OWASP | Security audits, compliance |
| `refactor` | Code improvement, modernization | Technical debt, cleanup |
| `test` | Test case generation, coverage | QA, edge cases |
| `general` | Any complex question | Research, planning |

---

## When to Use the Council

**Use the Council when:**
- Making important architecture decisions
- Reviewing security-critical code
- Debugging complex issues with multiple possible causes
- Wanting diverse perspectives on a problem
- The cost of being wrong is high

**Don't use the Council when:**
- Simple, straightforward tasks
- Time-sensitive quick fixes
- Budget is a major concern (3x API costs)

---

## Cost Considerations

Each council consultation calls 3 models + 1 aggregation.

| Model | Estimated Cost |
|-------|----------------|
| o3 | ~$0.10-0.50 |
| Claude Opus 4 | ~$0.05-0.20 |
| Gemini 2.5 Pro | ~$0.01-0.05 |
| Aggregation | ~$0.05-0.15 |
| **Total** | **~$0.20-0.90 per consultation** |

Use wisely for high-value decisions.

---

## Python API

```python
# Project Council
from project_council import ProjectCouncil

council = ProjectCouncil("/path/to/project")
council.analyze_project()

# Get clarifying questions
questions = council.generate_clarifying_questions("Add authentication")

# Consult with full context
result = council.consult_council(
    task="Add JWT authentication",
    answers={"preferred_method": "JWT with refresh tokens"},
    relevant_code={"auth.py": "...code..."},
    council_type="implement"
)
print(result)

# Council Agent
from council_agent import CouncilAgent

agent = CouncilAgent()
result = agent.consult(
    task="Review this code for security issues",
    context=open("api.py").read(),
    council_type="security",
    show_individual=True
)
print(result["synthesis"])

# Prompt Enhancement
from council import LLMCouncil

council = LLMCouncil()
result = council.enhance("Write a marketing email")
print(result.enhanced_prompt)
print(result.aggregator_reasoning)
```

---

## Architecture

```
llm-council/
├── project_council.py     # Deep project-aware agent
├── council_agent.py       # Standalone CLI tool
├── mcp_council_server.py  # MCP server for Claude Code
├── council.py             # Core council for prompt enhancement
├── enhancer.py            # Single-model prompt enhancer
├── strategies.py          # Enhancement strategies
├── cli.py                 # CLI entry point
├── requirements.txt       # Dependencies
├── setup.py               # Package setup
├── .env.example           # Environment template
└── CLAUDE_CODE_SETUP.md   # Claude Code setup guide
```

---

## Requirements

- Python 3.9+
- API keys for at least one provider (all three recommended)

### Dependencies

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

## License

MIT

---

## Contributing

Contributions welcome! Please open an issue or PR.

---

## Credits

Built with the best LLMs:
- [OpenAI o3](https://openai.com)
- [Anthropic Claude Opus 4](https://anthropic.com)
- [Google Gemini 2.5 Pro](https://deepmind.google/technologies/gemini/)
