#!/usr/bin/env bash
# 変更をじゃんけんマシンに即反映する（クイック反映・git不要）
#
# PC上の src/ をそのままマシンに転送してゲームを再起動する。
# ワークショップ中の試行錯誤はこれで回し、採用が決まったものだけ
# セッション末に commit & push する（CLAUDE.md「ワークショップモード」参照）。
#
# 使い方: bash scripts/deploy.sh
set -e
cd "$(dirname "$0")/.."

PI=janken@192.168.1.142

python -m py_compile src/*.py   # 構文エラーのまま送らない
scp -q src/*.py "$PI:~/janken-machine/src/"
ssh "$PI" 'sudo systemctl restart janken-machine.service'
sleep 2
ssh "$PI" 'systemctl is-active janken-machine.service' >/dev/null \
  && echo "✅ 反映完了! マシンを見てね" \
  || { echo "❌ ゲームが起動していない。scripts/restore.sh で戻せます"; exit 1; }
