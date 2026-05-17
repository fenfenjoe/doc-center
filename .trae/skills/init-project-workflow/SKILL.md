# 初始化项目工作流

## Description

当用户说要"初始化xxx项目"、"初始化xxx项目文档"时，负责协调整个初始化流程的主Skill。该Skill会：
1. 询问用户项目的git地址
2. 询问用户是否拉取代码到本地
3. 检查本地目录状态，处理冲突
4. 协调其他Skill完成项目拉取、分析和文档生成

## When to Use

- 用户提到"初始化xxx项目"
- 用户提到"初始化xxx项目文档"
- 用户提到"为xxx项目创建文档"
- 用户提到新项目需要初始化

## Input Format

- **项目名称**（必填）：待初始化文档的项目名称
- **项目Git地址**（可选）：项目的远程Git仓库地址
- **项目本地地址**（可选）：项目在本地的存储路径

## Process

### Step 1: 收集项目信息
- 如果用户未提供Git地址，询问用户
- 如果用户未提供本地地址，询问用户是否拉取代码

### Step 2: 检查本地目录状态
- 如果本地目录不存在，创建目录
- 如果本地目录存在但为空，询问用户是否拉取代码
- 如果本地目录存在且有内容：
  - 检查git地址是否匹配
  - 如果不匹配，询问用户哪个是正确的
  - 如果用户选择新的git地址，删除原内容后拉取

### Step 3: 拉取项目代码
- 调用 git-operations Skill 拉取代码

### Step 4: 分析项目
- 调用 project-analyzer Skill 分析项目结构和代码

### Step 5: 生成文档
- 调用 doc-generator Skill 生成文档

## Output Format

生成的文档结构：
```
Projects/{项目名}/
├── README.md          # 项目简介
├── prd/
│   └── README.md      # 需求分析文档
└── design/
    └── README.md      # 设计文档
```

## Dependencies

- git-operations: Git操作Skill
- project-analyzer: 项目分析Skill
- doc-generator: 文档生成Skill

## Scripts

执行脚本：`scripts/init_project_workflow.py`

用法：
```bash
python scripts/init_project_workflow.py <项目名称> [git_url] [local_path]
```
