# AgentMaker

**通过自然对话创建专属AI智能体 — 无需编程基础**

## 项目简介

AgentMaker 是一款AI驱动的工具，通过简单的对话引导，帮助用户创建专家级的专属AI智能体。只需告诉它你的需求，它就会自动生成并部署定制化的智能体。

**无需编程。无技术术语。纯自然语言。**

## 核心功能

- **自然对话界面** — 通过简单聊天引导智能体创建
- **多平台输出** — 同时生成 OpenClaw、LangChain、AutoGen、CrewAI 等多个平台的版本
- **融合顶级开源设计** — 包含 Datawhale、Hugging Face、Microsoft、NirDiamant 等项目的设计思想
- **本地优先** — 所有操作均在本地完成

## 快速开始

```bash
git clone https://github.com/wsererer/agent-maker-skill.git
cd agent-maker-skill
pip install pyyaml
python scripts/generate_agent.py
```

或在 OpenClaw 中说："帮我创建一个写文案的AI助手"

## 工作原理

1. **理解需求** — 通过对话了解用户需求
2. **意图转译** — 将大白话转为系统指令
3. **多平台生成** — 创建各平台配置
4. **静默部署** — 自动写入目标目录
5. **完成通知** — 告知使用方法

## 开发说明

- 本项目由 **AI辅助生成**
- 欢迎提交Issue和PR

## 许可证

MIT 许可证
