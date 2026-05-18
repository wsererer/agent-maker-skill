# AgentMaker

**Create Custom AI Agents Through Natural Conversation — No Coding Required.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)

## What is AgentMaker?

AgentMaker is an AI-powered tool that helps you create expert-level AI agents through a simple guided conversation. Just tell it what you need, and it automatically generates and deploys a custom agent for you.

**No coding required. No technical jargon. Just natural language.**

## Features

- **Natural Conversation Interface** — Guide the agent creation by simply chatting
- **Multi-Platform Output** — Generate agents for OpenClaw, LangChain, AutoGen, CrewAI, and more
- **Built on Best Practices** — Incorporates design patterns from Datawhale, Hugging Face, Microsoft, and NirDiamant's open-source projects
- **Privacy-First** — Everything runs locally on your machine

## Supported Platforms

| Platform | Output File | Description |
|----------|-------------|-------------|
| OpenClaw | `SKILL.md` | Native OpenClaw skill |
| LangChain | `langchain_agent.py` | Python agent with ReAct loop |
| AutoGen | `autogen_config.json` | Microsoft AutoGen configuration |
| CrewAI | `crewai_config.yaml` | CrewAI orchestration |
| Universal | `system_prompt.md` | Works with any AI platform |

## Quick Start

```bash
git clone https://github.com/wsererer/agent-maker-skill.git
cd agent-maker-skill
pip install pyyaml
python scripts/generate_agent.py
```

Or tell OpenClaw: "Create a new AI agent that helps me write articles"

## How It Works

1. **Understand** — Guide creation through natural conversation
2. **Translate** — Convert plain language to system instructions
3. **Generate** — Create multi-platform agent configurations
4. **Deploy** — Automatically write files to appropriate directories
5. **Notify** — Inform the user with clear usage instructions

## Architecture

| Pattern | Source | Application |
|---------|--------|-------------|
| ReAct | Hugging Face | Tool calling & reasoning |
| Plan-and-Solve | Datawhale | Task decomposition |
| Reflection | Microsoft | Self-improvement & error handling |
| Memory Management | NirDiamant | Context & preference storage |

## Development Notes

- This project was **generated with AI assistance**
- Contributions and improvements welcome
- Please report issues via GitHub Issues

## License

MIT License

## Acknowledgments

Design patterns incorporated from:
- Datawhale hello-agents
- Hugging Face agents-course
- Microsoft AI Agents for Beginners
- NirDiamant GenAI_Agents
- 500+ AI Agents Projects
