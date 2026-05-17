#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文档生成包装脚本
直接从文件读取分析结果
"""

import json
import sys
from pathlib import Path

# 添加doc-generator脚本路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'doc-generator' / 'scripts'))

from generate_docs import DocGenerator

def main():
    project_name = sys.argv[1]
    project_path = sys.argv[2]
    analysis_file = sys.argv[3]
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_result = json.load(f)
    
    generator = DocGenerator(project_name, project_path, analysis_result)
    result = generator.generate()
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
