# 文档生成

## Description

负责根据项目分析结果生成项目文档的Skill。按照/Projects/sample的目录结构生成文档。

## When to Use

- 需要为项目生成概述文档
- 需要为项目生成需求分析文档
- 需要为项目生成设计文档

## Input Format

- **项目名称**（必填）：项目名称
- **项目路径**（必填）：本地项目路径
- **分析结果**（必填）：项目分析结果的JSON字符串

## Process

### Step 1: 创建文档目录
- 在/Projects/{项目名}/下创建目录
- 创建prd/和design/子目录

### Step 2: 生成README.md
- 项目简介
- 技术栈信息
- 项目结构
- 快速开始指南

### Step 3: 生成prd/README.md
- 项目背景
- 功能需求
- 非功能需求
- 接口需求

### Step 4: 生成design/README.md
- 架构设计
- 技术栈
- 模块设计
- 数据库设计

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

## Scripts

执行脚本：`scripts/generate_docs.py`

用法：
```bash
python scripts/generate_docs.py <项目名称> <项目路径> <分析结果JSON>
```
