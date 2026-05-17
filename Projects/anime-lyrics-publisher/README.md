# anime-lyrics-publisher

## 项目简介

动漫歌词爬取与发布工具 - 自动化爬取动漫歌曲歌词，通过AI分析生成日语学习文章，并发布到微信公众号。

## 技术栈

- **编程语言**: Python
- **框架**: APScheduler (定时任务调度)
- **数据库**: SQLite
- **构建工具**: pip
- **第三方库**: requests, BeautifulSoup4, PIL/Pillow, urllib3

## 项目架构

### 主入口

**文件**: `main.py`

使用 `argparse` 实现命令行接口，支持以下命令：

| 命令 | 功能 |
|------|------|
| `python main.py scheduler` | 启动定时任务调度器 |
| `python main.py weekly` | 手动执行每周歌词爬取任务 |
| `python main.py daily` | 手动执行每日发布任务 |
| `python main.py generate` | 仅生成文章（不发布） |
| `python main.py status` | 显示系统状态 |

### 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| 配置管理 | `config.py` | 项目路径、微信配置、定时任务配置、动画池配置、LLM配置、数据库表结构定义 |
| 数据库 | `database.py` | SQLite操作封装，包含anime/lyrics/articles/task_logs/used_anime_images五个表 |
| 歌词爬虫 | `anime_lyrics_spider.py` | 从QQ音乐爬取动漫歌词，支持精确匹配歌曲名和歌手 |
| QQ音乐API | `qq_music.py` | QQ音乐搜索和歌词获取接口封装 |
| 文章生成 | `article_generator.py` | 将歌词数据格式化为微信公众号文章，支持AI分析结果集成 |
| AI分析 | `ai_analyzer.py` | 调用LLM分析歌词，生成翻译和语法解析 |
| 微信发布 | `wechat_publisher.py` | 微信公众号API封装，支持上传素材、创建草稿、发布文章 |
| 图片爬虫 | `image_spider.py` | 从MyAnimeList API爬取动画图片，支持感知哈希去重和本地缓存 |
| 定时调度 | `scheduler.py` | 基于APScheduler的定时任务管理 |

### 数据模型

**数据库**: `data/anime_lyrics.db` (SQLite)

| 表名 | 字段 | 说明 |
|------|------|------|
| `anime` | id, name, name_jp, year, cover_image_url, status, created_at, updated_at | 动画信息表 |
| `lyrics` | id, anime_id, song_name, song_name_cn, song_type, singer, language, lyrics_text, created_at | 歌词表 |
| `articles` | id, lyrics_id, article_title, article_content, cover_image_path, wechat_media_id, wechat_article_id, status, published_at, created_at | 文章表 |
| `task_logs` | id, task_type, status, message, created_at | 任务日志表 |
| `used_anime_images` | id, anime_name, image_url, image_path, hash_value, used_at | 已使用图片记录表 |

### 模块依赖关系

```
main.py
├── config.py
├── database.py
├── anime_lyrics_spider.py
│   ├── qq_music.py
│   └── database.py
├── article_generator.py
│   ├── config.py
│   ├── database.py
│   └── ai_analyzer.py
├── wechat_publisher.py
│   ├── config.py
│   ├── database.py
│   └── image_spider.py
└── scheduler.py
    ├── config.py
    ├── database.py
    ├── anime_lyrics_spider.py
    ├── article_generator.py
    └── wechat_publisher.py
```

## 工作流程

### 每周歌词爬取流程

1. 从动画池中随机选取待爬取的动画
2. 调用QQ音乐API搜索对应动画的歌曲
3. 获取歌词内容并存入数据库
4. 更新动画状态为completed

### 每日文章发布流程

1. 从数据库获取未使用的歌词
2. 写入 `data/pending_analysis.json` 等待AI分析
3. AI分析歌词并写入 `data/analysis_result.json`
4. 读取分析结果，格式化为文章
5. 爬取配图（从MyAnimeList API）
6. 发布到微信公众号草稿箱

## 快速开始

### 环境要求

- Python 3.8+
- SQLite3

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
# 启动定时任务调度器
python main.py scheduler

# 手动执行每周爬取任务
python main.py weekly

# 手动执行每日发布任务
python main.py daily

# 仅生成文章（不发布）
python main.py generate

# 查看系统状态
python main.py status
```

## 配置说明

### 微信公众号配置

在 `config.py` 中设置 `WECHAT_APP_ID` 和 `WECHAT_APP_SECRET`。

### 动画池配置

- `ANIME_LIST`: 主动画池，按顺序爬取
- `ANIME_RESERVE_LIST`: 后备动画池，主池耗尽后自动补充
- `ANIME_BATCH_SIZE`: 每次补充的动画数量

### LLM配置

- `LLM_PROVIDER`: 选择LLM提供商（mock/openai/anthropic/workbuddy）
- `OPENAI_API_KEY`: OpenAI API密钥
- `ANTHROPIC_API_KEY`: Anthropic API密钥

## 项目信息

- **项目名称**: anime-lyrics-publisher
- **项目路径**: E:\workspace\workbuddy\anime-lyrics-publisher
- **GitHub**: https://github.com/fenfenjoe/anime-lyrics-publisher
