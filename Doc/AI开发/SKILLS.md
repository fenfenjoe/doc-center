# SKILLS

## 为什么要写SKILLS




## 如何写SKILLS

### 概述

Skills 是一种让 AI 助手具备特定领域能力的机制，可以理解为给 AI 编写的"插件"或"技能包"。通过定义 Skills，我们可以让 AI 按照特定的流程、规范和最佳实践来处理任务。

**核心特点：**
- 结构化的任务执行流程
- 可复用的领域知识封装
- 自动触发机制（基于描述匹配）
- 标准化的输入输出格式

### Skills 的基本结构

一个标准的 Skill 通常包含以下部分：

```markdown
# Skill Name

## Description
简短描述这个技能的用途和适用场景

## When to Use
明确定义触发条件，什么情况下应该使用这个技能

## Input Format
定义输入参数的格式和要求

## Process
详细的执行步骤和流程

## Output Format
定义输出结果的格式

## Examples
提供具体的使用示例
```

### 实践步骤

#### 1. 明确技能目标

首先确定你要解决什么问题。例如：
- 代码审查（Code Review）
- API 文档生成
- 测试用例编写
- 代码重构建议

#### 2. 设计触发条件

定义清晰的触发描述，让 AI 知道何时使用这个技能：

```markdown
## When to Use
- 用户明确要求进行代码审查
- 用户提交包含 "/review" 的命令
- 用户询问代码质量或改进建议
```

#### 3. 定义执行流程

编写详细的步骤指南：

```markdown
## Process

Step 1: 分析代码结构
- 识别代码语言和框架
- 理解代码的主要功能

Step 2: 检查代码质量
- 命名规范检查
- 代码复杂度分析
- 潜在 bug 识别

Step 3: 提供改进建议
- 性能优化建议
- 可读性改进
- 最佳实践推荐

Step 4: 生成审查报告
- 按优先级排列问题
- 提供具体的修改示例
```

#### 4. 编写示例

提供清晰的使用示例帮助理解：

```markdown
## Example

### Input
用户: "请审查这段代码"
```javascript
function calc(a,b){
  var result=a+b
  return result
}
```

### Output
**代码审查报告**

🔴 严重问题：
- 缺少参数类型验证

🟡 改进建议：
1. 使用 const 替代 var
2. 添加 JSDoc 注释
3. 改进函数命名

📝 重构后的代码：
```javascript
/**
 * 计算两个数字的和
 * @param {number} a - 第一个数字
 * @param {number} b - 第二个数字
 * @returns {number} 两数之和
 */
function calculateSum(a, b) {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('参数必须是数字类型');
  }
  const result = a + b;
  return result;
}
```
```




## 参考资料

### Skills 相关
- [Continue.dev Skills 文档](https://continue.dev/docs/features/skills)
- [LangChain Agents 文档](https://python.langchain.com/docs/modules/agents/)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

### MCP 相关
- [Model Context Protocol 规范](https://modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [官方 MCP Servers 示例](https://github.com/modelcontextprotocol/servers)

### SubAgent 相关
- [Multi-Agent Systems 设计模式](https://arxiv.org/abs/2308.00352)
- [AutoGen Framework](https://microsoft.github.io/autogen/)
- [CrewAI - Multi-Agent 框架](https://www.crewai.io/)

### 自动化迭代
- [GitOps 实践指南](https://www.gitops.tech/)
- [Continuous Deployment 最佳实践](https://continuousdelivery.com/)
- [AI-Driven Development](https://martinfowler.com/articles/ai-driven-development.html)

### 实践案例
- [GitHub Copilot Workspace](https://github.com/features/copilot)
- [Cursor IDE](https://cursor.sh/)
- [Devin AI](https://www.cognition-labs.com/devin)
