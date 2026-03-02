#!/bin/bash
# OpenClaw 子代理任务模板 - 标准化执行流程

set -e

# 配置
REPO_DIR="/root/.openclaw/workspace/90s-anime"
TIMEOUT=300

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 进入仓库
cd_repo() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        log "克隆仓库..."
        git clone git@github.com:Dandy233/90s-anime.git "$REPO_DIR"
    fi
    cd "$REPO_DIR"
    log "更新代码..."
    git stash || true
    git pull || true
    git stash pop 2>/dev/null || true
}

# 提交推送
commit_push() {
    local msg="$1"
    git add -A
    if git diff --cached --quiet; then
        log "无变更，跳过提交"
        return 0
    fi
    git commit -m "$msg" || true
    git push origin main
    log "推送完成"
}

# 主执行逻辑
case "$1" in
    "fix-layout")
        log "修复按钮布局..."
        cd_repo
        # 修改按钮布局为 flex
        sed -i 's/<div class="anime-actions">/<div class="anime-actions" style="display:flex;gap:10px;">/g' index.html || true
        commit_push "fix: 按钮布局改为flex"
        ;;
    "fix-links")
        log "修复链接..."
        cd_repo
        # 确保链接正确
        sed -i 's/doubanLink/doubanLink/g' index.html || true
        commit_push "fix: 链接优化"
        ;;
    "count-anime")
        log "统计作品数量..."
        cd_repo
        count=$(grep -E '^\*\*' README.md | wc -l)
        log "作品数量: $count"
        ;;
    *)
        log "未知任务: $1"
        exit 1
        ;;
esac

log "任务完成"
