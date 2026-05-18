# AgentMaker 参考知识库

> 融合五大开源项目的设计思想，用于自动生成专家级AI Agent配置

---

## 一、Datawhale Hello-Agents — 代码级鲁棒性

### 核心理念
生成的Agent必须具备清晰的底层执行逻辑，包含完备的异常处理和边界防御。

### 三范式精要

#### ReAct（边想边做）
```
Thought: 分析当前情况...
Action: Search["查询内容"]
Observation: 获取结果
→ 循环直到 Finish[最终答案]
```
适用：需要搜索+推理的复杂任务

#### Plan-and-Solve（先思后行）
- 规划阶段：生成结构化行动计划
- 执行阶段：严格按计划执行
适用：多步骤数学题、报告撰写、代码生成

#### Reflection（自我反思）
- 执行 → 反思 → 优化 → 循环
- 反思维度：事实错误、逻辑漏洞、效率问题、遗漏信息

### 异常处理模板
```python
try:
    result = execute_task()
except ToolNotFoundError:
    # 回退到默认工具
    result = fallback_execute()
except NetworkTimeout:
    # 重试+降级
    result = retry_or_degrade()
except Exception as e:
    # 记录+报告
    log_error(e)
    report_to_user(str(e))
```

---

## 二、Hugging Face agents-course — 工具调用规范

### ReAct循环实现
```python
def react_loop(query):
    history = []
    while True:
        thought = llm.think(query, history)
        if thought.action == 'finish':
            return thought.output
        result = execute_tool(thought.tool, thought.params)
        history.append((thought, result))
```

### 工具定义规范
```json
{
  "name": "search_web",
  "description": "搜索互联网获取最新信息",
  "parameters": {
    "query": {
      "type": "string",
      "description": "搜索关键词"
    }
  }
}
```

### 关键原则
- 工具描述要清晰，LLM靠description判断何时调用
- 每次工具调用后要检查结果
- 超过3次同一工具失败，触发降级

---

## 三、Microsoft AI Agents — 企业级模块化

### 设计原则（三维度）
- **空间维度**：连接而非替代，支持多模态
- **时间维度**：回顾历史、关注当下、适应未来
- **核心维度**：承认不确定性，建立信任机制

### 生命周期管理
```
初始化 → 接收请求 → 理解意图 → 规划执行 → 工具调用 → 响应用户
                                    ↓
                              异常处理 → 降级/重试
```

### 安全机制
- 每次外部操作验证输入
- 数据库只读权限
- 敏感操作需要确认
- 操作日志完整记录

---

## 四、NirDiamant GenAI_Agents — 最佳实践案例库

### Agent类型匹配表

| 用户需求 | 推荐Agent类型 |
|----------|--------------|
| 客服/FAQ | Tool-Using Agent + Memory |
| 内容创作 | Creative Writing Agent |
| 数据分析 | Data Analysis Agent + RAG |
| 代码调试 | Code Agent + Reflection |
| 研究调研 | Research Agent + Web Search |
| 日程管理 | Task Agent + Calendar API |

### 记忆配置模板
```python
memory_config = {
    '短期记忆': '当前会话上下文',
    '长期记忆': '用户偏好+重要事实',
    '技能记忆': '可复用的工作流程'
}
```

---

## 五、500+ AI Agents Projects — 场景化架构

### 行业应用模板

#### 客服机器人
- 意图识别 → FAQ匹配 → 多轮对话 → 满意度跟踪
- 关键组件：NLU引擎、对话管理、知识库

#### 数据分析助手
- 数据获取 → 清洗整理 → 分析建模 → 可视化
- 关键组件：API集成、数据管道、图表生成

#### 写作助手
- 主题理解 → 大纲生成 → 内容撰写 → 审核优化
- 关键组件：模板库、风格迁移、质量评估

---

## 六、自动生成检查清单

生成Agent配置时，必须满足：

- [ ] 有明确的System Prompt定义身份
- [ ] 工具描述完整、无歧义
- [ ] 异常处理有降级路径
- [ ] 记忆配置明确（开/关/层级）
- [ ] 输出格式有示例
- [ ] 边界情况有处理

---

## 七、对话流程模板

### 引导问题顺序
1. "你希望这个助手平时帮你做什么？" → 确定核心场景
2. "它需要能上网查资料吗？" → 确定web搜索
3. "需要处理文件吗，比如Word/Excel？" → 确定文件处理
4. "需要记住之前聊过的事吗？" → 确定记忆功能
5. "给它起个名字吧？" → 确定名称

### 意图转译规则
| 用户大白话 | 转译为系统指令 |
|------------|--------------|
| "帮我写文案" | capabilities += 内容创作 |
| "能上网查" | has_web = True |
| "处理Excel" | has_file = True, tools += Excel |
| "记住我说的" | has_memory = True |
| "要专业一点" | personality = 专业严谨 |