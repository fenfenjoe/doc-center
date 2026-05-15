# MCP

## 如何写MCP

### 概述

MCP (Model Context Protocol) 是一种标准化协议，用于让 AI 模型与外部工具、数据源和服务进行交互。简单来说，MCP 就像是 AI 的"API 接口规范"，它定义了 AI 如何调用外部功能。

**MCP 的核心价值：**
- 统一的接口标准，降低集成成本
- 安全的权限控制机制
- 可扩展的工具生态系统
- 支持本地和远程服务

**典型应用场景：**
- 文件系统操作（读写文件、搜索代码）
- 数据库查询（SQL 执行、数据分析）
- API 调用（HTTP 请求、第三方服务集成）
- 开发工具集成（Git 操作、构建工具）

### MCP 的基本架构

```
┌─────────────┐
│   AI Model  │
└──────┬──────┘
       │ 通过 MCP 协议通信
       │
┌──────▼──────┐
│ MCP Server  │ (你编写的服务)
└──────┬──────┘
       │
       ├─► Tool 1: 文件操作
       ├─► Tool 2: 数据库查询
       └─► Tool 3: API 调用
```

### 实践步骤

#### 1. 理解 MCP 规范

MCP 定义了三个核心概念：

**Tools（工具）**：AI 可以调用的函数
```json
{
  "name": "read_file",
  "description": "读取文件内容",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "文件路径"
      }
    },
    "required": ["path"]
  }
}
```

**Resources（资源）**：AI 可以访问的数据源
```json
{
  "uri": "file:///project/README.md",
  "name": "项目说明文档",
  "mimeType": "text/markdown"
}
```

**Prompts（提示）**：预定义的提示模板
```json
{
  "name": "code_review",
  "description": "代码审查模板",
  "arguments": [
    {
      "name": "language",
      "description": "编程语言"
    }
  ]
}
```

#### 2. 选择实现方式

MCP 服务可以用多种语言实现：

**Node.js/TypeScript 示例：**
```typescript
import { McpServer } from '@modelcontextprotocol/sdk';

const server = new McpServer({
  name: 'my-mcp-server',
  version: '1.0.0'
});

// 注册工具
server.tool({
  name: 'get_user_info',
  description: '获取用户信息',
  inputSchema: {
    type: 'object',
    properties: {
      userId: { type: 'string' }
    },
    required: ['userId']
  },
  handler: async (input) => {
    // 实现获取用户信息的逻辑
    const userInfo = await fetchUserFromDB(input.userId);
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(userInfo)
      }]
    };
  }
});

server.start();
```

**Python 示例：**
```python
from mcp import MCPServer, Tool

server = MCPServer(name="my-mcp-server")

@server.tool()
async def search_code(query: str, file_pattern: str = "*.py"):
    """在代码库中搜索指定内容"""
    results = []
    # 实现搜索逻辑
    for file in glob.glob(file_pattern, recursive=True):
        with open(file, 'r') as f:
            content = f.read()
            if query in content:
                results.append({
                    'file': file,
                    'matches': content.count(query)
                })
    return results

server.run()
```

#### 3. 定义工具接口

设计清晰的工具接口是关键：

```typescript
// 好的设计：参数明确，职责单一
server.tool({
  name: 'execute_sql_query',
  description: '执行只读 SQL 查询',
  inputSchema: {
    type: 'object',
    properties: {
      query: { 
        type: 'string',
        description: 'SQL 查询语句（仅支持 SELECT）'
      },
      database: { 
        type: 'string',
        description: '数据库名称',
        enum: ['production', 'staging', 'development']
      },
      limit: {
        type: 'number',
        description: '返回结果数量限制',
        default: 100,
        maximum: 1000
      }
    },
    required: ['query', 'database']
  },
  handler: async (input) => {
    // 安全检查：确保只执行 SELECT 语句
    if (!input.query.trim().toLowerCase().startsWith('select')) {
      throw new Error('只允许执行 SELECT 查询');
    }
    
    const results = await executeQuery(
      input.database, 
      input.query,
      input.limit || 100
    );
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2)
      }]
    };
  }
});
```

#### 4. 实现错误处理

```typescript
server.tool({
  name: 'call_external_api',
  description: '调用外部 API',
  inputSchema: {
    type: 'object',
    properties: {
      endpoint: { type: 'string' },
      method: { type: 'string', enum: ['GET', 'POST'] },
      data: { type: 'object' }
    },
    required: ['endpoint', 'method']
  },
  handler: async (input) => {
    try {
      const response = await fetch(input.endpoint, {
        method: input.method,
        headers: { 'Content-Type': 'application/json' },
        body: input.data ? JSON.stringify(input.data) : undefined,
        timeout: 5000 // 5秒超时
      });
      
      if (!response.ok) {
        throw new Error(`API 返回错误: ${response.status}`);
      }
      
      const data = await response.json();
      
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(data)
        }]
      };
    } catch (error) {
      // 返回友好的错误信息
      return {
        content: [{
          type: 'text',
          text: `调用失败: ${error.message}`
        }],
        isError: true
      };
    }
  }
});
```

#### 5. 配置和部署

创建 MCP 配置文件（通常是 `mcp.json` 或在 IDE 配置中）：

```json
{
  "mcpServers": {
    "my-project-tools": {
      "command": "node",
      "args": ["./mcp-server/index.js"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb",
        "API_KEY": "${env:MY_API_KEY}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./project"]
    }
  }
}
```

#### 6. 测试和调试

编写测试用例验证工具功能：

```typescript
import { testMcpTool } from '@modelcontextprotocol/sdk/testing';

describe('MCP Tools', () => {
  it('should fetch user info correctly', async () => {
    const result = await testMcpTool({
      server: myServer,
      toolName: 'get_user_info',
      input: { userId: '12345' }
    });
    
    expect(result.content[0].text).toContain('username');
  });
  
  it('should handle invalid user ID', async () => {
    const result = await testMcpTool({
      server: myServer,
      toolName: 'get_user_info',
      input: { userId: 'invalid' }
    });
    
    expect(result.isError).toBe(true);
  });
});
```

### 完整示例：构建一个项目管理 MCP 服务

```typescript
import { McpServer } from '@modelcontextprotocol/sdk';
import { readFile, writeFile } from 'fs/promises';
import { join } from 'path';

const server = new McpServer({
  name: 'project-manager',
  version: '1.0.0'
});

// 工具1：列出项目任务
server.tool({
  name: 'list_tasks',
  description: '列出项目中的所有任务',
  inputSchema: {
    type: 'object',
    properties: {
      status: {
        type: 'string',
        enum: ['pending', 'in-progress', 'completed', 'all'],
        default: 'all'
      }
    }
  },
  handler: async (input) => {
    const tasksFile = join(process.cwd(), 'tasks.json');
    const tasks = JSON.parse(await readFile(tasksFile, 'utf-8'));
    
    const filtered = input.status === 'all' 
      ? tasks 
      : tasks.filter(t => t.status === input.status);
    
    return {
      content: [{
        type: 'text',
        text: `找到 ${filtered.length} 个任务:\n\n` +
              filtered.map(t => 
                `- [${t.status}] ${t.title} (优先级: ${t.priority})`
              ).join('\n')
      }]
    };
  }
});

// 工具2：创建新任务
server.tool({
  name: 'create_task',
  description: '创建一个新的项目任务',
  inputSchema: {
    type: 'object',
    properties: {
      title: { type: 'string' },
      description: { type: 'string' },
      priority: { 
        type: 'string', 
        enum: ['low', 'medium', 'high'],
        default: 'medium'
      }
    },
    required: ['title']
  },
  handler: async (input) => {
    const tasksFile = join(process.cwd(), 'tasks.json');
    const tasks = JSON.parse(await readFile(tasksFile, 'utf-8'));
    
    const newTask = {
      id: Date.now().toString(),
      title: input.title,
      description: input.description || '',
      priority: input.priority || 'medium',
      status: 'pending',
      createdAt: new Date().toISOString()
    };
    
    tasks.push(newTask);
    await writeFile(tasksFile, JSON.stringify(tasks, null, 2));
    
    return {
      content: [{
        type: 'text',
        text: `✅ 任务创建成功！\n\n` +
              `ID: ${newTask.id}\n` +
              `标题: ${newTask.title}\n` +
              `优先级: ${newTask.priority}`
      }]
    };
  }
});

// 工具3：更新任务状态
server.tool({
  name: 'update_task_status',
  description: '更新任务的状态',
  inputSchema: {
    type: 'object',
    properties: {
      taskId: { type: 'string' },
      status: { 
        type: 'string',
        enum: ['pending', 'in-progress', 'completed']
      }
    },
    required: ['taskId', 'status']
  },
  handler: async (input) => {
    const tasksFile = join(process.cwd(), 'tasks.json');
    const tasks = JSON.parse(await readFile(tasksFile, 'utf-8'));
    
    const task = tasks.find(t => t.id === input.taskId);
    if (!task) {
      throw new Error(`任务 ${input.taskId} 不存在`);
    }
    
    task.status = input.status;
    task.updatedAt = new Date().toISOString();
    
    await writeFile(tasksFile, JSON.stringify(tasks, null, 2));
    
    return {
      content: [{
        type: 'text',
        text: `✅ 任务状态已更新：${task.title} → ${input.status}`
      }]
    };
  }
});

server.start();
```

### Skills vs MCP 的区别

| 维度 | Skills | MCP |
|------|--------|-----|
| **定位** | AI 的"工作流程" | AI 的"工具接口" |
| **内容** | 思维框架、执行步骤 | 具体功能实现 |
| **实现** | Markdown 文档 | 代码（服务端程序） |
| **触发** | 基于描述自动匹配 | AI 主动调用工具 |
| **示例** | 代码审查流程、测试策略 | 文件读写、数据库查询 |

**配合使用示例：**
- **Skill**: "代码审查技能" 定义审查流程
- **MCP**: 提供 `analyze_complexity`、`check_style` 等工具
- **效果**: AI 按照 Skill 的流程，调用 MCP 工具完成审查
