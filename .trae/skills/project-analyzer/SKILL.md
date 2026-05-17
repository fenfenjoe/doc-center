# 项目分析

## Description

负责分析项目结构、代码、技术栈的Skill。

## When to Use

- 需要分析项目的技术栈
- 需要检测项目使用的语言和框架
- 需要获取项目结构信息

## Input Format

- **项目路径**（必填）：本地项目路径

## Process

### Step 1: 检测项目语言
- 扫描项目文件扩展名
- 统计各语言文件数量

### Step 2: 检测框架
- 检查package.json（Node.js项目）
- 检查requirements.txt（Python项目）
- 检查pom.xml/build.gradle（Java项目）

### Step 3: 检测数据库
- 搜索数据库相关配置文件
- 检查依赖中的数据库驱动

### Step 4: 获取项目结构
- 生成目录树结构
- 限制深度为3层

## Output Format

JSON格式的分析结果：
```json
{
  "languages": {"Python": 10, "JavaScript": 5},
  "frameworks": ["Django", "React"],
  "databases": ["MySQL", "Redis"],
  "description": "项目描述",
  "structure": ["├── src", "├── tests"]
}
```

## Scripts

执行脚本：`scripts/analyze_project.py`

用法：
```bash
python scripts/analyze_project.py <项目路径>
```
