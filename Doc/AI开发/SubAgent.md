# SubAgent

## 概述

SubAgent（子代理）是一种将复杂任务分解给多个专门化 AI 代理协作完成的架构模式。每个 SubAgent 负责特定领域的工作，类似于团队中不同角色的成员。

**核心理念：**
- 专业化分工：每个 Agent 专注于特定任务
- 协作完成：Agent 之间可以相互调用
- 降低复杂度：大任务拆解为小任务
- 提高准确性：专门化提升质量

## SubAgent 架构模式

```
┌─────────────────┐
│  Master Agent   │ (主协调者)
└────────┬────────┘
         │
    ┌────┼────┬────────┐
    │    │    │        │
┌───▼──┐ │ ┌──▼───┐ ┌─▼────┐
│Code  │ │ │Test  │ │Doc   │
│Agent │ │ │Agent │ │Agent │
└──────┘ │ └──────┘ └──────┘
         │
    ┌────▼────┐
    │Review   │
    │Agent    │
    └─────────┘
```

## 实践示例

### 示例1：代码生成系统

```typescript
// 定义 SubAgent 接口
interface SubAgent {
  name: string;
  role: string;
  execute(task: Task): Promise<Result>;
}

// 代码生成 Agent
class CodeGeneratorAgent implements SubAgent {
  name = 'CodeGenerator';
  role = '根据需求生成代码实现';
  
  async execute(task: Task): Promise<Result> {
    // 调用 AI 生成代码
    const prompt = `
      根据以下需求生成代码：
      ${task.requirements}
      
      要求：
      - 遵循 ${task.language} 最佳实践
      - 添加必要的注释
      - 考虑边界情况
    `;
    
    const code = await callAI(prompt);
    return { code, metadata: { agent: this.name } };
  }
}

// 测试生成 Agent
class TestGeneratorAgent implements SubAgent {
  name = 'TestGenerator';
  role = '为代码生成测试用例';
  
  async execute(task: Task): Promise<Result> {
    const prompt = `
      为以下代码生成完整的测试用例：
      ${task.code}
      
      要求：
      - 覆盖正常情况和边界情况
      - 使用 ${task.testFramework} 框架
      - 测试覆盖率 > 80%
    `;
    
    const tests = await callAI(prompt);
    return { tests, metadata: { agent: this.name } };
  }
}

// 文档生成 Agent
class DocGeneratorAgent implements SubAgent {
  name = 'DocGenerator';
  role = '生成 API 文档';
  
  async execute(task: Task): Promise<Result> {
    const prompt = `
      为以下代码生成 API 文档：
      ${task.code}
      
      要求：
      - 包含函数说明、参数、返回值
      - 提供使用示例
      - Markdown 格式
    `;
    
    const docs = await callAI(prompt);
    return { docs, metadata: { agent: this.name } };
  }
}

// 代码审查 Agent
class CodeReviewAgent implements SubAgent {
  name = 'CodeReviewer';
  role = '审查代码质量并提供改进建议';
  
  async execute(task: Task): Promise<Result> {
    const prompt = `
      审查以下代码：
      ${task.code}
      
      检查：
      - 代码规范
      - 潜在 bug
      - 性能问题
      - 安全隐患
    `;
    
    const review = await callAI(prompt);
    return { review, metadata: { agent: this.name } };
  }
}

// 主协调 Agent
class MasterAgent {
  private agents: Map<string, SubAgent>;
  
  constructor() {
    this.agents = new Map([
      ['code', new CodeGeneratorAgent()],
      ['test', new TestGeneratorAgent()],
      ['doc', new DocGeneratorAgent()],
      ['review', new CodeReviewAgent()]
    ]);
  }
  
  async executeWorkflow(requirements: string): Promise<ProjectResult> {
    console.log('🚀 开始执行开发流程...\n');
    
    // Step 1: 生成代码
    console.log('📝 Step 1: 生成代码实现');
    const codeResult = await this.agents.get('code')!.execute({
      requirements,
      language: 'TypeScript'
    });
    console.log('✅ 代码生成完成\n');
    
    // Step 2: 并行生成测试和文档
    console.log('⚡ Step 2: 并行生成测试和文档');
    const [testResult, docResult] = await Promise.all([
      this.agents.get('test')!.execute({
        code: codeResult.code,
        testFramework: 'Jest'
      }),
      this.agents.get('doc')!.execute({
        code: codeResult.code
      })
    ]);
    console.log('✅ 测试和文档生成完成\n');
    
    // Step 3: 代码审查
    console.log('🔍 Step 3: 执行代码审查');
    const reviewResult = await this.agents.get('review')!.execute({
      code: codeResult.code
    });
    console.log('✅ 审查完成\n');
    
    // Step 4: 如果有严重问题，重新生成
    if (reviewResult.review.severity === 'high') {
      console.log('⚠️  发现严重问题，重新生成...');
      return this.executeWorkflow(
        requirements + '\n改进建议：' + reviewResult.review.suggestions
      );
    }
    
    return {
      code: codeResult.code,
      tests: testResult.tests,
      docs: docResult.docs,
      review: reviewResult.review
    };
  }
}

// 使用示例
const master = new MasterAgent();
const result = await master.executeWorkflow(`
  创建一个用户认证模块，包含：
  - 用户注册功能
  - 登录验证
  - JWT token 生成
  - 密码加密存储
`);

console.log('🎉 开发完成！');
console.log('代码:', result.code);
console.log('测试:', result.tests);
console.log('文档:', result.docs);
console.log('审查:', result.review);
```

### 示例2：数据分析系统

```python
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class AnalysisTask:
    data: Any
    task_type: str
    parameters: Dict[str, Any]

class SubAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
    
    async def execute(self, task: AnalysisTask) -> Dict[str, Any]:
        raise NotImplementedError

# 数据清洗 Agent
class DataCleaningAgent(SubAgent):
    def __init__(self):
        super().__init__('DataCleaner', '数据清洗和预处理')
    
    async def execute(self, task: AnalysisTask) -> Dict[str, Any]:
        print(f"🧹 [{self.name}] 开始清洗数据...")
        
        # 调用 AI 分析数据质量
        prompt = f"""
        分析以下数据的质量问题：
        {task.data[:100]}...
        
        识别：
        - 缺失值
        - 异常值
        - 重复数据
        - 数据类型问题
        
        并提供清洗方案
        """
        
        cleaning_plan = await call_ai(prompt)
        cleaned_data = apply_cleaning(task.data, cleaning_plan)
        
        return {
            'data': cleaned_data,
            'report': cleaning_plan,
            'agent': self.name
        }

# 统计分析 Agent
class StatisticalAnalysisAgent(SubAgent):
    def __init__(self):
        super().__init__('StatAnalyzer', '统计分析')
    
    async def execute(self, task: AnalysisTask) -> Dict[str, Any]:
        print(f"📊 [{self.name}] 执行统计分析...")
        
        prompt = f"""
        对数据进行统计分析：
        {task.data}
        
        计算：
        - 描述性统计（均值、中位数、标准差）
        - 分布特征
        - 相关性分析
        - 异常检测
        """
        
        analysis = await call_ai(prompt)
        
        return {
            'statistics': analysis,
            'agent': self.name
        }

# 可视化 Agent
class VisualizationAgent(SubAgent):
    def __init__(self):
        super().__init__('Visualizer', '数据可视化')
    
    async def execute(self, task: AnalysisTask) -> Dict[str, Any]:
        print(f"📈 [{self.name}] 生成可视化...")
        
        prompt = f"""
        根据统计分析结果生成可视化方案：
        {task.parameters['statistics']}
        
        生成：
        - 合适的图表类型选择
        - Python Matplotlib/Seaborn 代码
        - 图表配置（标题、标签、样式）
        """
        
        viz_code = await call_ai(prompt)
        charts = execute_viz_code(viz_code, task.data)
        
        return {
            'charts': charts,
            'code': viz_code,
            'agent': self.name
        }

# 洞察生成 Agent
class InsightGeneratorAgent(SubAgent):
    def __init__(self):
        super().__init__('InsightGenerator', '生成业务洞察')
    
    async def execute(self, task: AnalysisTask) -> Dict[str, Any]:
        print(f"💡 [{self.name}] 生成业务洞察...")
        
        prompt = f"""
        基于以下分析结果生成业务洞察：
        
        统计分析：{task.parameters['statistics']}
        可视化：{task.parameters['charts']}
        
        提供：
        - 关键发现
        - 趋势分析
        - 异常解释
        - 行动建议
        """
        
        insights = await call_ai(prompt)
        
        return {
            'insights': insights,
            'agent': self.name
        }

# 主协调 Agent
class DataAnalysisMaster:
    def __init__(self):
        self.agents = {
            'cleaner': DataCleaningAgent(),
            'analyzer': StatisticalAnalysisAgent(),
            'visualizer': VisualizationAgent(),
            'insights': InsightGeneratorAgent()
        }
    
    async def analyze(self, raw_data: Any) -> Dict[str, Any]:
        print("🚀 开始数据分析流程\n")
        
        # Step 1: 数据清洗
        clean_result = await self.agents['cleaner'].execute(
            AnalysisTask(data=raw_data, task_type='clean', parameters={})
        )
        
        # Step 2: 统计分析
        stat_result = await self.agents['analyzer'].execute(
            AnalysisTask(
                data=clean_result['data'],
                task_type='analyze',
                parameters={}
            )
        )
        
        # Step 3: 可视化
        viz_result = await self.agents['visualizer'].execute(
            AnalysisTask(
                data=clean_result['data'],
                task_type='visualize',
                parameters={'statistics': stat_result['statistics']}
            )
        )
        
        # Step 4: 生成洞察
        insight_result = await self.agents['insights'].execute(
            AnalysisTask(
                data=None,
                task_type='insights',
                parameters={
                    'statistics': stat_result['statistics'],
                    'charts': viz_result['charts']
                }
            )
        )
        
        print("\n✅ 分析完成！")
        
        return {
            'cleaned_data': clean_result['data'],
            'statistics': stat_result['statistics'],
            'visualizations': viz_result['charts'],
            'insights': insight_result['insights']
        }

# 使用示例
master = DataAnalysisMaster()
result = await master.analyze(sales_data)
print("\n📋 分析报告：")
print(result['insights'])
```

## SubAgent 设计最佳实践

### 1. 合理划分职责

```typescript
// ❌ 不好：职责不清
class DoEverythingAgent {
  async execute(task) {
    const code = await generateCode(task);
    const tests = await generateTests(code);
    const docs = await generateDocs(code);
    const review = await reviewCode(code);
    return { code, tests, docs, review };
  }
}

// ✅ 好：职责单一
class CodeAgent { /* 只负责生成代码 */ }
class TestAgent { /* 只负责生成测试 */ }
class DocAgent { /* 只负责生成文档 */ }
class ReviewAgent { /* 只负责审查 */ }
```

### 2. 定义清晰的通信协议

```typescript
// 标准化的消息格式
interface AgentMessage {
  from: string;        // 发送者
  to: string;          // 接收者
  type: 'request' | 'response' | 'notification';
  payload: any;        // 数据
  metadata: {
    timestamp: string;
    taskId: string;
    priority: 'high' | 'medium' | 'low';
  };
}

class Agent {
  async send(message: AgentMessage): Promise<void> {
    // 发送消息到其他 Agent
  }
  
  async receive(message: AgentMessage): Promise<AgentMessage> {
    // 处理接收到的消息
  }
}
```

### 3. 实现错误处理和重试

```typescript
class ResilientAgent extends SubAgent {
  private maxRetries = 3;
  
  async execute(task: Task): Promise<Result> {
    let lastError: Error;
    
    for (let i = 0; i < this.maxRetries; i++) {
      try {
        return await this.doExecute(task);
      } catch (error) {
        console.log(`❌ 尝试 ${i + 1} 失败: ${error.message}`);
        lastError = error;
        
        // 指数退避
        await sleep(Math.pow(2, i) * 1000);
      }
    }
    
    throw new Error(
      `Agent ${this.name} 失败 ${this.maxRetries} 次: ${lastError.message}`
    );
  }
  
  protected async doExecute(task: Task): Promise<Result> {
    // 实际执行逻辑
  }
}
```

### 4. 添加监控和日志

```typescript
class MonitoredAgent extends SubAgent {
  private metrics = {
    totalExecutions: 0,
    successCount: 0,
    failureCount: 0,
    avgExecutionTime: 0
  };
  
  async execute(task: Task): Promise<Result> {
    const startTime = Date.now();
    this.metrics.totalExecutions++;
    
    try {
      const result = await super.execute(task);
      
      this.metrics.successCount++;
      const executionTime = Date.now() - startTime;
      this.updateAvgTime(executionTime);
      
      console.log(`✅ [${this.name}] 完成 (${executionTime}ms)`);
      
      return result;
    } catch (error) {
      this.metrics.failureCount++;
      console.error(`❌ [${this.name}] 失败: ${error.message}`);
      throw error;
    }
  }
  
  getMetrics() {
    return {
      ...this.metrics,
      successRate: this.metrics.successCount / this.metrics.totalExecutions
    };
  }
}
```
