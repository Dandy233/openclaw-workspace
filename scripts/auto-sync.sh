#!/bin/bash
# Auto Git Sync Script
# 每小时自动检查并提交改动

set -e

WORKSPACE="/root/.openclaw/workspace"
cd "$WORKSPACE"

# 检查是否有改动
if [ -z "$(git status --porcelain)" ]; then
    echo "$(date): No changes to commit"
    exit 0
fi

# 添加所有改动
git add -A

# 提交
git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"

# 推送
git push origin main

echo "$(date): Auto-sync completed"
