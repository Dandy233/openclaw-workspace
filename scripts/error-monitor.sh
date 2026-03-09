#!/bin/bash
# Error Monitor Script
# 检查脚本错误日志，生成报告

ERROR_LOG="/var/log/openclaw-script-errors.log"
REPORT_FILE="/tmp/openclaw-error-report.txt"

# 如果错误日志不存在或为空，直接退出
if [ ! -f "$ERROR_LOG" ] || [ ! -s "$ERROR_LOG" ]; then
    echo "NO_ERRORS"
    exit 0
fi

# 获取最近一小时的错误（默认检查最近一小时）
TIME_WINDOW="${1:-1 hour ago}"
REPORT_CONTENT=$(echo "=== OpenClaw 脚本错误报告 ===" > "$REPORT_FILE")
echo "生成时间: $(date)" >> "$REPORT_FILE"
echo "检查窗口: $TIME_WINDOW" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 提取最近的错误（简单实现：取最后20行）
tail -20 "$ERROR_LOG" >> "$REPORT_FILE"

# 清空已报告的错误（避免重复报告）
# 保留最后5行作为上下文
if [ $(wc -l < "$ERROR_LOG") -gt 5 ]; then
    tail -5 "$ERROR_LOG" > "$ERROR_LOG.tmp"
    mv "$ERROR_LOG.tmp" "$ERROR_LOG"
fi

cat "$REPORT_FILE"
