#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档生成脚本
负责根据项目分析结果生成项目文档
"""

import os
import sys
import json
from pathlib import Path


class DocGenerator:
    """文档生成器"""
    
    def __init__(self, project_name, project_path, analysis_result):
        self.project_name = project_name
        self.project_path = Path(project_path)
        self.analysis_result = analysis_result
        
        # 文档输出路径
        self.doc_base = self.project_path
        self.prd_dir = self.doc_base / 'prd'
        self.design_dir = self.doc_base / 'design'
    
    def generate(self):
        """生成所有文档"""
        # 创建目录
        self.prd_dir.mkdir(parents=True, exist_ok=True)
        self.design_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成文档
        self._generate_readme()
        self._generate_prd()
        self._generate_design()
        
        return {
            'status': 'success',
            'project_name': self.project_name,
            'doc_path': str(self.doc_base),
            'generated_files': [
                str(self.doc_base / 'README.md'),
                str(self.prd_dir / 'README.md'),
                str(self.design_dir / 'README.md')
            ]
        }
    
    def _generate_readme(self):
        """生成项目简介"""
        languages = self.analysis_result.get('languages', {})
        frameworks = self.analysis_result.get('frameworks', [])
        databases = self.analysis_result.get('databases', [])
        build_tools = self.analysis_result.get('build_tools', [])
        structure = self.analysis_result.get('structure', [])
        description = self.analysis_result.get('description', f'{self.project_name} 项目')
        
        lang_str = ', '.join(languages.keys()) if languages else '待分析'
        framework_str = ', '.join(frameworks) if frameworks else '待分析'
        db_str = ', '.join(databases) if databases else '待分析'
        tools_str = ', '.join(build_tools) if build_tools else '待分析'
        
        structure_str = '\n'.join([f'    {line}' for line in structure]) if structure else '待分析'
        
        content = f"""# {self.project_name}

## 项目简介

{description}

## 技术栈

- **编程语言**: {lang_str}
- **框架**: {framework_str}
- **数据库**: {db_str}
- **构建工具**: {tools_str}

## 项目结构

```
{structure_str}
```

## 快速开始

### 环境要求

根据项目技术栈安装相应环境。

### 安装依赖

```bash
# 根据项目类型安装依赖
# Python项目: pip install -r requirements.txt
# Node.js项目: npm install
# Java项目: mvn install
```

### 运行项目

```bash
# 根据项目类型运行
# Python项目: python main.py
# Node.js项目: npm start
# Java项目: mvn spring-boot:run
```

## 项目信息

- **项目名称**: {self.project_name}
- **项目路径**: {self.project_path}
"""
        
        readme_path = self.doc_base / 'README.md'
        readme_path.write_text(content, encoding='utf-8')
        print(f"已生成: {readme_path}")
    
    def _generate_prd(self):
        """生成需求分析文档"""
        languages = self.analysis_result.get('languages', {})
        frameworks = self.analysis_result.get('frameworks', [])
        databases = self.analysis_result.get('databases', [])
        description = self.analysis_result.get('description', f'{self.project_name} 项目')
        
        lang_str = ', '.join(languages.keys()) if languages else '待分析'
        framework_str = ', '.join(frameworks) if frameworks else '待分析'
        db_str = ', '.join(databases) if databases else '待分析'
        
        content = f"""# {self.project_name} - 需求分析文档

## 项目背景

{description}

## 技术栈概述

- **编程语言**: {lang_str}
- **框架**: {framework_str}
- **数据库**: {db_str}

## 功能需求

### 核心功能

> 待补充：根据项目代码分析，识别核心功能模块

### 辅助功能

> 待补充：根据项目代码分析，识别辅助功能模块

### 用户角色

> 待补充：定义系统的用户角色和权限

## 非功能需求

### 性能要求

> 待补充：定义系统的性能指标

### 安全要求

> 待补充：定义系统的安全要求

### 可用性要求

> 待补充：定义系统的可用性要求

## 接口需求

### 外部接口

> 待补充：定义系统与外部的接口

### 内部接口

> 待补充：定义系统内部的接口

## 数据需求

### 数据存储

> 待补充：定义数据存储需求

### 数据流

> 待补充：定义数据流转需求

## 约束条件

### 技术约束

> 待补充：定义技术层面的约束

### 业务约束

> 待补充：定义业务层面的约束
"""
        
        prd_path = self.prd_dir / 'README.md'
        prd_path.write_text(content, encoding='utf-8')
        print(f"已生成: {prd_path}")
    
    def _generate_design(self):
        """生成设计文档"""
        languages = self.analysis_result.get('languages', {})
        frameworks = self.analysis_result.get('frameworks', [])
        databases = self.analysis_result.get('databases', [])
        build_tools = self.analysis_result.get('build_tools', [])
        description = self.analysis_result.get('description', f'{self.project_name} 项目')
        
        lang_str = ', '.join(languages.keys()) if languages else '待分析'
        framework_str = ', '.join(frameworks) if frameworks else '待分析'
        db_str = ', '.join(databases) if databases else '待分析'
        tools_str = ', '.join(build_tools) if build_tools else '待分析'
        
        content = f"""# {self.project_name} - 设计文档

## 架构设计

### 技术栈

- **编程语言**: {lang_str}
- **框架**: {framework_str}
- **数据库**: {db_str}
- **构建工具**: {tools_str}

### 系统架构

> 待补充：根据项目代码分析，绘制系统架构图

### 架构模式

> 待补充：定义系统采用的架构模式（MVC、微服务等）

## 模块设计

### 核心模块

> 待补充：根据项目代码分析，识别核心模块

### 模块关系

> 待补充：定义模块之间的依赖关系

## 数据库设计

### 数据模型

> 待补充：根据项目代码分析，识别数据模型

### 表结构

> 待补充：定义数据库表结构

## 接口设计

### API设计

> 待补充：定义系统API接口

### 接口规范

> 待补充：定义接口规范（RESTful、GraphQL等）

## 部署设计

### 部署架构

> 待补充：定义系统部署架构

### 环境配置

> 待补充：定义各环境配置

## 安全设计

### 认证授权

> 待补充：定义认证授权方案

### 数据安全

> 待补充：定义数据安全措施
"""
        
        design_path = self.design_dir / 'README.md'
        design_path.write_text(content, encoding='utf-8')
        print(f"已生成: {design_path}")


def main():
    if len(sys.argv) < 4:
        print("用法: python generate_docs.py <项目名称> <项目路径> <分析结果JSON>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    project_path = sys.argv[2]
    analysis_json = sys.argv[3]
    
    try:
        analysis_result = json.loads(analysis_json)
    except json.JSONDecodeError as e:
        print(f"分析结果JSON解析失败: {e}")
        sys.exit(1)
    
    generator = DocGenerator(project_name, project_path, analysis_result)
    result = generator.generate()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
