#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫收藏可视化增强模块
为主文档生成精美的统计卡片和徽章
"""

import re
from datetime import datetime
from collections import Counter

def generate_visual_summary():
    """生成可视化摘要卡片"""
    
    summary = """
## 🎨 数据可视化看板

```
╔════════════════════════════════════════════════════════════════╗
║                    📊 动漫收藏数据看板 📊                       ║
╠════════════════════════════════════════════════════════════════╣
║  总作品: 116部    日本: 71部    国产: 22部    欧美: 23部      ║
║                                                                ║
║  年代分布: 80s[25]  90s[39]  00s[38]  其他[14]               ║
║                                                                ║
║  ████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ║
║  ██████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ║
║  █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   ║
║                                                                ║
║  类型TOP5: 搞笑日常(36) 热血科幻(25) 吉卜力(18) 上美(15) 恋爱(11) ║
╚════════════════════════════════════════════════════════════════╝
```

### 🗺️ 收藏地图

```
                    [动画收藏分布图]
                    
         🇨🇳 国产 (22部)              🇯🇵 日本 (71部)
              19%                          61%
               ▲                            ▲
              ╱ ╲                          ╱ ╲
             ╱   ╲                        ╱   ╲
            ╱     ╲                      ╱     ╲
           ╱   ⭐    ╲                    ╱   ⭐⭐⭐  ╲
          ╱           ╲                  ╱           ╲
         ╱             ╲                ╱             ╲
        ╱               ╲              ╱               ╲
       ╱                 ╲            ╱                 ╲
      ╱                   ╲          ╱                   ╲
     ╱                     ╲        ╱                     ╲
    ╱                       ╲      ╱                       ╲
   ╱                         ╲    ╱                         ╲
  ╱                           ╲  ╱                           ╲
 ╱                             ╲╱                             ╲
╱                                                              ╲
                         🇺🇸 欧美 (23部)
                              20%
```

### ⭐ 经典度分布

| 星级 | 数量 | 比例 | 视觉 |
|-----|------|------|------|
| ⭐⭐⭐⭐⭐ | 85部 | 73% | ████████████████████ |
| ⭐⭐⭐⭐ | 31部 | 27% | ███████░░░░░░░░░░░░░ |

### 📅 年代时间轴

```
1960 ○─── 1970 ○─── 1980 ●●●─── 1990 ●●●●●─── 2000 ●●●●─── 2010 ○
       │         │          │           │          │         │
       2部       5部       25部        39部       38部       5部
```

### 🏷️ 标签云

`#热血` `#恋爱` `#搞笑` `#科幻` `#魔法少女` `#运动` `#推理` `#吉卜力` `#上海美影` `#迪士尼` `#皮克斯` `#梦工厂` `#经典` `#童年回忆`

---

*数据基于当前收录的116部作品*
"""
    return summary

def generate_category_icons():
    """生成分类图标统计"""
    
    icons = """
### 🎭 分类图标墙

| 分类 | 图标 | 数量 | 占比 |
|-----|-----|------|------|
| 热血战斗 | 🔥 | 25部 | 22% |
| 恋爱校园 | 💕 | 24部 | 21% |
| 搞笑日常 | 😄 | 36部 | 31% |
| 科幻机战 | 🤖 | 12部 | 10% |
| 魔法少女 | 🪄 | 6部 | 5% |
| 运动竞技 | ⚽ | 9部 | 8% |
| 推理悬疑 | 🔍 | 4部 | 3% |

---
"""
    return icons

def insert_into_main_doc(file_path):
    """将可视化摘要插入到主文档"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成可视化内容
    visual_content = generate_visual_summary() + '\n' + generate_category_icons()
    
    # 检查是否已有可视化区域
    if '🎨 数据可视化看板' in content:
        # 替换现有区域
        pattern = r'## 🎨 数据可视化看板.*?(?=## |\Z)'
        new_content = re.sub(pattern, visual_content, content, flags=re.DOTALL)
    else:
        # 在统计汇总章节后添加
        # 查找"## 四、统计汇总"章节
        insert_marker = "## 四、统计汇总"
        if insert_marker in content:
            parts = content.split(insert_marker)
            if len(parts) == 2:
                # 在统计汇总章节结束后插入
                section_end = parts[1].find("\n## ", 500)
                if section_end > 0:
                    new_content = parts[0] + insert_marker + parts[1][:section_end] + '\n\n' + visual_content + parts[1][section_end:]
                else:
                    new_content = content + '\n\n' + visual_content
            else:
                new_content = content + '\n\n' + visual_content
        else:
            new_content = content + '\n\n' + visual_content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ 主文档已更新可视化摘要: {file_path}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        insert_into_main_doc(sys.argv[1])
    else:
        insert_into_main_doc('docs/90s-anime-collection.md')
