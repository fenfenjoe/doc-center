#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
项目分析脚本
负责分析项目结构、技术栈等
"""

import os
import sys
import json
from pathlib import Path


class ProjectAnalyzer:
    """项目分析器"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        
        # 语言扩展名映射
        self.language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'JavaScript (React)',
            '.tsx': 'TypeScript (React)',
            '.java': 'Java',
            '.kt': 'Kotlin',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.swift': 'Swift',
            '.rs': 'Rust',
            '.vue': 'Vue',
            '.html': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sql': 'SQL',
        }
        
        # 框架检测规则
        self.framework_rules = {
            'React': ['react', 'react-dom'],
            'Vue.js': ['vue'],
            'Angular': ['@angular/core'],
            'Next.js': ['next'],
            'Nuxt.js': ['nuxt'],
            'Express': ['express'],
            'Django': ['django'],
            'Flask': ['flask'],
            'FastAPI': ['fastapi'],
            'Spring Boot': ['spring-boot'],
            'Rails': ['rails'],
            'Laravel': ['laravel'],
        }
        
        # 数据库检测规则
        self.database_rules = {
            'MySQL': ['mysql', 'pymysql', 'mysqlclient'],
            'PostgreSQL': ['postgresql', 'psycopg2', 'pg'],
            'SQLite': ['sqlite', 'sqlite3'],
            'MongoDB': ['mongodb', 'mongoengine', 'pymongo'],
            'Redis': ['redis'],
            'Elasticsearch': ['elasticsearch'],
        }
    
    def analyze(self):
        """执行完整分析"""
        if not self.project_path.exists():
            return {
                'status': 'error',
                'message': f'项目路径不存在: {self.project_path}'
            }
        
        result = {
            'status': 'success',
            'project_name': self.project_path.name,
            'project_path': str(self.project_path),
            'languages': self._detect_languages(),
            'frameworks': self._detect_frameworks(),
            'databases': self._detect_databases(),
            'build_tools': self._detect_build_tools(),
            'structure': self._get_project_structure(),
            'architecture': self._analyze_architecture(),
            'description': self._generate_description()
        }
        
        return result
    
    def _detect_languages(self):
        """检测项目语言"""
        languages = {}
        
        for ext, lang_name in self.language_map.items():
            files = list(self.project_path.rglob(f'*{ext}'))
            # 过滤掉node_modules、.git等目录
            files = [f for f in files if not self._is_ignored_path(f)]
            if files:
                languages[lang_name] = len(files)
        
        return languages
    
    def _detect_frameworks(self):
        """检测项目框架"""
        frameworks = []
        
        # 检查package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    dep_names = set(deps.keys())
                    
                    for framework, keywords in self.framework_rules.items():
                        if any(kw in dep_names for kw in keywords):
                            frameworks.append(framework)
            except:
                pass
        
        # 检查requirements.txt
        requirements_txt = self.project_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    for framework, keywords in self.framework_rules.items():
                        if any(kw.lower() in content for kw in keywords):
                            if framework not in frameworks:
                                frameworks.append(framework)
            except:
                pass
        
        # 检查pom.xml
        pom_xml = self.project_path / 'pom.xml'
        if pom_xml.exists():
            frameworks.append('Maven')
            try:
                with open(pom_xml, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if 'spring-boot' in content:
                        frameworks.append('Spring Boot')
            except:
                pass
        
        # 检查build.gradle
        build_gradle = self.project_path / 'build.gradle'
        if build_gradle.exists():
            frameworks.append('Gradle')
        
        return frameworks
    
    def _detect_databases(self):
        """检测数据库"""
        databases = []
        
        # 检查package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    dep_names = set(deps.keys())
                    
                    for db, keywords in self.database_rules.items():
                        if any(kw in dep_names for kw in keywords):
                            databases.append(db)
            except:
                pass
        
        # 检查requirements.txt
        requirements_txt = self.project_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    for db, keywords in self.database_rules.items():
                        if any(kw.lower() in content for kw in keywords):
                            if db not in databases:
                                databases.append(db)
            except:
                pass
        
        # 搜索配置文件
        config_patterns = [
            'database.yml', 'database.yaml', 'db.yml', 'db.yaml',
            'database.json', 'db.json', 'database.ini', 'db.ini',
            '.env', 'config.py', 'settings.py', 'application.yml',
            'application.yaml', 'application.properties'
        ]
        
        for pattern in config_patterns:
            for config_file in self.project_path.rglob(pattern):
                if self._is_ignored_path(config_file):
                    continue
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for db, keywords in self.database_rules.items():
                            if any(kw.lower() in content for kw in keywords):
                                if db not in databases:
                                    databases.append(db)
                except:
                    pass
        
        return databases
    
    def _detect_build_tools(self):
        """检测构建工具"""
        tools = []
        
        if (self.project_path / 'package.json').exists():
            tools.append('npm')
            if (self.project_path / 'yarn.lock').exists():
                tools.append('yarn')
            if (self.project_path / 'pnpm-lock.yaml').exists():
                tools.append('pnpm')
        
        if (self.project_path / 'pom.xml').exists():
            tools.append('Maven')
        
        if (self.project_path / 'build.gradle').exists():
            tools.append('Gradle')
        
        if (self.project_path / 'requirements.txt').exists():
            tools.append('pip')
        
        if (self.project_path / 'Pipfile').exists():
            tools.append('Pipenv')
        
        if (self.project_path / 'poetry.lock').exists():
            tools.append('Poetry')
        
        if (self.project_path / 'Makefile').exists():
            tools.append('Make')
        
        if (self.project_path / 'CMakeLists.txt').exists():
            tools.append('CMake')
        
        if (self.project_path / 'Dockerfile').exists():
            tools.append('Docker')
        
        return tools
    
    def _get_project_structure(self, max_depth=3, current_depth=0):
        """获取项目结构"""
        if current_depth >= max_depth:
            return []
        
        structure = []
        try:
            items = sorted([
                p for p in self.project_path.iterdir()
                if not p.name.startswith('.') and not self._is_ignored_path(p)
            ])
        except PermissionError:
            return []
        
        for i, item in enumerate(items):
            is_last = (i == len(items) - 1)
            connector = '└── ' if is_last else '├── '
            structure.append(f'{connector}{item.name}')
            
            if item.is_dir():
                extension = '    ' if is_last else '│   '
                # 临时改变project_path来获取子目录结构
                old_path = self.project_path
                self.project_path = item
                sub_structure = self._get_project_structure(max_depth, current_depth + 1)
                self.project_path = old_path
                
                for line in sub_structure:
                    structure.append(f'{extension}{line}')
        
        return structure
    
    def _generate_description(self):
        """生成项目描述"""
        languages = list(self._detect_languages().keys())
        frameworks = self._detect_frameworks()
        
        if frameworks:
            return f'基于 {", ".join(frameworks)} 的 {", ".join(languages)} 项目'
        elif languages:
            return f'{", ".join(languages)} 项目'
        else:
            return f'{self.project_path.name} 项目'
    
    def _analyze_architecture(self):
        """分析项目架构：主入口、核心模块、数据模型、依赖关系"""
        architecture = {
            'main_entry': self._find_main_entry(),
            'core_modules': self._find_core_modules(),
            'data_models': self._find_data_models(),
            'dependencies': self._analyze_dependencies()
        }
        return architecture
    
    def _find_main_entry(self):
        """查找主入口函数"""
        main_entries = []
        
        # 检查 main.py
        main_file = self.project_path / 'main.py'
        if main_file.exists():
            entry = self._parse_python_main(main_file)
            if entry:
                main_entries.append(entry)
        
        # 检查 __main__.py
        main_module = self.project_path / '__main__.py'
        if main_module.exists():
            entry = self._parse_python_main(main_module)
            if entry:
                main_entries.append(entry)
        
        # 检查 app.py
        app_file = self.project_path / 'app.py'
        if app_file.exists():
            entry = self._parse_python_main(app_file)
            if entry:
                main_entries.append(entry)
        
        # 检查 index.js/index.ts
        for index_file in ['index.js', 'index.ts', 'app.js', 'app.ts']:
            idx = self.project_path / index_file
            if idx.exists():
                entry = self._parse_js_main(idx)
                if entry:
                    main_entries.append(entry)
        
        return main_entries
    
    def _parse_python_main(self, file_path):
        """解析Python主入口文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entry = {
                'file': str(file_path.relative_to(self.project_path)),
                'functions': [],
                'commands': [],
                'imports': []
            }
            
            # 提取函数定义
            import re
            functions = re.findall(r'def (\w+)\(', content)
            entry['functions'] = functions[:20]  # 限制数量
            
            # 提取命令行参数（argparse）
            if 'argparse' in content:
                commands = re.findall(r"add_parser\(['\"](\w+)['\"]", content)
                entry['commands'] = commands
            
            # 提取主要导入
            imports = re.findall(r'^(?:from|import)\s+(\S+)', content, re.MULTILINE)
            entry['imports'] = [imp for imp in imports if not imp.startswith('.')][:15]
            
            # 提取if __name__ == "__main__"块
            if '__name__' in content and '__main__' in content:
                entry['has_main_block'] = True
            
            return entry
        except:
            return None
    
    def _parse_js_main(self, file_path):
        """解析JavaScript主入口文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entry = {
                'file': str(file_path.relative_to(self.project_path)),
                'functions': [],
                'imports': []
            }
            
            import re
            # 提取函数定义
            functions = re.findall(r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:function|\([^)]*\)\s*=>))', content)
            entry['functions'] = [f[0] or f[1] for f in functions][:20]
            
            # 提取导入
            imports = re.findall(r"(?:import|require)\(['\"]([^'\"]+)['\"]\)", content)
            entry['imports'] = imports[:15]
            
            return entry
        except:
            return None
    
    def _find_core_modules(self):
        """查找核心模块"""
        core_modules = []
        
        # Python项目：查找.py文件中的类定义
        for py_file in self.project_path.rglob('*.py'):
            if self._is_ignored_path(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                import re
                
                # 提取类定义
                classes = re.findall(r'class\s+(\w+)', content)
                
                # 提取主要函数
                functions = re.findall(r'def\s+(\w+)\(', content)
                
                # 只保留有类或重要函数的模块
                if classes or len(functions) > 3:
                    module_info = {
                        'name': py_file.stem,
                        'file': str(py_file.relative_to(self.project_path)),
                        'classes': classes[:10],
                        'functions': functions[:15]
                    }
                    core_modules.append(module_info)
            except:
                pass
        
        # 限制返回数量
        return core_modules[:30]
    
    def _find_data_models(self):
        """查找数据模型"""
        data_models = []
        
        # 检查数据库配置
        config_file = self.project_path / 'config.py'
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                import re
                
                # 提取SQL CREATE语句
                create_statements = re.findall(r'CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\)', content, re.DOTALL)
                for table_name, columns in create_statements:
                    # 解析列
                    col_lines = [line.strip() for line in columns.split('\n') if line.strip() and not line.strip().startswith('--')]
                    cols = []
                    for col_line in col_lines:
                        if col_line.startswith(('CREATE', 'PRIMARY', 'FOREIGN', 'UNIQUE', 'INDEX')):
                            continue
                        parts = col_line.split()
                        if len(parts) >= 2:
                            cols.append({'name': parts[0], 'type': parts[1]})
                    
                    data_models.append({
                        'name': table_name,
                        'type': 'database_table',
                        'columns': cols[:15]
                    })
            except:
                pass
        
        # 检查SQLAlchemy模型
        for py_file in self.project_path.rglob('*.py'):
            if self._is_ignored_path(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                import re
                
                # 检查SQLAlchemy模型
                if 'db.Model' in content or 'Base' in content:
                    models = re.findall(r'class\s+(\w+)\(.*?Model\)', content)
                    for model in models:
                        data_models.append({
                            'name': model,
                            'type': 'sqlalchemy_model',
                            'file': str(py_file.relative_to(self.project_path))
                        })
                
                # 检查Pydantic模型
                if 'BaseModel' in content:
                    models = re.findall(r'class\s+(\w+)\(BaseModel\)', content)
                    for model in models:
                        data_models.append({
                            'name': model,
                            'type': 'pydantic_model',
                            'file': str(py_file.relative_to(self.project_path))
                        })
            except:
                pass
        
        return data_models
    
    def _analyze_dependencies(self):
        """分析模块依赖关系"""
        dependencies = {}
        
        # Python项目：分析import语句
        for py_file in self.project_path.rglob('*.py'):
            if self._is_ignored_path(py_file):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                import re
                
                module_name = py_file.stem
                
                # 提取本地导入
                local_imports = re.findall(r'^(?:from|import)\s+([a-zA-Z_]\w*)', content, re.MULTILINE)
                local_imports = [imp for imp in local_imports if imp not in ['os', 'sys', 'json', 're', 'logging', 'datetime', 'typing', 'pathlib']]
                
                if local_imports:
                    dependencies[module_name] = local_imports[:10]
            except:
                pass
        
        return dependencies
    
    def _is_ignored_path(self, path):
        """检查路径是否应该被忽略"""
        ignored_dirs = {
            'node_modules', '.git', '__pycache__', '.venv', 'venv',
            'dist', 'build', '.next', '.nuxt', 'target', 'out'
        }
        
        parts = path.parts
        return any(part in ignored_dirs for part in parts)


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze_project.py <项目路径>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    analyzer = ProjectAnalyzer(project_path)
    result = analyzer.analyze()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
