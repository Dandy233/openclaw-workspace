# 动漫文档社交功能设计文档

> 参考设计：MyAnimeList社区 + Letterboxd社交列表 + GitHub原生讨论区

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    社交功能架构图                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  讨论区系统  │    │  推荐系统   │    │  榜单系统   │ │
│  │  (GitHub)   │◄──►│  (本地算法) │◄──►│  (GitHub)   │ │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘ │
│         │                  │                  │        │
│         └──────────────────┼──────────────────┘        │
│                            │                           │
│                            ▼                           │
│                     ┌─────────────┐                    │
│                     │  对比系统   │                    │
│                     │  (模板工具) │                    │
│                     └─────────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 二、详细设计

### 2.1 讨论区系统 (GitHub Discussions)

**分类设计：**
```
📁 Discussions
├── 📂 作品讨论 (Anime Discussion)
│   ├── [七龙珠Z] 讨论帖
│   ├── [灌篮高手] 讨论帖
│   └── ...
├── 📂 推荐求助 (Recommendations)
│   ├── "求推荐类似EVA的作品"
│   └── "喜欢热血番的进"
├── 📂 榜单投票 (Rankings)
│   ├── 最受欢迎作品投票
│   └── 最被低估作品投票
└── 📂 综合交流 (General)
    ├── 怀旧分享
    └── 新番讨论
```

**每部作品讨论帖模板：**
```markdown
# [作品名] - [年份]

## 基本信息
- 类型：[热血/科幻/恋爱...]
- 制作：[制作公司]
- 经典度：⭐⭐⭐⭐⭐

## 讨论区
[在此发表评论]

## 相关推荐
- 相似作品：...
- 同作者：...
```

### 2.2 推荐系统算法

**算法一：基于类型的相似推荐**
```python
# 伪代码
def recommend_by_type(anime, watched_list):
    # 1. 获取目标作品的类型
    target_type = anime.type  # e.g., "热血战斗"
    
    # 2. 找出同类型作品
    same_type = filter(lambda x: x.type == target_type, all_anime)
    
    # 3. 排除已观看
    candidates = same_type - watched_list
    
    # 4. 按经典度排序
    return sorted(candidates, key=lambda x: x.rating, reverse=True)[:10]
```

**算法二：协同过滤 "喜欢X的人也喜欢Y"**
```python
def collaborative_filter(user_watched, all_users_data):
    """
    基于用户观看历史的协同过滤
    """
    # 1. 找到相似用户
    similar_users = find_users_with_similar_taste(user_watched)
    
    # 2. 统计相似用户观看但当前用户未看的作品
    recommendations = {}
    for user in similar_users:
        for anime in user.watched:
            if anime not in user_watched:
                recommendations[anime] += 1
    
    # 3. 返回推荐排序
    return sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
```

**算法三：综合推荐分数**
```
推荐分数 = 0.4 * 类型匹配度 + 0.3 * 协同过滤分数 + 0.2 * 经典度 + 0.1 * 热度
```

### 2.3 榜单投票机制

**投票方式：**
- 在GitHub Discussion中使用 👍 👎 反应
- 每季度结算一次票数
- 自动生成榜单更新

**榜单分类：**
1. **最受欢迎作品榜** - 总票数最高
2. **最被低估作品榜** - 高评分但低讨论度
3. **怀旧经典榜** - 按年代分类的人气榜
4. **类型细分榜** - 热血/科幻/恋爱等分类榜

**计分公式：**
```
作品得分 = 👍数量 × 1.0 + 💖数量 × 2.0 + 🚀数量 × 1.5
```

### 2.4 对比功能设计

**对比维度：**
```
┌──────────────────────────────────────────┐
│           用户A vs 用户B 对比报告          │
├──────────────────────────────────────────┤
│                                          │
│  共同看过的作品 (23部)                    │
│  ├── 七龙珠Z ⭐⭐⭐⭐⭐                   │
│  ├── 灌篮高手 ⭐⭐⭐⭐⭐                   │
│  └── ...                                 │
│                                          │
│  相似度评分: 78%                          │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │        口味分析                     │ │
│  │  A偏好: 热血战斗 (45%)              │ │
│  │  B偏好: 科幻机战 (38%)              │ │
│  │  共同偏好: 热血战斗 (32%)           │ │
│  └────────────────────────────────────┘ │
│                                          │
│  A看过但B没看的推荐 (10部)                │
│  B看过但A没看的推荐 (8部)                 │
│                                          │
└──────────────────────────────────────────┘
```

**相似度计算公式：**
```
Jaccard相似度 = |A∩B| / |A∪B|
加权相似度 = Σ(作品匹配权重) / Σ(所有作品权重)
```

## 三、技术实现方案

### 3.1 文件结构

```
docs/
├── 90s-anime-collection.md          # 主文档
├── 90s-anime-collection-checklist.md # 可标记版
├── social/
│   ├── README.md                     # 社交功能总览
│   ├── recommendations/              # 推荐列表
│   │   ├── by-type/                  # 按类型推荐
│   │   ├── by-era/                   # 按年代推荐
│   │   └── similar-pairs.md          # "喜欢X也喜欢Y"
│   ├── rankings/                     # 榜单排行
│   │   ├── most-popular.md           # 最受欢迎
│   │   ├── underrated.md             # 最被低估
│   │   └── by-genre/                 # 分类榜单
│   ├── discussion-guide.md           # 讨论区使用指南
│   └── compare/
│       ├── template.md               # 对比模板
│       └── examples/                 # 对比示例
└── .github/
    └── DISCUSSION_TEMPLATE/          # GitHub讨论模板
        ├── anime_discussion.yml      # 作品讨论模板
        ├── recommendation.yml        # 推荐求助模板
        └── ranking_vote.yml          # 投票模板
```

### 3.2 数据结构

**作品元数据 (anime-metadata.json):**
```json
{
  "anime": [
    {
      "id": "dragon-ball-z",
      "name": "七龙珠Z",
      "name_jp": "ドラゴンボールZ",
      "year": "1989-1996",
      "type": ["热血战斗"],
      "studio": "东映动画",
      "rating": 5,
      "tags": ["少年漫", "格斗", "外星", "经典"],
      "relations": {
        "similar": ["幽游白书", "全职猎人"],
        "same_studio": ["美少女战士", "数码宝贝"],
        "same_author": ["阿拉蕾", "龙珠超"]
      }
    }
  ]
}
```

**用户观看数据 (user-watchlist.json):**
```json
{
  "user": "username",
  "watched": [
    {
      "anime_id": "dragon-ball-z",
      "watched_date": "2024-01-15",
      "rating": 5,
      "tags": ["童年回忆", "神作"]
    }
  ],
  "favorites": ["anime_id_1", "anime_id_2"],
  "wishlist": ["anime_id_3"]
}
```

## 四、使用流程

### 4.1 参与讨论
1. 进入GitHub Discussions
2. 选择作品讨论区
3. 发表评论或回复他人

### 4.2 获取推荐
1. 查看社交/recommendations目录
2. 根据已看作品找相似推荐
3. 使用协同过滤推荐列表

### 4.3 参与投票
1. 进入榜单投票Discussion
2. 对喜欢的作品添加👍反应
3. 查看实时排行榜

### 4.4 生成对比
1. 复制对比模板
2. 填写两个用户的观看列表
3. 生成对比报告

## 五、未来扩展

### 5.1 高级功能
- [ ] 个人观看时间线
- [ ] 成就系统（观看里程碑）
- [ ] 动态推荐（根据观看历史实时更新）
- [ ] 评分预测

### 5.2 集成计划
- [ ] 与Bangumi API集成获取评分
- [ ] 与豆瓣API获取图片和简介
- [ ] 自动化榜单更新脚本

## 附录：GitHub Discussions 设置指南

### 启用Discussions
1. 进入仓库 Settings
2. 勾选 Features → Discussions
3. 创建 Discussion 分类

### 创建模板
1. 新建 `.github/DISCUSSION_TEMPLATE/anime_discussion.yml`
2. 定义表单字段
3. 提交到main分支

---

*设计文档 v1.0*
*最后更新: 2026-03-02*
