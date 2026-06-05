# Langchain

## 开发环境搭建

1. 安装node.js

```bash
# 安装 nvm（macOS / Linux）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新加载 shell 配置（或重启终端）
source ~/.bashrc   # 如果使用 bash
# 或 source ~/.zshrc

# 安装 Node.js 20 LTS（推荐用于 Agent 开发）
nvm install 20
nvm use 20
nvm alias default 20

# 检查是否安装成功
node --version   # 应输出 v20.x.x
npm --version    # 应输出 10.x.x 或更高
```

2. 安装pnpm（可选）

```bash
# 全局安装 pnpm
npm install -g pnpm

# 验证安装
pnpm --version
```

3. 获取大模型API Key

略

4. 初始化项目

```bash
mkdir my-awesome-agent
cd my-awesome-agent
npm init -y
```

5. 初始化TypeScript配置

```bash
npx tsc --init
```

6. 安装核心依赖

```bash
# 安装LangGraph核心依赖（环境数据暂存）
npm install @langchain/langgraph @langchain/core @langchain/openai

# 安装TypeScript开发依赖
npm install -D typescript ts-node @types/node dotenv
```

7. 编写你的Agent代码

略

8. 调试

（1）使用ts-node快速执行
```bash
# 假设你的Agent入口为index.ts
npx ts-node index.ts
```

（2）使用 LangGraph CLI 和 Studio 获得可视化调试体验

```bash
#安装CLI
npm install -g @langchain/langgraph-cli
#启动服务器
langgraph dev
```

9. 部署（Docker）

（1）使用Express 框架，将Agent封装成一个 Web API，详情略  

（2）编写 Dockerfile  

（3）确保 package.json 中有 build 脚本：  
```json
"scripts": {
  "build": "tsc",
  "start": "node dist/server.js"
}
```

（4）构建容器  
```bash
docker build -t my-agent:latest .
```

（5）运行容器  
```bash
docker run -d --name my-agent \
  -p 3000:3000 \
  -e OPENAI_API_KEY="你的API密钥" \
  my-agent:latest
```

10. 测试API

```bash
curl -X POST http://localhost:3000/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，Agent！"}'
```