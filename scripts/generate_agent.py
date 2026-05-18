# -*- coding: utf-8 -*-
"""
AgentMaker 核心生成器 v2.0
根据用户需求，自动生成专家级专属AI Agent的多平台配置
支持：OpenClaw / LangChain / AutoGen / CrewAI / 通用System Prompt
"""
import json
import sys
import os
import re
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 输出目录
SKILLS_DIR = r'C:\Users\Administrator\.openclaw\workspace\skills'
OUTPUT_DIR = r'C:\Users\Administrator\.openclaw\workspace\agent-output'
MEMORY_DIR = r'C:\Users\Administrator\.openclaw\workspace\memory'


def sanitize_name(name):
    """将用户输入的名称转换为合法的文件名/目录名"""
    name = name.lower()
    name = re.sub(r'[^a-z0-9\u4e00-\u9fa5]', '-', name)
    name = re.sub(r'-+', '-', name)
    return name[:50].strip('-')


def sanitize_python_name(name):
    """转换为Python变量名"""
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '_', name)
    name = re.sub(r'_+', '_', name)
    return name.strip('_')[:50]


def generate_system_prompt(agent_config):
    """生成通用的System Prompt（适用于所有平台）"""
    display_name = agent_config.get('display_name', '我的助手')
    personality = agent_config.get('personality', '乐于助人，简洁高效')
    capabilities = agent_config.get('capabilities', '解答问题，完成各种任务')
    
    return f"""你是{display_name}，一个专为用户服务的AI助手。

## 核心身份
{personality}

## 你能做什么
{capabilities}

## 工作原则
1. 主动理解用户需求，不确定时主动确认
2. 复杂任务分解步骤，逐步完成
3. 遇到错误及时报告，不隐瞒问题
4. 不知道就说不知道，不编造信息
"""


# ============ OpenClaw SKILL.md ============
def generate_openclaw_skill(agent_config):
    """生成OpenClaw版SKILL.md"""
    name = agent_config['name']
    display_name = agent_config.get('display_name', name)
    description = agent_config.get('description', '一个AI助手')
    personality = agent_config.get('personality', '乐于助人，简洁高效')
    capabilities = agent_config.get('capabilities', '解答问题，完成各种任务')
    scenarios = agent_config.get('scenarios', ['通用助手'])
    has_web = agent_config.get('has_web', False)
    has_file = agent_config.get('has_file', False)
    has_memory = agent_config.get('has_memory', True)
    
    system_prompt = generate_system_prompt(agent_config)
    
    tools = []
    if has_web:
        tools.append('- 网页搜索（web_search）')
        tools.append('- 网页内容抓取（web_fetch）')
    if has_file:
        tools.append('- 文件读写（read/write）')
    if has_memory:
        tools.append('- 记忆管理（memory_search/memory_get）')
    tools_text = '\n'.join(tools) if tools else '- 对话交互'
    scenarios_text = ', '.join(scenarios) if scenarios else '通用助手'
    
    return f"""---
name: {name}
description: {display_name} - {description}
---

# {display_name}

## 身份设定

{display_name}，{personality}

## 核心能力

{capabilities}

## 适用场景

{scenarios_text}

## 工具配置

已启用以下工具：
{tools_text}

## System Prompt

```
{system_prompt}
```

## 使用指南

### 基本对话
直接发送消息，{display_name}会尽力帮助你。

### 复杂任务
{display_name}会自动分解任务，逐步完成。如需多步骤操作，会主动汇报进度。

### 记忆功能
{display_name}能够记住对话中的重要信息，提供连续性服务。

### 遇到问题
如果无法完成某些操作，{display_name}会明确告知原因并提供替代方案。
"""


# ============ LangChain Agent ============
def generate_langchain_agent(agent_config):
    """生成LangChain版Python脚本"""
    display_name = agent_config.get('display_name', '我的助手')
    personality = agent_config.get('personality', '乐于助人')
    capabilities = agent_config.get('capabilities', '解答问题')
    scenarios = agent_config.get('scenarios', ['通用助手'])
    has_web = agent_config.get('has_web', False)
    has_file = agent_config.get('has_file', False)
    has_memory = agent_config.get('has_memory', True)
    
    system_prompt = generate_system_prompt(agent_config)
    python_name = sanitize_python_name(display_name)
    
    # 根据配置生成不同的工具代码
    if has_web:
        tools_setup = '''
        # 导入必要库
        from langchain.tools import Tool
        from langchain_community.utilities import SerpAPIWrapper
        
        # 创建搜索工具
        search = SerpAPIWrapper()
        search_tool = Tool(
            name="web_search",
            func=search.run,
            description="搜索互联网获取最新信息，输入搜索关键词"
        )
        
        # 创建浏览器工具
        from langchain.tools import BraveSearch
        browser = BraveSearch()
        browser_tool = Tool(
            name="web_fetch",
            func=browser.run,
            description="抓取网页内容并提取关键信息，输入URL"
        )
        
        # 所有工具
        tools = [search_tool, browser_tool]'''
        tools_init = 'self.tools = [search_tool, browser_tool]'
    elif has_file:
        tools_setup = '''
        # 创建文件读取工具
        from langchain.tools import Tool
        import os
        
        def read_file_tool(path):
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
            return "文件不存在"
        
        file_tool = Tool(
            name="file_read",
            func=read_file_tool,
            description="读取本地文件内容，输入文件路径"
        )
        
        tools = [file_tool]'''
        tools_init = 'self.tools = [file_tool]'
    else:
        tools_setup = '''
        # 对话工具（无外部工具）
        tools = []'''
        tools_init = 'self.tools = []'
    
    return f'''# -*- coding: utf-8 -*-
"""
{display_name} - LangChain Agent
自动生成版本

依赖安装:
    pip install langchain langchain-openai langchain-community
"""

import os

class {python_name}Agent:
    """{display_name}"""
    
    def __init__(self, api_key=None, model="gpt-4"):
        if api_key is None:
            api_key = os.environ.get("OPENAI_API_KEY", "")
        
        from langchain.chat_models import ChatOpenAI
        self.llm = ChatOpenAI(openai_api_key=api_key, model=model)
        
        # 初始化工具
{tools_setup}
        
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain.prompts import PromptTemplate
        
        # System Prompt
        SYSTEM_PROMPT = """{system_prompt}"""
        
        # ReAct Prompt
        prompt_template = f"""你是一个有帮助的AI助手。

严格按照以下格式响应：
Thought: 分析当前情况
Action: 选择要使用的工具（如果需要）
Action Input: 工具的输入参数
Observation: 执行结果
... (重复直到完成)
Final Answer: 最终答案

可用工具: {{tools}}

开始！用户问题: {{input}}

{{agent_scratchpad}}"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            partial_variables={{"tools": str([t.name for t in self.tools]) if self.tools else "无"}}
        )
        
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10
        )
    
    def chat(self, message):
        """发送消息并获取回复"""
        result = self.executor.invoke({{"input": message}})
        return result["output"]
    
    def run(self, task):
        """执行单次任务"""
        return self.chat(task)


if __name__ == "__main__":
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        api_key = input("请输入OpenAI API Key: ")
    
    agent = {python_name}Agent(api_key=api_key)
    
    print("=== {display_name} ===")
    print("输入 'quit' 退出")
    
    while True:
        user_input = input("\\n你: ")
        if user_input.lower() == 'quit':
            print("再见！")
            break
        response = agent.chat(user_input)
        print(f"{display_name}: {{response}}")
'''


# ============ AutoGen Agent ============
def generate_autogen_config(agent_config):
    """生成AutoGen配置文件"""
    display_name = agent_config.get('display_name', '我的助手')
    personality = agent_config.get('personality', '乐于助人')
    capabilities = agent_config.get('capabilities', '解答问题')
    scenarios = agent_config.get('scenarios', ['通用助手'])
    has_web = agent_config.get('has_web', False)
    has_file = agent_config.get('has_file', False)
    has_memory = agent_config.get('has_memory', True)
    
    system_prompt = generate_system_prompt(agent_config)
    
    tools_list = []
    if has_web:
        tools_list.append({
            "name": "web_search",
            "description": "搜索互联网获取最新信息",
            "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}
        })
        tools_list.append({
            "name": "web_fetch", 
            "description": "抓取网页内容并提取关键信息",
            "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}
        })
    if has_file:
        tools_list.append({
            "name": "read_file",
            "description": "读取文件内容",
            "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}
        })
    
    config = {
        "name": agent_config['name'],
        "display_name": display_name,
        "description": agent_config.get('description', ''),
        "system_prompt": system_prompt,
        "model": "gpt-4",
        "tools": tools_list if tools_list else None,
        "agent_type": "ReAct",
        "max_retry": 3,
        "timeout": 60
    }
    
    return json.dumps(config, ensure_ascii=False, indent=2)


# ============ CrewAI Agent ============
def generate_crewai_yaml(agent_config):
    """生成CrewAI配置文件 - 简化版，避免YAML缩进问题"""
    display_name = agent_config.get('display_name', '我的助手')
    personality = agent_config.get('personality', '乐于助人')
    scenarios = agent_config.get('scenarios', ['通用助手'])
    system_prompt = generate_system_prompt(agent_config)
    
    # system prompt处理（去掉复杂格式，使用简单文本）
    prompt_simple = system_prompt.replace('"', '\\"').replace('\n', ' ')
    
    return f'''# {display_name} - CrewAI Configuration
# 自动生成版本

agents:
  - role: "{scenarios[0] if scenarios else '助手'}"
    backstory: "{personality}"
    goal: "为用户提供专业、高效的帮助"
    verbose: true

tasks:
  - description: "处理用户请求"
    expected_output: "专业、准确的回复"

crew:
  name: "{agent_config['name']}_crew"
  description: "{agent_config.get('description', '')}"
  agents:
    - role: "{scenarios[0] if scenarios else '助手'}"
  tasks:
    - description: "处理用户请求"
  process: sequential
  verbose: 2

# System Prompt (可用作参考)
system_prompt: "{prompt_simple}"

# CrewAI 安装: pip install crewai
# 使用示例:
# from crewai import Agent, Crew, Task, Process
# agent = Agent(role="学习辅导", backstory="耐心细致", goal="帮助用户", verbose=True)
# task = Task(description="处理用户请求", expected_output="专业回复", agent=agent)
# crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
# result = crew.kickoff()
'''


# ============ 通用 System Prompt ============
def generate_generic_system_prompt(agent_config):
    """生成通用System Prompt（适用于任何平台）"""
    display_name = agent_config.get('display_name', '我的助手')
    description = agent_config.get('description', '')
    personality = agent_config.get('personality', '乐于助人，简洁高效')
    capabilities = agent_config.get('capabilities', '解答问题，完成各种任务')
    scenarios = agent_config.get('scenarios', ['通用助手'])
    has_web = agent_config.get('has_web', False)
    has_file = agent_config.get('has_file', False)
    has_memory = agent_config.get('has_memory', True)
    
    tools_note = """
## 可用工具
"""
    if has_web:
        tools_note += """
- web_search: 搜索互联网获取最新信息
- web_fetch: 抓取网页内容并提取关键信息
"""
    if has_file:
        tools_note += """
- read_file: 读取本地文件内容
- write_file: 写入文件
"""
    if has_memory:
        tools_note += """
- memory_search: 搜索历史记忆
- memory_save: 保存重要信息到记忆
"""
    if not (has_web or has_file or has_memory):
        tools_note = ""
    
    return f"""# {display_name}

## 基本信息
- **名称**: {display_name}
- **描述**: {description}
- **适用场景**: {', '.join(scenarios)}

## 身份设定
{personality}

## 核心能力
{capabilities}

## 工作原则
1. 主动理解用户需求，不确定时主动确认
2. 复杂任务分解步骤，逐步完成
3. 遇到错误及时报告，不隐瞒问题
4. 不知道就说不知道，不编造信息
5. 保持回复简洁、有条理

{tools_note}

## 使用方法

### 基本对话
直接发送消息即可，无需特殊格式。

### 复杂任务
我会自动分解任务为多个步骤，逐步完成并汇报进度。

### 工具使用
根据任务需要，我会自动选择合适的工具来完成任务。

## 限制与边界
- 不确定的问题会如实告知
- 超出能力范围的任务会明确说明
- 遵循安全和道德准则
"""


# ============ 主生成函数 ============
def create_agent(user_answers):
    """
    根据用户回答生成多平台Agent配置
    """
    agent_name = sanitize_name(user_answers.get('name', 'my-agent'))
    
    # 创建输出目录
    output_dir = os.path.join(OUTPUT_DIR, agent_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    results = {}
    
    # 1. OpenClaw版
    openclaw_dir = os.path.join(SKILLS_DIR, agent_name)
    if not os.path.exists(openclaw_dir):
        os.makedirs(openclaw_dir)
    
    openclaw_content = generate_openclaw_skill(user_answers)
    openclaw_path = os.path.join(openclaw_dir, 'SKILL.md')
    with open(openclaw_path, 'w', encoding='utf-8') as f:
        f.write(openclaw_content)
    results['openclaw'] = openclaw_path
    
    # 2. LangChain版
    lc_content = generate_langchain_agent(user_answers)
    lc_path = os.path.join(output_dir, 'langchain_agent.py')
    with open(lc_path, 'w', encoding='utf-8') as f:
        f.write(lc_content)
    results['langchain'] = lc_path
    
    # 3. AutoGen版
    autogen_content = generate_autogen_config(user_answers)
    autogen_path = os.path.join(output_dir, 'autogen_config.json')
    with open(autogen_path, 'w', encoding='utf-8') as f:
        f.write(autogen_content)
    results['autogen'] = autogen_path
    
    # 4. CrewAI版
    crewai_content = generate_crewai_yaml(user_answers)
    crewai_path = os.path.join(output_dir, 'crewai_config.yaml')
    with open(crewai_path, 'w', encoding='utf-8') as f:
        f.write(crewai_content)
    results['crewai'] = crewai_path
    
    # 5. 通用System Prompt
    generic_content = generate_generic_system_prompt(user_answers)
    generic_path = os.path.join(output_dir, 'system_prompt.md')
    with open(generic_path, 'w', encoding='utf-8') as f:
        f.write(generic_content)
    results['generic'] = generic_path
    
    # 6. 生成README说明
    readme = f'''# {user_answers.get('display_name', '我的助手')} - 多平台Agent包

> 自动生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 包含文件

| 文件 | 适用平台 | 使用说明 |
|------|----------|----------|
| `openclaw/SKILL.md` | OpenClaw | 直接放入 `~/.openclaw/skills/` 目录 |
| `langchain_agent.py` | LangChain | `pip install langchain langchain-openai` 后运行 |
| `autogen_config.json` | AutoGen | `pip install autogen` 后加载配置 |
| `crewai_config.yaml` | CrewAI | `pip install crewai` 后加载配置 |
| `system_prompt.md` | 通用 | 适用于任何AI平台/框架 |

## 快速使用

### OpenClaw
将 `openclaw/SKILL.md` 复制到你的 OpenClaw skills 目录即可。

### LangChain
```bash
pip install langchain langchain-openai
export OPENAI_API_KEY="your-key"
python langchain_agent.py
```

### CrewAI
```python
from crewai import Agent, Crew, Task
# 加载 crewai_config.yaml 配置
```

## 配置信息
- **Agent名称**: {user_answers.get('display_name', '')}
- **描述**: {user_answers.get('description', '')}
- **性格**: {user_answers.get('personality', '')}
- **能力**: {user_answers.get('capabilities', '')}
- **场景**: {', '.join(user_answers.get('scenarios', []))}
'''
    
    readme_path = os.path.join(output_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme)
    results['readme'] = readme_path
    
    return agent_name, output_dir, results


if __name__ == '__main__':
    # 测试模式
    test_config = {
        'name': 'my-study-assistant',
        'display_name': '学习助手小智',
        'description': '帮助用户学习的专属AI助手',
        'personality': '耐心细致，循循善诱',
        'capabilities': '解答学术问题、整理学习笔记、制定学习计划、查询资料',
        'scenarios': ['学习辅导', '知识查询', '计划制定'],
        'has_web': True,
        'has_file': True,
        'has_memory': True,
    }
    
    agent_name, output_dir, results = create_agent(test_config)
    
    print(f"✅ 多平台Agent生成成功！")
    print(f"Agent名称: {agent_name}")
    print(f"保存位置: {output_dir}")
    print()
    print("生成的文件:")
    for platform, path in results.items():
        print(f"  {platform}: {path}")