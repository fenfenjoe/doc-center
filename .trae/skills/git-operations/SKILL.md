# Git操作

## Description

负责Git操作的Skill，包括克隆仓库、检查远程地址、清空目录等。

## When to Use

- 需要克隆Git仓库到本地
- 需要检查目录的Git远程地址
- 需要清空目录内容

## Input Format

- **操作类型**（必填）：clone, check_remote, clear
- **Git地址**（clone操作必填）：远程Git仓库地址
- **目标路径**（必填）：本地目录路径

## Process

### clone操作
- 检查目标路径是否存在
- 如果存在且不为空，询问是否覆盖
- 执行git clone

### check_remote操作
- 检查目录是否有.git
- 获取origin远程地址

### clear操作
- 清空目录所有内容

## Output Format

JSON格式的操作结果

## Scripts

执行脚本：`scripts/git_operations.py`

用法：
```bash
python scripts/git_operations.py <操作类型> [git_url] [target_path]
```
