# CLAUDE.md — janken-machine

Raspberry Pi 4B + RGB LEDマトリックス + ボタンで動くイベント展示用じゃんけんゲーム機。

## プロジェクト概要

- **リポジトリ**: ShigaRyunosuke10/janken-machine
- **実行環境**: Raspberry Pi 4B（Raspberry Pi OS 64-bit Lite）単体で完結。デプロイ先・サーバーなし
- **SSH接続**: `ssh janken@192.168.1.142`
- **自動起動**: systemdサービス（`janken-machine.service`、root実行）

## 技術スタック

- Python 3（PEP 8準拠）
- **GPIO制御**: gpiozero（ボタン入力・ボタンLED出力）
- **LEDマトリックス**: rpi-rgb-led-matrix (hzeller) — 32×64パネル×2枚を parallel=2 で縦連結し64×64
- **描画**: Pillow — PIL Imageを組み立てて `SetImage()` で転送（ちらつき防止のため必須）
- **フォント**: Noto Sans CJK JP 12px（`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`）

## ファイル構成

```
src/
├── main.py               # ゲームループ（JankenGame）
├── button_controller.py  # ボタン入力・ボタンLED制御（ButtonController）
└── matrix_display.py     # LEDマトリックス描画（MatrixDisplay）
tests/                    # Raspberry Pi実機で実行する動作確認スクリプト
├── test_button_input.py  # ボタン入力テスト
├── test_button_led.py    # ボタンLEDテスト
├── test_matrix_display.py# マトリックス表示テスト
├── test_all_screens.py   # 全画面表示テスト
├── test_game_flow.py     # ゲームフロー自動テスト（ボタン入力なし）
└── test_font_offset.py   # フォント描画オフセット調査ツール
scripts/
├── deploy.sh             # 変更を実機に即反映（scp+再起動、コミット不要）
├── restore.sh            # 実機を保存済みの安定版に即復旧
└── save.sh               # いまの状態を安定版として保存（Pi内部git、GitHub不要）
docs/                     # セットアップ・運用手順・ワークショップ資料
reference/                # 要件定義・GPIOピン配置
```

## ハードウェア制約（重要）

- **GPIO 0/1 をボタン入力に使用** → Piの **I2Cを無効化必須**（`/boot/firmware/config.txt` の `dtparam=i2c_arm=on` をコメントアウト）
- ボタンLEDは **active_high=False**（負論理）
- マトリックス設定は動作確認済みの値を変更しないこと:
  `chain_length=1, parallel=2, disable_hardware_pulsing=True, gpio_slowdown=5`
- rgbmatrixはroot権限が必要 → 実行は `sudo python3 src/main.py`

## 開発ワークフロー

実機がないと動作確認できない。開発はPC上で編集し、Piで実行して確認する:

```bash
# PC側: 編集 → コミット → push
git push origin main

# Pi側: 反映 → 再起動
ssh janken@192.168.1.142
cd ~/janken-machine && git pull
sudo systemctl restart janken-machine.service

# ログ確認
sudo journalctl -u janken-machine.service -f
```

単体の動作確認は `tests/` のスクリプトをPi上で実行する（sudo必要、`test_button_input.py` のみ不要）。

## ワークショップモード（最重要の運用形態）

このマシンは **子ども（中学生以上）がAIに日本語で指示してじゃんけんマシンを改造するワークショップ** の機材を兼ねる。成果は広報にも使う。進行ガイドとお題例は [docs/WORKSHOP.md](docs/WORKSHOP.md)。

ワークショップ中のClaudeの動き方:

1. **子どもの発案をそのまま聞く**。曖昧なら「どんな色?」「何秒?」と簡単な質問で具体化する（大人向けの選択肢羅列はしない）
2. **小さく実装 → `bash scripts/deploy.sh` で即反映**（数秒で実機に出る。コミットはまだしない）
3. マシンを見てもらい、気に入らなければその場で調整を繰り返す
4. 動かなくなったら `bash scripts/restore.sh` で即復旧（Pi内部のgitに保存された安定版に戻る）
5. **セッション終盤にまとめて**: 採用された状態で `bash scripts/save.sh "メモ"` を実行（Pi内部で安定版化、GitHub不要）+ [docs/WORKSHOP_LOG.md](docs/WORKSHOP_LOG.md) に「誰が・何を作ったか」を記録（広報素材）

※ GitHubへのpushは必須ではない（バックアップしたい場合のみ任意で）。日常運用は deploy.sh / restore.sh / save.sh の3つで完結する。

ルール:
- 説明は中学生に伝わる言葉で。専門用語には一言の補足を付ける
- 1回の変更は1アイデアずつ。複数の子の案を混ぜて一度に実装しない
- ワークショップ中でもゲームの基本フロー（スタート→選択→勝敗）は壊さない
- 展示の安定性が最優先。実装に迷ったら凝った案より確実に動く案を選ぶ

## ゲーム仕様の要点

仕様の詳細は [docs/GAME_SPEC.md](docs/GAME_SPEC.md) を参照。

- スタート待機 → 5秒カウントダウン中に手選択（赤=グー、黄=チョキ、青=パー）
- 勝つと連勝カウント継続、「つづきをやる？」で5秒以内にスタートボタンで続行
- 負け・タイムアウトで連勝リセットしスタート画面へ
- あいこは連勝中のみ続行確認、連勝0なら即スタート画面へ
- 隠しコマンド: スタート待機中に 赤→黄→青→青→黄→赤 でイースターエッグ

## コーディング規約

- PEP 8準拠、日本語docstring
- ボタン・LED・手の名前は文字列キーで統一: `'start' / 'red' / 'yellow' / 'blue'`、`'rock' / 'scissors' / 'paper'`
- 画面描画は `MatrixDisplay` に集約し、ゲームロジックから直接rgbmatrixを触らない
- LED点滅はスレッドベース（`ButtonController.start_blink`）。停止時は `stop_blink` / `stop_all_blinks` を必ず呼ぶ

## Git運用

- mainブランチのみのシンプル運用
- コミットメッセージ: `<type>: <subject>`（type: feat / fix / docs / refactor / test / chore）
- 禁止: `push --force`、`reset --hard`（ユーザー明示指示除く）
