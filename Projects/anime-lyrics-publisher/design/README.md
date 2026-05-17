# anime-lyrics-publisher - 设计文档

## 架构设计

### 技术栈

- **编程语言**: Python
- **框架**: APScheduler (定时任务调度)
- **数据库**: SQLite
- **构建工具**: pip
- **第三方库**: requests, BeautifulSoup4, PIL/Pillow, urllib3

### 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        主入口 (main.py)                          │
│                     命令行接口 (argparse)                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  定时调度器    │      │  手动命令执行  │      │  状态查询      │
│ (scheduler.py)│      │               │      │               │
└───────┬───────┘      └───────┬───────┘      └───────────────┘
        │                      │
        │  每周六 2:00         │  每天 7:00
        ▼                      ▼
┌───────────────┐      ┌───────────────┐
│  歌词爬取任务  │      │  文章发布任务  │
│               │      │               │
│ 1.选动画      │      │ 1.取歌词       │
│ 2.爬歌词      │      │ 2.AI分析       │
│ 3.存数据库    │      │ 3.生成文章     │
│               │      │ 4.爬取配图     │
│               │      │ 5.发布微信     │
└───────┬───────┘      └───────┬───────┘
        │                      │
        ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据库层 (database.py)                      │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐         │
│  │ anime   │  │ lyrics  │  │ articles │  │ task_logs│         │
│  └─────────┘  └─────────┘  └──────────┘  └──────────┘         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│  QQ音乐爬虫    │      │  文章生成器    │      │  微信发布器    │
│ (qq_music.py) │      │ (article_gen) │      │ (wechat_pub)  │
│               │      │               │      │               │
│ - 搜索歌曲    │      │ - 准备AI任务  │      │ - 获取Token   │
│ - 获取歌词    │      │ - 等待AI结果  │      │ - 上传素材    │
│ - 解析歌词    │      │ - 格式化文章  │      │ - 创建草稿    │
└───────────────┘      └───────┬───────┘      └───────┬───────┘
                               │                      │
                               ▼                      ▼
                      ┌───────────────┐      ┌───────────────┐
                      │  AI分析器      │      │  图片爬虫      │
                      │ (ai_analyzer) │      │ (image_spider)│
                      │               │      │               │
                      │ - 调用LLM     │      │ - MAL API     │
                      │ - 翻译歌词    │      │ - 感知哈希    │
                      │ - 语法解析    │      │ - 本地缓存    │
                      └───────────────┘      └───────────────┘
```

### 架构模式

- **分层架构**: 命令行层 → 业务逻辑层 → 数据访问层
- **模块化设计**: 每个功能模块独立，通过数据库和配置文件交互
- **事件驱动**: 定时任务触发业务流程

## 模块设计

### 核心模块

#### 1. 配置管理模块 (config.py)

**职责**: 集中管理所有配置项

**主要配置**:
- 项目路径配置
- 微信公众号配置 (AppID, AppSecret)
- 定时任务配置 (每周爬取时间、每日发布时间)
- 动画池配置 (ANIME_LIST, ANIME_RESERVE_LIST)
- 歌词网站配置
- 文章生成配置 (标题模板、歌词数量限制)
- LLM配置 (提供商选择、API密钥)
- 数据库表结构定义 (DB_INIT_SQL)

#### 2. 数据库模块 (database.py)

**职责**: 封装SQLite数据库操作

**核心类**: `Database`

**主要方法**:
- `add_anime()`: 添加动画记录
- `get_random_pending_anime()`: 获取随机待爬取动画
- `update_anime_status()`: 更新动画状态
- `add_lyrics()`: 添加歌词记录
- `get_random_unused_lyrics()`: 获取随机未使用歌词
- `add_article()`: 添加文章记录
- `update_article_wechat_ids()`: 更新文章微信ID
- `add_task_log()`: 添加任务日志
- `get_recent_task_logs()`: 获取最近任务日志

**设计特点**:
- 使用上下文管理器管理数据库连接
- 支持事务自动提交/回滚
- 全局单例模式 (`db = Database()`)

#### 3. 歌词爬虫模块 (anime_lyrics_spider.py)

**职责**: 从QQ音乐爬取动漫歌词

**核心类**: `LyricsSpider`

**主要功能**:
- QQ音乐歌曲搜索
- 歌词内容获取和解析
- 动画歌曲配置表 (ANIME_SONG_CONFIG)
- 每周歌词爬取入口 (`crawl_weekly_lyrics()`)

**设计特点**:
- 精确匹配歌曲名和歌手
- 支持search_hints兜底搜索
- 歌词去重检查

#### 4. QQ音乐API模块 (qq_music.py)

**职责**: 封装QQ音乐API接口

**主要功能**:
- 歌曲搜索 (`search_song()`)
- 歌词获取 (`get_lyrics_by_song()`)
- 歌词解析和格式化

#### 5. 文章生成模块 (article_generator.py)

**职责**: 将歌词数据格式化为微信公众号文章

**核心类**: `ArticleGenerator`

**工作流程**:
1. 从数据库获取未使用歌词
2. 写入 `pending_analysis.json` 等待AI分析
3. 轮询等待 `analysis_result.json` 出现
4. 读取AI分析结果
5. 格式化为文章HTML
6. 存入数据库

**主要函数**:
- `prepare_analysis_task()`: 准备AI分析任务
- `wait_for_analysis()`: 等待AI分析结果
- `format_article()`: 格式化文章
- `generate_daily_article()`: 每日文章生成入口

#### 6. AI分析模块 (ai_analyzer.py)

**职责**: 调用LLM分析歌词

**主要功能**:
- 读取待分析任务文件
- 调用LLM API (OpenAI/Anthropic/WorkBuddy)
- 生成翻译和语法解析
- 写入分析结果文件

#### 7. 微信发布模块 (wechat_publisher.py)

**职责**: 封装微信公众号API

**核心类**: `WechatPublisher`

**主要方法**:
- `get_access_token()`: 获取微信access_token
- `upload_image()`: 上传图片素材
- `create_draft_article()`: 创建草稿图文消息
- `publish_article()`: 发布文章
- `generate_and_publish_article()`: 完整发布流程

**设计特点**:
- access_token自动缓存和刷新
- Markdown转HTML
- 图片URL处理
- 绕过系统代理设置

#### 8. 图片爬虫模块 (image_spider.py)

**职责**: 从MyAnimeList API爬取动画图片

**核心类**: 
- `ImageSpider`: 图片爬虫
- `ImageCache`: 图片缓存管理器

**主要功能**:
- MAL API动画搜索
- 图片下载
- 感知哈希(aHash)去重
- 本地缓存管理
- 文章配图获取

**缓存策略**:
1. 优先使用未使用图片
2. 不足时自动从MAL补仓
3. 补仓仍不足则回退复用已使用图片

#### 9. 定时调度模块 (scheduler.py)

**职责**: 管理定时任务

**核心类**: `TaskScheduler`

**任务配置**:
- 每周爬取: 周六 2:00 (CronTrigger)
- 每日发布: 每天 7:00 (CronTrigger)

**主要方法**:
- `setup_jobs()`: 设置定时任务
- `weekly_crawl_task()`: 执行每周爬取
- `daily_publish_task()`: 执行每日发布
- `run()`: 启动调度器

### 模块关系

```
main.py
├── config.py (配置)
├── database.py (数据访问)
├── anime_lyrics_spider.py (爬虫)
│   ├── qq_music.py (QQ音乐API)
│   └── database.py
├── article_generator.py (文章生成)
│   ├── config.py
│   ├── database.py
│   └── ai_analyzer.py (AI分析)
├── wechat_publisher.py (微信发布)
│   ├── config.py
│   ├── database.py
│   └── image_spider.py (图片爬虫)
└── scheduler.py (定时调度)
    ├── config.py
    ├── database.py
    ├── anime_lyrics_spider.py
    ├── article_generator.py
    └── wechat_publisher.py
```

## 数据库设计

### 数据模型

**数据库文件**: `data/anime_lyrics.db`

### 表结构

#### 1. anime (动画信息表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| name | TEXT | NOT NULL | 动画中文名 |
| name_jp | TEXT | | 动画日文名 |
| year | INTEGER | | 年份 |
| cover_image_url | TEXT | | 封面图片URL |
| status | TEXT | DEFAULT 'pending' | 状态: pending/crawling/completed/failed |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

#### 2. lyrics (歌词表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| anime_id | INTEGER | NOT NULL, FOREIGN KEY | 关联动画 |
| song_name | TEXT | NOT NULL | 歌曲名 |
| song_name_cn | TEXT | | 歌曲中文名 |
| song_type | TEXT | | 歌曲类型: OP/ED/IN/TM |
| singer | TEXT | | 歌手 |
| language | TEXT | DEFAULT 'ja' | 语言: ja/en/zh/ko |
| lyrics_text | TEXT | | 歌词内容 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 3. articles (文章表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| lyrics_id | INTEGER | NOT NULL, FOREIGN KEY | 关联歌词 |
| article_title | TEXT | | 文章标题 |
| article_content | TEXT | | 文章内容(HTML) |
| cover_image_path | TEXT | | 封面图片路径 |
| wechat_media_id | TEXT | | 微信素材ID |
| wechat_article_id | TEXT | | 微信草稿ID |
| status | TEXT | DEFAULT 'draft' | 状态: draft/published |
| published_at | TIMESTAMP | | 发布时间 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 4. task_logs (任务日志表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| task_type | TEXT | NOT NULL | 任务类型: weekly_crawl/daily_publish |
| status | TEXT | DEFAULT 'running' | 状态: running/success/failed |
| message | TEXT | | 消息 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |

#### 5. used_anime_images (已使用图片记录表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | 主键 |
| anime_name | TEXT | NOT NULL | 动画中文名 |
| image_url | TEXT | NOT NULL, UNIQUE | 图片源URL |
| image_path | TEXT | NOT NULL | 本地文件路径 |
| hash_value | TEXT | | 感知哈希(aHash) |
| used_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 使用时间 |

## 接口设计

### 外部API接口

#### 1. QQ音乐API

- **搜索接口**: `https://c.y.qq.com/soso/fcgi-bin/client_search_cp`
- **歌词接口**: `https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg`

#### 2. MyAnimeList Jikan API

- **动画搜索**: `https://api.jikan.moe/v4/anime?q={query}`
- **动画详情**: `https://api.jikan.moe/v4/anime/{id}`
- **动画图片**: `https://api.jikan.moe/v4/anime/{id}/pictures`

#### 3. 微信公众号API

- **Token获取**: `GET https://api.weixin.qq.com/cgi-bin/token`
- **素材上传**: `POST https://api.weixin.qq.com/cgi-bin/material/add_material`
- **草稿创建**: `POST https://api.weixin.qq.com/cgi-bin/draft/add`

### 内部接口

#### AI交换文件

- **待分析任务**: `data/pending_analysis.json`
- **分析结果**: `data/analysis_result.json`

**任务格式**:
```json
{
  "task_id": "task_1234567890",
  "created_at": "2026-05-17T10:00:00",
  "status": "pending",
  "anime_name": "鬼灭之刃",
  "anime_name_jp": "鬼滅の刃",
  "song_name": "紅蓮華",
  "song_type": "OP",
  "singer": "LiSA",
  "language": "ja",
  "lyrics_lines": ["歌词行1", "歌词行2", ...],
  "result": []
}
```

**结果格式**:
```json
{
  "status": "done",
  "result": [
    {
      "original": "原文歌词",
      "furigana": "注音",
      "translation": "中文翻译",
      "grammar": "语法解析"
    }
  ]
}
```

## 部署设计

### 部署架构

- **单机部署**: 所有组件运行在同一台机器
- **定时任务**: 使用APScheduler内置BlockingScheduler
- **数据存储**: SQLite单文件数据库

### 环境配置

- **开发环境**: 本地Python环境
- **生产环境**: 服务器持续运行 `python main.py scheduler`

## 安全设计

### 认证授权

- **微信Token**: access_token自动获取和刷新，提前5分钟过期
- **API密钥**: 当前硬编码在config.py中，建议迁移到环境变量

### 数据安全

- **数据库**: SQLite文件权限控制
- **图片缓存**: 本地文件系统存储
- **日志**: 记录任务执行状态，便于问题追踪
