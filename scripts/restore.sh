#!/usr/bin/env bash
# じゃんけんマシンを最後の安定版（GitHubのmain）に戻す
#
# deploy.sh で転送した未コミットの変更をすべて破棄して再起動する。
# 改造が動かなくなった・変になったときの緊急復旧用。
#
# 使い方: bash scripts/restore.sh
set -e

PI=janken@192.168.1.142

ssh "$PI" 'cd ~/janken-machine && git restore src/ && sudo systemctl restart janken-machine.service'
sleep 2
ssh "$PI" 'systemctl is-active janken-machine.service' >/dev/null \
  && echo "✅ 安定版に戻しました" \
  || { echo "❌ 復旧失敗。ログ確認: ssh '"$PI"' sudo journalctl -u janken-machine.service -n 30"; exit 1; }
