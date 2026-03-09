#!/bin/bash
# Auto Git Sync Script with Error Handling
# 每小时自动检查并提交改动，出错时记录到错误日志

set -e

WORKSPACE="/root/.openclaw/workspace"
ERROR_LOG="/var/log/openclaw-script-errors.log"
SCRIPT_NAME="auto-git-sync"
cd "$WORKSPACE"

# 错误处理函数
handle_error() {
    local error_msg="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$SCRIPT_NAME] ERROR: $error_msg" >> "$ERROR_LOG"
    echo "[$SCRIPT_NAME] 错误已记录: $error_msg" >&2
    exit 1
}

# 检查 Git 仓库状态
if ! git status --porcelain > /dev/null 2>&1; then
    handle_error "无法获取 Git 状态，可能不在 Git 仓库中"
fi

# 检查是否有改动
if [ -z "$(git status --porcelain)" ]; then
    echo "$(date): No changes to commit"
    exit 0
fi

# 检查远程连接
if ! git ls-remote origin > /dev/null 2>&1; then
    handle_error "无法连接到远程仓库 origin"
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)

# 先拉取远程更新（避免冲突）
if ! git pull origin "$CURRENT_BRANCH" --rebase > /tmp/git-pull.log 2>&1; then
    handle_error "拉取远程更新失败: $(cat /tmp/git-pull.log)"
fi

# 添加所有改动
git add -A

# 提交
if ! git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" > /tmp/git-commit.log 2>&1; then
    handle_error "提交失败: $(cat /tmp/git-commit.log)"
fi

# 推送
if ! git push origin "$CURRENT_BRANCH" > /tmp/git-push.log 2>&1; then
    handle_error "推送失败: $(cat /tmp/git-push.log)"
fi

echo "$(date): Auto-sync completed successfully"
