#!/bin/bash
# Auto Git Sync Script with Error Handling
# 每小时自动检查并提交改动，出错时记录到错误日志
# 支持HTTPS和SSH双模式推送

set -e

WORKSPACE="/root/.openclaw/workspace"
ERROR_LOG="/var/log/openclaw-script-errors.log"
SCRIPT_NAME="auto-git-sync"
cd "$WORKSPACE"

# 获取原始远程URL
ORIGIN_URL=$(git remote get-url origin)
# SSH URL（从HTTPS转换）
SSH_URL="git@github.com:Dandy233/kimiclaw-workspace.git"

# 错误处理函数
handle_error() {
    local error_msg="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$SCRIPT_NAME] ERROR: $error_msg" >> "$ERROR_LOG"
    echo "[$SCRIPT_NAME] 错误已记录: $error_msg" >&2
    exit 1
}

# 切换远程URL函数
switch_to_ssh() {
    git remote set-url origin "$SSH_URL"
    echo "$(date): 已切换到SSH模式" >&2
}

switch_to_https() {
    git remote set-url origin "$ORIGIN_URL"
    echo "$(date): 已恢复到HTTPS模式" >&2
}

# 检查 Git 仓库状态
if ! git status --porcelain > /dev/null 2>&1; then
    handle_error "无法获取 Git 状态，可能不在 Git 仓库中"
fi

# 检查远程连接 (HTTPS方式)
if ! git ls-remote origin > /dev/null 2>&1; then
    echo "$(date): HTTPS连接失败，尝试SSH模式..." >&2
    switch_to_ssh
    if ! git ls-remote origin > /dev/null 2>&1; then
        switch_to_https
        handle_error "无法连接到远程仓库 origin (HTTPS和SSH都失败)"
    fi
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)

# 如果有本地未提交的改动，先提交
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    if ! git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" > /tmp/git-commit.log 2>&1; then
        handle_error "提交失败: $(cat /tmp/git-commit.log)"
    fi
fi

# 先拉取远程更新（避免冲突）
if ! git pull origin "$CURRENT_BRANCH" --rebase > /tmp/git-pull.log 2>&1; then
    # 如果rebase失败，尝试用merge
    if ! git pull origin "$CURRENT_BRANCH" --no-rebase > /tmp/git-pull.log 2>&1; then
        handle_error "拉取远程更新失败: $(cat /tmp/git-pull.log)"
    fi
fi

# 检查是否有新改动需要推送（pull后可能有merge commit）
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    if ! git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" > /tmp/git-commit.log 2>&1; then
        handle_error "提交失败: $(cat /tmp/git-commit.log)"
    fi
fi

# 推送（只有本地领先远程时才需要）
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "")
if [ "$LOCAL" != "$REMOTE" ]; then
    PUSH_SUCCESS=false
    
    # 首先尝试HTTPS推送
    if git push origin "$CURRENT_BRANCH" > /tmp/git-push.log 2>&1; then
        PUSH_SUCCESS=true
        echo "$(date): HTTPS推送成功"
    else
        HTTPS_ERROR=$(cat /tmp/git-push.log)
        echo "$(date): HTTPS推送失败: $HTTPS_ERROR" >&2
        
        # HTTPS失败，切换到SSH重试
        switch_to_ssh
        
        if git push origin "$CURRENT_BRANCH" > /tmp/git-push-ssh.log 2>&1; then
            PUSH_SUCCESS=true
            echo "$(date): SSH推送成功"
            # 保持SSH模式，下次可能还能用
        else
            SSH_ERROR=$(cat /tmp/git-push-ssh.log)
            echo "$(date): SSH推送也失败: $SSH_ERROR" >&2
            
            # 恢复HTTPS模式
            switch_to_https
            handle_error "推送失败 (HTTPS和SSH都失败). HTTPS: $HTTPS_ERROR | SSH: $SSH_ERROR"
        fi
    fi
fi

echo "$(date): Auto-sync completed successfully"
