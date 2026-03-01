#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动漫收藏统计可视化脚本
功能：分析动漫文档，生成统计图表和进度追踪
"""

import re
import json
from datetime import datetime
from collections import defaultdict

class AnimeStats:
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = ""
        self.anime_list = []
        self.stats = {
            'total': 0,
            'watched': 0,
            'unwatched': 0,
            'want_to_watch': 0,
            'by_region': defaultdict(lambda: {'total': 0, 'watched': 0}),
            'by_decade': defaultdict(int),
            'by_category': defaultdict(lambda: {'total': 0, 'watched': 0}),
            'ghibli': {'total': 0, 'watched': 0},
            'shanghai_animation': {'total': 0, 'watched': 0}
        }
        
    def load_file(self):
        """加载文件内容"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()
    
    def parse_anime(self):
        """解析文档中的动漫条目"""
        # 匹配格式：| [x] | 作品名 | 年份 | 简介 | 星级 |
        pattern = r'\|\s*\[([ x])\]\s*\|\s*\*\*(.+?)\*\*\s*\[.+?\]\s*\|\s*(.+?)\s*\|'
        matches = re.findall(pattern, self.content)
        
        # 确定当前区域
        current_region = "未知"
        current_category = "其他"
        
        lines = self.content.split('\n')
        for i, line in enumerate(lines):
            # 检测区域标题
            if '## 一、日本动画篇' in line:
                current_region = "日本动画"
            elif '## 二、国产动画篇' in line:
                current_region = "国产动画"
            elif '## 三、欧美动画篇' in line:
                current_region = "欧美动画"
            
            # 检测分类
            if '### 1.1' in line or '### 1.2' in line or '热血' in line or '科幻' in line or '机战' in line:
                current_category = "热血/科幻"
            elif '魔法少女' in line:
                current_category = "魔法少女"
            elif '恋爱' in line or '校园' in line:
                current_category = "恋爱校园"
            elif '运动' in line or '竞技' in line:
                current_category = "运动竞技"
            elif '搞笑' in line or '日常' in line:
                current_category = "搞笑日常"
            elif '推理' in line or '悬疑' in line:
                current_category = "推理悬疑"
            elif '宫崎骏' in line or '吉卜力' in line:
                current_category = "吉卜力"
            elif '上海美术' in line or '上海美影' in line:
                current_category = "上海美影厂"
            
            # 解析作品行
            match = re.search(r'\|\s*\[([ x])\]\s*\|\s*\*\*(.+?)\*\*', line)
            if match:
                watched = match.group(1) == 'x'
                name = match.group(2).strip()
                
                # 提取年份
                year_match = re.search(r'\|\s*(\d{4})', line)
                year = int(year_match.group(1)) if year_match else 0
                
                anime = {
                    'name': name,
                    'watched': watched,
                    'region': current_region,
                    'category': current_category,
                    'year': year,
                    'line_index': i
                }
                self.anime_list.append(anime)
        
        self._calculate_stats()
    
    def _calculate_stats(self):
        """计算统计数据"""
        self.stats['total'] = len(self.anime_list)
        self.stats['watched'] = sum(1 for a in self.anime_list if a['watched'])
        self.stats['unwatched'] = self.stats['total'] - self.stats['watched']
        
        for anime in self.anime_list:
            region = anime['region']
            category = anime['category']
            year = anime['year']
            watched = anime['watched']
            
            # 按区域统计
            self.stats['by_region'][region]['total'] += 1
            if watched:
                self.stats['by_region'][region]['watched'] += 1
            
            # 按年代统计
            if year >= 1960 and year < 1970:
                self.stats['by_decade']['1960s'] += 1
            elif year >= 1970 and year < 1980:
                self.stats['by_decade']['1970s'] += 1
            elif year >= 1980 and year < 1990:
                self.stats['by_decade']['1980s'] += 1
            elif year >= 1990 and year < 2000:
                self.stats['by_decade']['1990s'] += 1
            elif year >= 2000 and year < 2010:
                self.stats['by_decade']['2000s'] += 1
            elif year >= 2010:
                self.stats['by_decade']['2010s+'] += 1
            
            # 按分类统计
            self.stats['by_category'][category]['total'] += 1
            if watched:
                self.stats['by_category'][category]['watched'] += 1
            
            # 吉卜力作品
            if '吉卜力' in category or any(g in anime['name'] for g in ['龙猫', '千与千寻', '天空之城', '魔女宅急便', '幽灵公主', '哈尔的移动城堡', '风之谷', '萤火虫之墓']):
                self.stats['ghibli']['total'] += 1
                if watched:
                    self.stats['ghibli']['watched'] += 1
            
            # 上海美影厂作品
            if '上海美影厂' in category or any(s in anime['name'] for s in ['大闹天宫', '哪吒闹海', '天书奇谭', '黑猫警长', '葫芦兄弟', '舒克和贝塔', '阿凡提', '三个和尚', '九色鹿', '雪孩子']):
                self.stats['shanghai_animation']['total'] += 1
                if watched:
                    self.stats['shanghai_animation']['watched'] += 1
    
    def generate_progress_bar(self, current, total, length=20, filled='█', empty='░'):
        """生成进度条"""
        if total == 0:
            return f"[{empty * length}] 0%"
        percent = current / total
        filled_len = int(length * percent)
        bar = filled * filled_len + empty * (length - filled_len)
        return f"[{bar}] {percent*100:.1f}% ({current}/{total})"
    
    def generate_heatmap(self, data, max_fire=10):
        """生成热力图（emoji形式）"""
        if not data:
            return "暂无数据"
        
        max_val = max(data.values()) if data else 1
        result = []
        for decade, count in sorted(data.items()):
            fire_count = max(1, int(count / max(max_val, 1) * max_fire))
            fires = '🔥' * fire_count
            result.append(f"**{decade}**: {fires} ({count}部)")
        return '\n'.join(result)
    
    def get_achievement(self, watched_count):
        """获取成就等级"""
        achievements = [
            {'min': 0, 'max': 0, 'title': '🔰 零基础', 'desc': '从0开始动画之旅'},
            {'min': 1, 'max': 10, 'title': '🌱 动画萌新', 'desc': '开始探索动画世界'},
            {'min': 11, 'max': 30, 'title': '🌿 进阶观众', 'desc': '已初步涉猎经典作品'},
            {'min': 31, 'max': 50, 'title': '🌳 资深观众', 'desc': '对动画有深入了解'},
            {'min': 51, 'max': 100, 'title': '🏆 动画大师', 'desc': '阅片无数的大佬'},
            {'min': 101, 'max': 9999, 'title': '👑 神级存在', 'desc': '你是行走的传奇'}
        ]
        
        for ach in achievements:
            if ach['min'] <= watched_count <= ach['max']:
                next_level = ach['max'] + 1 if ach['max'] < 9999 else None
                progress = (watched_count - ach['min'] + 1) / (ach['max'] - ach['min'] + 1) * 100 if ach['max'] > ach['min'] else 100
                return {
                    'title': ach['title'],
                    'desc': ach['desc'],
                    'progress': progress,
                    'next_level': next_level
                }
        return achievements[0]
    
    def check_special_achievements(self):
        """检查特殊成就"""
        special = []
        
        # 吉卜力收藏家
        if self.stats['ghibli']['watched'] == self.stats['ghibli']['total'] and self.stats['ghibli']['total'] > 0:
            special.append('🎬 **吉卜力收藏家**：看过全部吉卜力工作室作品')
        elif self.stats['ghibli']['watched'] > 0:
            special.append(f'🎬 吉卜力收藏家进度：{self.stats["ghibli"]["watched"]}/{self.stats["ghibli"]["total"]}')
        
        # 上海美影厂收藏家
        if self.stats['shanghai_animation']['watched'] == self.stats['shanghai_animation']['total'] and self.stats['shanghai_animation']['total'] > 0:
            special.append('🇨🇳 **国产经典收藏家**：看过全部上海美影厂经典作品')
        elif self.stats['shanghai_animation']['watched'] > 0:
            special.append(f'🇨🇳 国产经典收藏家进度：{self.stats["shanghai_animation"]["watched"]}/{self.stats["shanghai_animation"]["total"]}')
        
        return special
    
    def generate_stats_section(self):
        """生成统计区域Markdown"""
        watched = self.stats['watched']
        total = self.stats['total']
        completion_rate = (watched / total * 100) if total > 0 else 0
        achievement = self.get_achievement(watched)
        special_achievements = self.check_special_achievements()
        
        md = f"""## 📊 观看统计仪表盘

> 🕐 **最后更新**：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
> 
> 🔄 **自动统计**：运行 `python3 scripts/anime_stats.py` 更新数据

---

### 🎯 总体进度

| 指标 | 数值 | 进度 |
|-----|------|------|
| **总作品数** | {total} 部 | - |
| **已观看** | {watched} 部 | {self.generate_progress_bar(watched, total)} |
| **未观看** | {self.stats['unwatched']} 部 | - |
| **完成率** | {completion_rate:.1f}% | {self.generate_progress_bar(int(completion_rate), 100, length=20)} |

---

### 📈 分类进度条

#### 按地区统计

"""
        
        # 按地区进度条
        for region, data in sorted(self.stats['by_region'].items(), key=lambda x: x[1]['total'], reverse=True):
            bar = self.generate_progress_bar(data['watched'], data['total'])
            md += f"- **{region}**：{bar}\n"
        
        md += "\n#### 按类型统计\n\n"
        
        # 按分类进度条
        for cat, data in sorted(self.stats['by_category'].items(), key=lambda x: x[1]['total'], reverse=True):
            if data['total'] >= 3:  # 只显示数量>=3的分类
                bar = self.generate_progress_bar(data['watched'], data['total'], length=15)
                md += f"- **{cat}**：{bar}\n"
        
        md += f"""
---

### 🔥 年代分布热力图

{self.generate_heatmap(dict(self.stats['by_decade']))}

---

### 🏆 成就系统

#### 当前等级

```
┌─────────────────────────────────────────┐
│  {achievement['title']:36} │
│  {achievement['desc']:36} │
│  进度: {self.generate_progress_bar(int(achievement['progress']), 100, length=25, filled='▓', empty='░')} │
└─────────────────────────────────────────┘
```

#### 等级体系

| 等级 | 范围 | 徽章 | 称号 |
|-----|------|-----|------|
| Lv.1 | 1-10部 | 🌱 | 动画萌新 |
| Lv.2 | 11-30部 | 🌿 | 进阶观众 |
| Lv.3 | 31-50部 | 🌳 | 资深观众 |
| Lv.4 | 51-100部 | 🏆 | 动画大师 |
| Lv.5 | 100+部 | 👑 | 神级存在 |

#### 特殊成就

"""
        
        if special_achievements:
            for ach in special_achievements:
                md += f"- {ach}\n"
        else:
            md += "- 🎯 暂无特殊成就，继续加油！\n"
        
        md += f"""
---

### 📋 快捷操作

```bash
# 重新统计
python3 scripts/anime_stats.py

# 导出JSON数据
python3 scripts/anime_stats.py --json

# 查看详细报告
python3 scripts/anime_stats.py --report
```

---

*统计由自动化脚本生成* 🎉
"""
        
        return md
    
    def export_json(self, output_path='anime_stats.json'):
        """导出JSON格式统计数据"""
        data = {
            'generated_at': datetime.now().isoformat(),
            'stats': {
                'total': self.stats['total'],
                'watched': self.stats['watched'],
                'unwatched': self.stats['unwatched'],
                'completion_rate': round(self.stats['watched'] / self.stats['total'] * 100, 2) if self.stats['total'] > 0 else 0,
                'by_region': dict(self.stats['by_region']),
                'by_decade': dict(self.stats['by_decade']),
                'by_category': dict(self.stats['by_category']),
                'special_collections': {
                    'ghibli': dict(self.stats['ghibli']),
                    'shanghai_animation': dict(self.stats['shanghai_animation'])
                }
            },
            'anime_list': self.anime_list
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 统计数据已导出到: {output_path}")
    
    def update_document(self, output_path=None):
        """更新文档，插入统计区域"""
        if output_path is None:
            output_path = self.file_path
        
        stats_section = self.generate_stats_section()
        
        # 查找原有统计区域并替换
        pattern = r'## 📊 观看统计.*?(?=## 🔗|$)'
        
        if re.search(pattern, self.content, re.DOTALL):
            # 替换现有统计区域
            new_content = re.sub(pattern, stats_section, self.content, flags=re.DOTALL)
        else:
            # 在文档末尾添加
            new_content = self.content + '\n\n' + stats_section
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 文档已更新: {output_path}")
        print(f"📊 统计摘要：{self.stats['watched']}/{self.stats['total']} 部已观看 ({self.stats['watched']/self.stats['total']*100:.1f}%)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='动漫收藏统计可视化工具')
    parser.add_argument('--file', '-f', default='docs/90s-anime-collection-checklist.md', 
                        help='输入文件路径')
    parser.add_argument('--output', '-o', default=None, 
                        help='输出文件路径（默认覆盖原文件）')
    parser.add_argument('--json', '-j', action='store_true', 
                        help='导出JSON格式')
    parser.add_argument('--report', '-r', action='store_true', 
                        help='显示详细报告')
    
    args = parser.parse_args()
    
    stats = AnimeStats(args.file)
    stats.load_file()
    stats.parse_anime()
    
    if args.json:
        stats.export_json()
    
    if args.report:
        print("\n📊 动漫收藏统计报告")
        print("=" * 50)
        print(f"总作品数: {stats.stats['total']}")
        print(f"已观看: {stats.stats['watched']}")
        print(f"完成率: {stats.stats['watched']/stats.stats['total']*100:.1f}%")
        print("\n按地区统计:")
        for region, data in sorted(stats.stats['by_region'].items()):
            print(f"  {region}: {data['watched']}/{data['total']}")
        print("\n年代分布:")
        for decade, count in sorted(stats.stats['by_decade'].items()):
            print(f"  {decade}: {count}部")
    
    # 默认更新文档
    stats.update_document(args.output)


if __name__ == '__main__':
    main()
