#!/usr/bin/env bash
# いまマシンで動いている状態を「安定版」として保存する（GitHub不要）
#
# Pi内部のgitにコミットするだけ。以後 restore.sh はこの状態に戻るようになる。
# ワークショップのセッション終盤に、採用が決まった状態で実行する。
#
# 使い方: bash scripts/save.sh "保存メモ（例: ○○くんのキラキラ演出）"
set -e

PI=janken@192.168.1.142
MSG="${1:-workshop: save stable state}"

ssh "$PI" "cd ~/janken-machine && git add -A && { git diff-index --quiet HEAD && echo '変更なし（すでに保存済み）' || git -c user.name=janken-machine -c user.email=janken@local commit -q -m \"$MSG\"; }"
echo "✅ いまの状態を安定版として保存しました（restore.sh はここに戻ります）"
