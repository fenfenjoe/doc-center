#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初始化项目工作流主脚本
负责协调整个初始化流程
"""

import os
import sys
import json
import subprocess
from pathlib import Path


class InitProjectWorkflow:
    """初始化项目工作流"""
    
    def __init__(self, project_name, git_url=None, local_path=None):
        self.project_name = project_name
        self.git_url = git_url
        self.local_path = local_path
        
        # 获取项目根目录
        self.script_dir = Path(__file__).parent.parent
        self.config_path = self.script_dir / 'config' / 'config.json'
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.project_base = Path(self.config['project_base_path']).resolve()
        self.sample_template = Path(self.config['sample_template_path']).resolve()
        
        # 确保Projects目录存在
        self.project_base.mkdir(parents=True, exist_ok=True)
    
    def run(self):
        """执行完整工作流"""
        print(f"开始初始化项目: {self.project_name}")
        
        # Step 1: 收集项目信息
        self._collect_project_info()
        
        # Step 2: 检查本地目录状态
        self._check_local_directory()
        
        # Step 3: 拉取项目代码（如果需要）
        if self._need_pull_code():
            self._pull_project_code()
        
        # Step 4: 分析项目
        analysis_result = self._analyze_project()
        
        # Step 5: 生成文档
        self._generate_documents(analysis_result)
        
        print(f"\n项目 {self.project_name} 初始化完成！")
        print(f"文档位置: {self.local_path}")
        
        return {
            'status': 'success',
            'project_name': self.project_name,
            'project_path': str(self.local_path),
            'git_url': self.git_url
        }
    
    def _collect_project_info(self):
        """收集项目信息"""
        if not self.git_url:
            print("请提供项目的Git地址:")
            self.git_url = input().strip()
        
        if not self.local_path:
            self.local_path = self.project_base / self.project_name
        
        print(f"项目名称: {self.project_name}")
        print(f"Git地址: {self.git_url}")
        print(f"本地路径: {self.local_path}")
    
    def _check_local_directory(self):
        """检查本地目录状态"""
        local_path = Path(self.local_path)
        
        if not local_path.exists():
            print(f"本地目录不存在，将创建: {local_path}")
            local_path.mkdir(parents=True, exist_ok=True)
            return
        
        # 检查目录是否为空
        files = list(local_path.iterdir())
        if not files:
            print(f"本地目录为空: {local_path}")
            return
        
        # 目录有内容，检查git地址
        print(f"本地目录已有内容: {local_path}")
        existing_git_url = self._get_git_remote_url(local_path)
        
        if existing_git_url and existing_git_url != self.git_url:
            print(f"\n警告: 本地目录的Git地址与提供的不一致！")
            print(f"  本地Git: {existing_git_url}")
            print(f"  提供Git:   {self.git_url}")
            print(f"\n哪个是正确的？")
            print(f"  1. 使用本地已有的Git地址")
            print(f"  2. 使用新的Git地址（将覆盖本地内容）")
            
            choice = input("请选择 (1/2): ").strip()
            
            if choice == '1':
                self.git_url = existing_git_url
                print(f"使用本地Git地址: {self.git_url}")
            elif choice == '2':
                print(f"将删除本地内容并拉取新项目...")
                self._clear_directory(local_path)
            else:
                print("无效选择，使用新的Git地址")
                self._clear_directory(local_path)
        else:
            print("本地目录Git地址匹配，无需操作")
    
    def _get_git_remote_url(self, path):
        """获取目录的git远程地址"""
        try:
            result = subprocess.run(
                ['git', '-C', str(path), 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None
    
    def _clear_directory(self, path):
        """清空目录"""
        import shutil
        path = Path(path)
        if path.exists():
            for item in path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            print(f"已清空目录: {path}")
    
    def _need_pull_code(self):
        """判断是否需要拉取代码"""
        local_path = Path(self.local_path)
        if not local_path.exists():
            return True
        
        files = list(local_path.iterdir())
        if not files:
            return True
        
        # 检查是否有.git目录
        git_dir = local_path / '.git'
        if not git_dir.exists():
            return True
        
        return False
    
    def _pull_project_code(self):
        """拉取项目代码"""
        print(f"\n开始拉取项目代码...")
        print(f"Git地址: {self.git_url}")
        print(f"目标路径: {self.local_path}")
        
        local_path = Path(self.local_path)
        local_path.mkdir(parents=True, exist_ok=True)
        
        try:
            result = subprocess.run(
                ['git', 'clone', self.git_url, str(local_path)],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(f"项目代码拉取成功！")
            else:
                print(f"Git拉取失败: {result.stderr}")
                sys.exit(1)
        except Exception as e:
            print(f"Git操作失败: {e}")
            sys.exit(1)
    
    def _analyze_project(self):
        """分析项目"""
        print(f"\n开始分析项目: {self.local_path}")
        
        # 调用project-analyzer skill
        analyzer_script = self.script_dir.parent / 'project-analyzer' / 'scripts' / 'analyze_project.py'
        
        if analyzer_script.exists():
            result = subprocess.run(
                ['python', str(analyzer_script), str(self.local_path)],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                print(f"项目分析失败: {result.stderr}")
        
        # 如果analyzer不存在，使用简单分析
        return self._simple_analyze()
    
    def _simple_analyze(self):
        """简单项目分析"""
        local_path = Path(self.local_path)
        
        # 检测项目语言
        languages = {}
        for ext in ['*.py', '*.js', '*.ts', '*.java', '*.go', '*.rb', '*.php']:
            files = list(local_path.rglob(ext))
            if files:
                lang_name = ext[2:].upper()
                if lang_name == 'PY':
                    lang_name = 'Python'
                elif lang_name == 'JS':
                    lang_name = 'JavaScript'
                elif lang_name == 'TS':
                    lang_name = 'TypeScript'
                elif lang_name == 'JAVA':
                    lang_name = 'Java'
                elif lang_name == 'GO':
                    lang_name = 'Go'
                languages[lang_name] = len(files)
        
        # 检测框架
        frameworks = []
        package_json = local_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    if 'react' in deps:
                        frameworks.append('React')
                    if 'vue' in deps:
                        frameworks.append('Vue.js')
                    if 'angular' in deps:
                        frameworks.append('Angular')
                    if 'express' in deps:
                        frameworks.append('Express')
            except:
                pass
        
        requirements_txt = local_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if 'django' in content:
                        frameworks.append('Django')
                    if 'flask' in content:
                        frameworks.append('Flask')
                    if 'fastapi' in content:
                        frameworks.append('FastAPI')
            except:
                pass
        
        pom_xml = local_path / 'pom.xml'
        if pom_xml.exists():
            frameworks.append('Maven')
        
        build_gradle = local_path / 'build.gradle'
        if build_gradle.exists():
            frameworks.append('Gradle')
        
        # 检测数据库
        databases = []
        for db in ['mysql', 'postgresql', 'sqlite', 'mongodb', 'redis']:
            for f in local_path.rglob(f'*{db}*'):
                if f.is_file():
                    databases.append(db.upper())
                    break
        
        return {
            'languages': languages,
            'frameworks': frameworks,
            'databases': databases,
            'description': f'{self.project_name} 项目',
            'structure': self._get_project_structure(local_path)
        }
    
    def _get_project_structure(self, path, prefix='', is_last=True, max_depth=3, current_depth=0):
        """获取项目结构"""
        if current_depth >= max_depth:
            return []
        
        structure = []
        items = sorted([p for p in path.iterdir() if not p.name.startswith('.')])
        
        for i, item in enumerate(items):
            is_last_item = (i == len(items) - 1)
            connector = '└── ' if is_last_item else '├── '
            structure.append(f'{prefix}{connector}{item.name}')
            
            if item.is_dir():
                extension = '    ' if is_last_item else '│   '
                sub_structure = self._get_project_structure(
                    item, prefix + extension, is_last_item, max_depth, current_depth + 1
                )
                structure.extend(sub_structure)
        
        return structure
    
    def _generate_documents(self, analysis_result):
        """生成文档"""
        print(f"\n开始生成文档...")
        
        # 调用doc-generator skill
        generator_script = self.script_dir.parent / 'doc-generator' / 'scripts' / 'generate_docs.py'
        
        if generator_script.exists():
            result = subprocess.run(
                [
                    'python', str(generator_script),
                    self.project_name,
                    str(self.local_path),
                    json.dumps(analysis_result)
                ],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                print(result.stdout)
                return
            else:
                print(f"文档生成失败: {result.stderr}")
        
        # 如果generator不存在，使用简单生成
        self._simple_generate_docs(analysis_result)
    
    def _simple_generate_docs(self, analysis_result):
        """简单文档生成"""
        local_path = Path(self.local_path)
        
        # 创建文档目录
        prd_dir = local_path / 'prd'
        design_dir = local_path / 'design'
        prd_dir.mkdir(exist_ok=True)
        design_dir.mkdir(exist_ok=True)
        
        # 生成README.md
        readme_content = self._generate_readme(analysis_result)
        (local_path / 'README.md').write_text(readme_content, encoding='utf-8')
        print(f"生成 README.md")
        
        # 生成prd/README.md
        prd_content = self._generate_prd(analysis_result)
        (prd_dir / 'README.md').write_text(prd_content, encoding='utf-8')
        print(f"生成 prd/README.md")
        
        # 生成design/README.md
        design_content = self._generate_design(analysis_result)
        (design_dir / 'README.md').write_text(design_content, encoding='utf-8')
        print(f"生成 design/README.md")
    
    def _generate_readme(self, analysis_result):
        """生成项目简介"""
        languages = analysis_result.get('languages', {})
        frameworks = analysis_result.get('frameworks', [])
        databases = analysis_result.get('databases', [])
        structure = analysis_result.get('structure', [])
        
        lang_str = ', '.join(languages.keys()) if languages else '未知'
        framework_str = ', '.join(frameworks) if frameworks else '未知'
        db_str = ', '.join(databases) if databases else '未知'
        
        structure_str = '\n'.join(structure) if structure else '无'
        
        return f"""# {self.project_name}

## 项目简介

{analysis_result.get('description', f'{self.project_name} 项目')}

## 技术栈

- **编程语言**: {lang_str}
- **框架**: {framework_str}
- **数据库**: {db_str}

## 项目结构

```
{structure_str}
```

## 快速开始

### 环境要求

- Python 3.8+
- Git

### 安装依赖

```bash
# 根据项目类型安装依赖
"""

    def _generate_prd(self, analysis_result):
        """生成需求文档"""
        return f"""# {self.project_name} - 需求分析文档

## 项目背景

{analysis_result.get('description', f'{self.project_name} 项目')}

## 功能需求

### 核心功能

待补充...

### 辅助功能

待补充...

## 非功能需求

### 性能要求

待补充...

### 安全要求

待补充...

## 接口需求

待补充...
"""

    def _generate_design(self, analysis_result):
        """生成设计文档"""
        languages = analysis_result.get('languages', {})
        frameworks = analysis_result.get('frameworks', [])
        databases = analysis_result.get('databases', [])
        
        lang_str = ', '.join(languages.keys()) if languages else '未知'
        framework_str = ', '.join(frameworks) if frameworks else '未知'
        db_str = ', '.join(databases) if databases else '未知'
        
        return f"""# {self.project_name} - 设计文档

## 架构设计

### 技术栈

- **编程语言**: {lang_str}
- **框架**: {framework_str}
- **数据库**: {db_str}

### 系统架构

待补充...

## 模块设计

### 核心模块

待补充...

## 数据库设计

待补充...

## 接口设计

待补充...
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python init_project_workflow.py <项目名称> [git_url] [local_path]")
        sys.exit(1)
    
    project_name = sys.argv[1]
    git_url = sys.argv[2] if len(sys.argv) > 2 else None
    local_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    workflow = InitProjectWorkflow(project_name, git_url, local_path)
    result = workflow.run()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
