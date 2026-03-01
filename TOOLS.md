# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 当前配置

### 定时任务（5个）
- daily-it-news: 每天 9:00 发送 IT 新闻简报
- daily-task-review: 每天 18:00 任务回顾日报
- weekly-system-check: 每周一 10:00 系统健康检查
- auto-git-sync: 每小时自动 Git 同步
- delayed-surprise: 2026-03-02 9:00 知识更新调研

### 脚本
- scripts/health-check.sh: 系统健康检查脚本
- scripts/auto-sync.sh: Git 自动同步脚本

### 目录结构
- memory/: 每日日志和长期记忆
- diary/: 私人日记
- scripts/: 自动化脚本
- archive/: 归档文件（大会话文件等）
- docs/: 文档和报告

---

## 技能使用指南

### 🌤️ Weather (天气查询)
- **状态**: ✅ 已就绪
- **来源**: openclaw-bundled
- **依赖**: curl
- **API**: wttr.in / Open-Meteo

**使用示例**:
```bash
# 快速查询（北京）
curl -s "wttr.in/Beijing?format=3"
# 输出: Beijing: ⛅️ +8°C

# 紧凑格式（位置+天气+温度+湿度+风力）
curl -s "wttr.in/Beijing?format=%l:+%c+%t+%h+%w"
# 输出: Beijing: ⛅️ +8°C 71% ↙5km/h

# 完整预报（无广告）
curl -s "wttr.in/Beijing?T"

# 当前天气（今天）
curl -s "wttr.in/Beijing?0"
```

**格式代码**:
| 代码 | 含义 |
|------|------|
| %c | 天气状况图标 |
| %t | 温度 |
| %h | 湿度 |
| %w | 风力 |
| %l | 位置名称 |
| %m | 月相 |

**高级用法**:
```bash
# 机场代码查询
curl -s "wttr.in/JFK?format=3"

# 公制单位
curl -s "wttr.in/Beijing?m"

# 英制单位
curl -s "wttr.in/New+York?u"

# 生成PNG图片
curl -s "wttr.in/Beijing.png" -o /tmp/weather.png
```

### 🧾 Summarize (内容摘要)
- **状态**: ✅ 已安装（简化版）
- **来源**: 本地脚本
- **功能**: 从URL提取网页文本，从本地文件提取内容
- **用途**: 快速阅读文章、文档预览

**安装位置**: `scripts/summarize`

**使用方法**:
```bash
# 网页摘要
summarize https://example.com/article

# 本地文件
summarize /path/to/document.txt
```

**注意**: 当前安装的是简化版，使用curl+文本提取实现。完整版功能（PDF解析、视频转录）需安装官方CLI：
```bash
brew install summarize  # macOS
```

**使用场景**:
- 快速了解长文章内容
- 提取网页正文（去除广告/导航）
- 文档自动摘要

### 📦 ClawHub 技能管理

**搜索技能**:
```bash
clawhub search <关键词>
```

**安装技能**:
```bash
clawhub install <技能名> --no-input
```

**列出已安装**:
```bash
clawhub list
```

**更新技能**:
```bash
clawhub update <技能名>
```
