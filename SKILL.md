---
name: agent-maker
description: 全自动创建专属AI Agent的工具。当用户想要创建一个新的AI助手、想要一个能完成特定任务的Agent、想要定制自己的AI助手时使用。通过极简对话引导，自动生成并静默部署专家级专属Agent。支持多平台输出：OpenClaw / LangChain / AutoGen / CrewAI / 通用System Prompt。
---

# AgentMaker v2.0

全自动创建专属AI Agent的工具。融合Datawhale、Hugging Face、Microsoft、NirDiamant、500+开源项目的设计思想，一键生成多平台通用的专家级Agent。

## 核心能力

### 一次生成，多平台部署

生成的Agent同时输出5个版本：

| 版本 | 文件 | 适用平台 |
|------|------|----------|
| **OpenClaw** | `openclaw/SKILL.md` | OpenClaw（直接使用） |
| **LangChain** | `langchain_agent.py` | Python + LangChain框架 |
| **AutoGen** | `autogen_config.json` | Microsoft AutoGen |
| **CrewAI** | `crewai_config.yaml` | CrewAI编排框架 |
| **通用** | `system_prompt.md` | 任何AI平台/框架 |

## 工作流程

### 第一步：理解需求

通过极简对话了解用户需求，每次只问一个问题：

1. "你希望这个助手平时帮你做什么？" → 确定**核心场景**
2. "它需要能上网查最新的资料吗？" → 确定**联网能力**
3. "需要处理文件吗，比如Word/Excel？" → 确定**文件处理**
4. "需要记住之前聊过的事吗？" → 确定**记忆功能**
5. "给它起个名字吧？" → 确定**Agent名称**

### 第二步：意图转译

将用户大白话自动转译为系统指令：

| 用户说的话 | 转译结果 |
|------------|----------|
| "帮我写文案/文章" | capabilities += 内容创作 |
| "能上网查" | has_web = True |
| "处理Excel/Word" | has_file = True |
| "记住我说的" | has_memory = True |
| "要专业一点" | personality = 专业严谨 |
| "陪我聊天" | personality = 亲切友好 |

### 第三步：多平台生成

调用 `scripts/generate_agent.py` 自动生成所有平台配置：

```bash
python scripts/generate_agent.py
```

脚本会生成：
- `~/.openclaw/skills/{agent-name}/SKILL.md` — OpenClaw版
- `agent-output/{agent-name}/` — 其他平台配置文件

### 第四步：静默部署

自动将配置写入目标目录，**绝不打印代码让用户复制**。

### 第五步：成功通知

告诉用户：
- "✅ {Agent名称} 已创建完成！"
- 生成了哪些平台的版本
- 每个版本的使用方法

## 输出文件说明

### OpenClaw版 (SKILL.md)
完整的OpenClaw Skill配置，包含：
- YAML frontmatter元数据
- 身份设定、核心能力、适用场景
- 工具配置（web_search/web_fetch/file/memory）
- System Prompt

### LangChain版 (langchain_agent.py)
可直接运行的Python脚本：
- 导入LangChain必要的库
- 定义ReAct Agent
- 配置对话记忆
- 包含测试代码（可删除）

### AutoGen版 (autogen_config.json)
JSON格式的配置：
- system_prompt
- 模型配置
- 工具定义（OpenAPI格式）
- Agent类型和参数

### CrewAI版 (crewai_config.yaml)
YAML格式的Crew配置：
- Agent定义（backstory/goal/role）
- 工具配置
- Task定义
- Crew流程配置

### 通用版 (system_prompt.md)
纯System Prompt，无任何框架依赖：
- 完整的身份设定
- 能力描述
- 工作原则
- 工具说明（通用描述）

## 匹配最佳实践

根据用户场景，自动匹配以下模板：

| 场景 | 匹配架构 |
|------|----------|
| 客服/FAQ | Tool-Using Agent + Memory |
| 内容创作 | Creative Writing + Reflection |
| 数据分析 | Data Agent + RAG |
| 代码调试 | Code Agent + Reflection + ReAct |
| 研究调研 | Research Agent + Web Search |
| 日程管理 | Task Agent + Calendar API |

## 异常处理

生成过程中的异常：

1. **目录写入失败** → 报告具体路径错误，建议检查权限
2. **名称冲突** → 自动添加数字后缀，如 `my-agent-2`
3. **配置不完整** → 用默认值补充，优先保证能运行

## 使用示例

### 示例对话

**用户**：我想创建一个帮我写文案的助手

**AgentMaker**：
1. "你希望这个助手平时帮你做什么？" → 内容创作
2. "它需要能上网查资料吗？" → 是
3. "需要处理文件吗？" → Word/Excel
4. "需要记住你的偏好习惯吗？" → 是
5. "叫什么名字好呢？" → 文案小能手

**生成结果**：
```
✅ 文案小能手 已创建完成！

📦 已生成5个平台版本：
• OpenClaw: 直接使用
• LangChain: pip install langchain 后运行
• AutoGen: pip install autogen 后加载
• CrewAI: pip install crewai 后加载
• 通用: system_prompt.md 适用于任何平台

以后直接说"帮我写一篇XX文案"，它就会来帮你啦~
```

## 参考资料

生成Agent时需要融合的设计思想：

- **Datawhale hello-agents**：ReAct/Plan-and-Solve/Reflection三范式
- **Hugging Face agents-course**：工具调用规范、ReAct循环
- **Microsoft ai-agents**：三维度设计原则、生命周期管理
- **NirDiamant GenAI_Agents**：Agent类型匹配、最佳实践模板
- **500+ AI Agents Projects**：行业应用场景库

详见 [references/architecture.md](references/architecture.md)