#!/bin/bash
set -e

cd "$(dirname "$0")"

PORT="8080"
HTML_FILE="ev3620-user-guide.html"
TOOL_FILE="qr-tool.html"

LAN_IP="$(ipconfig getifaddr en0 2>/dev/null || true)"
if [ -z "$LAN_IP" ]; then
  LAN_IP="$(ifconfig en0 | awk '/inet / {print $2; exit}')"
fi

if [ -z "$LAN_IP" ]; then
  echo "没有找到当前电脑的局域网 IP。请确认电脑已连接 Wi-Fi。"
  read -r -p "按回车退出..."
  exit 1
fi

if ! curl -s "http://127.0.0.1:${PORT}/${TOOL_FILE}" >/dev/null 2>&1; then
  python3 -m http.server "$PORT" --bind 0.0.0.0 >/tmp/ev3620-qr-tool-server.log 2>&1 &
  sleep 1
fi

TARGET_URL="http://${LAN_IP}:${PORT}/${HTML_FILE}"
TOOL_URL="http://${LAN_IP}:${PORT}/${TOOL_FILE}?target=${TARGET_URL}"

open "$TOOL_URL"

echo "二维码生成工具已打开。"
echo "二维码内容：${TARGET_URL}"
echo ""
echo "请保持这个窗口不要关闭；关闭后本地服务可能停止。"
echo "手机和电脑需要连接同一个 Wi-Fi。"
read -r -p "按回车关闭这个窗口..."
