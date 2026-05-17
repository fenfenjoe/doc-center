#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Git操作脚本
负责执行Git相关操作
"""

import os
import sys
import json
import subprocess
from pathlib import Path


class GitOperations:
    """Git操作类"""
    
    def __init__(self):
        pass
    
    def clone(self, git_url, target_path):
        """克隆Git仓库"""
        target = Path(target_path)
        
        # 检查目标路径是否存在
        if target.exists():
            files = list(target.iterdir())
            if files:
                print(f"警告: 目标路径不为空: {target}")
                print("是否覆盖？(y/n)")
                choice = input().strip().lower()
                if choice != 'y':
                    return {'status': 'cancelled', 'message': '用户取消操作'}
                self._clear_directory(target)
        
        # 创建目录
        target.mkdir(parents=True, exist_ok=True)
        
        # 执行clone
        try:
            result = subprocess.run(
                ['git', 'clone', git_url, str(target)],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': f'成功克隆仓库到 {target}',
                    'path': str(target)
                }
            else:
                return {
                    'status': 'error',
                    'message': f'Git clone失败: {result.stderr}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Git操作失败: {str(e)}'
            }
    
    def check_remote(self, target_path):
        """检查远程Git地址"""
        target = Path(target_path)
        
        if not target.exists():
            return {
                'status': 'error',
                'message': f'路径不存在: {target}'
            }
        
        git_dir = target / '.git'
        if not git_dir.exists():
            return {
                'status': 'error',
                'message': '不是Git仓库'
            }
        
        try:
            result = subprocess.run(
                ['git', '-C', str(target), 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'remote_url': result.stdout.strip()
                }
            else:
                return {
                    'status': 'error',
                    'message': f'获取远程地址失败: {result.stderr}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Git操作失败: {str(e)}'
            }
    
    def clear(self, target_path):
        """清空目录"""
        import shutil
        target = Path(target_path)
        
        if not target.exists():
            return {
                'status': 'error',
                'message': f'路径不存在: {target}'
            }
        
        try:
            self._clear_directory(target)
            return {
                'status': 'success',
                'message': f'已清空目录: {target}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'清空目录失败: {str(e)}'
            }
    
    def _clear_directory(self, path):
        """清空目录内容"""
        import shutil
        path = Path(path)
        for item in path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()


def main():
    if len(sys.argv) < 2:
        print("用法: python git_operations.py <操作类型> [git_url] [target_path]")
        print("操作类型: clone, check_remote, clear")
        sys.exit(1)
    
    operation = sys.argv[1]
    git_ops = GitOperations()
    
    if operation == 'clone':
        if len(sys.argv) < 4:
            print("clone操作需要git_url和target_path参数")
            sys.exit(1)
        result = git_ops.clone(sys.argv[2], sys.argv[3])
    
    elif operation == 'check_remote':
        if len(sys.argv) < 3:
            print("check_remote操作需要target_path参数")
            sys.exit(1)
        result = git_ops.check_remote(sys.argv[2])
    
    elif operation == 'clear':
        if len(sys.argv) < 3:
            print("clear操作需要target_path参数")
            sys.exit(1)
        result = git_ops.clear(sys.argv[2])
    
    else:
        print(f"未知操作: {operation}")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
