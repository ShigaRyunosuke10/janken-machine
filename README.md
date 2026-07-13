# じゃんけんマシン (Janken Machine)

Raspberry Pi 4BとRGB LEDマトリックス、ボタンを使用したイベント展示用じゃんけんゲーム機

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%204B-red.svg)

## 概要

このプロジェクトは、Raspberry Pi 4Bを使用したインタラクティブなじゃんけんゲーム機です。64×64のRGB LEDマトリックス（32×64パネル×2枚）と4つのLED内蔵ボタンで、直感的な操作とビジュアル豊かなゲーム体験を提供します。

## ハードウェア

### 必要な部品

- **Raspberry Pi 4B**
- **RGB LEDマトリックスパネル**: 64×32 P4ピッチ × 2枚（HUB75インターフェース）
- **外部電源**: 5V 8A（LED用）
- **LED内蔵ボタン**: 4個
  - スタートボタン（白）
  - 赤ボタン（グー）
  - 黄ボタン（チョキ）
  - 青ボタン（パー）
- **microSDカード**: 32GB以上推奨

### GPIO配置

| ボタン名 | 色 | 機能 | 入力GPIO | LED出力GPIO |
|----------|-----|------|---------|------------|
| スタートボタン | 白 | ゲーム開始 | GPIO 0 | GPIO 2 |
| 赤ボタン | 赤 | グー選択 | GPIO 1 | GPIO 3 |
| 黄ボタン | 黄 | チョキ選択 | GPIO 16 | GPIO 14 |
| 青ボタン | 青 | パー選択 | GPIO 26 | GPIO 15 |

**LEDマトリックス**: HUB75インターフェース（rgbmatrixライブラリのデフォルトピン）

詳細: [reference/gpio_pinout.md](reference/gpio_pinout.md)

## 機能

### ゲームフロー

1. **スタート待機**: 「スタートをおしてね」表示、スタートボタンLED点滅
2. **カウントダウン + 手選択**: 5秒のカウントダウン中に赤/黄/青ボタンで手を選択（時間切れでスタート画面に戻る）
3. **CPU選択**: CPUがランダムに手を選択
4. **勝敗判定・結果表示**: 対決画面 → 勝敗表示、LED演出
5. **連勝システム**: 勝つと連勝数を表示。「つづきをやる？」で5秒以内にスタートボタンを押すと連勝継続
6. **リセット**: 負け・タイムアウトで連勝リセットしスタート画面へ

さらに、スタート待機中の隠しコマンドでイースターエッグが発動します。

詳細仕様: [docs/GAME_SPEC.md](docs/GAME_SPEC.md)

### LED演出

- **勝利**: 全LED点滅（4回）
- **敗北**: スタートボタンLED点滅（3回）
- **引き分け**: 選択ボタンLED同時点滅（3回）

## インストール

### 1. 環境構築

詳細な環境構築手順: [docs/SETUP.md](docs/SETUP.md)

```bash
# 必要パッケージのインストール
sudo apt update
sudo apt install -y python3-dev python3-pip python3-venv python3-gpiozero \
  libjpeg-dev zlib1g-dev libfreetype6-dev build-essential git cython3

# rgbmatrixライブラリのインストール
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make -C lib
cd bindings/python
sudo make build-python
sudo make install-python

# I2C無効化（GPIO 0/1使用のため）
# /boot/firmware/config.txt で dtparam=i2c_arm=on をコメントアウト
sudo reboot
```

### 2. プロジェクトのクローン

```bash
cd ~
git clone https://github.com/ShigaRyunosuke10/janken-machine.git
cd janken-machine
```

### 3. 自動起動設定（systemdサービス）

```bash
# サービスファイルを配置
sudo cp janken-machine.service /etc/systemd/system/

# サービスを有効化・起動
sudo systemctl daemon-reload
sudo systemctl enable janken-machine.service
sudo systemctl start janken-machine.service

# 状態確認
sudo systemctl status janken-machine.service
```

**電源を入れ直すと自動的にゲームが起動します！**

## 使用方法

### 手動実行

```bash
# メインゲーム実行（sudoが必要）
sudo python3 ~/janken-machine/src/main.py
```

### テストプログラム

Raspberry Pi実機上で実行する動作確認スクリプトです。

```bash
# ボタン入力テスト
python3 ~/janken-machine/tests/test_button_input.py

# ボタンLED出力テスト
sudo python3 ~/janken-machine/tests/test_button_led.py

# LEDマトリックス表示テスト
sudo python3 ~/janken-machine/tests/test_matrix_display.py

# 全画面表示テスト
sudo python3 ~/janken-machine/tests/test_all_screens.py

# ゲームフロー自動テスト（ボタン入力なし）
sudo python3 ~/janken-machine/tests/test_game_flow.py
```

### サービス管理

```bash
# サービス停止
sudo systemctl stop janken-machine.service

# サービス再起動
sudo systemctl restart janken-machine.service

# ログ確認
sudo journalctl -u janken-machine.service -f
```

## ファイル構成

```
janken-machine/
├── src/
│   ├── main.py                    # メインゲームロジック
│   ├── button_controller.py       # ボタン・LED制御モジュール
│   └── matrix_display.py          # LEDマトリックス表示モジュール
├── tests/
│   ├── test_button_input.py       # ボタン入力テスト
│   ├── test_button_led.py         # ボタンLED出力テスト
│   ├── test_matrix_display.py     # LEDマトリックス表示テスト
│   ├── test_all_screens.py        # 全画面表示テスト
│   ├── test_game_flow.py          # ゲームフロー自動テスト
│   └── test_font_offset.py        # フォント描画オフセット調査ツール
├── docs/
│   ├── GAME_SPEC.md               # ゲーム仕様書
│   ├── SETUP.md                   # 環境構築手順（完全版）
│   ├── SD_CARD_SETUP.md           # SDカード書き込み手順
│   └── REMOTE_DEVELOPMENT.md      # リモート開発手順
├── reference/
│   ├── requirements.md            # 要件定義書
│   └── gpio_pinout.md             # GPIO配置仕様
├── janken-machine.service         # systemdサービスファイル
├── CLAUDE.md                      # Claude Code用プロジェクト設定
└── README.md                      # このファイル
```

## トラブルシューティング

### サービスが起動しない

```bash
# ログを確認
sudo journalctl -u janken-machine.service -n 50

# サービス状態を確認
sudo systemctl status janken-machine.service

# 手動実行でエラー確認
sudo python3 ~/janken-machine/src/main.py
```

### LEDマトリックスが表示されない

- 電源電圧確認（5V 8A）
- HUB75ケーブル接続確認
- パネル設定確認（`--led-rows=32 --led-cols=64 --led-chain=2`）

### GPIO 0/1 が反応しない

- I2C無効化確認: `ls /dev/i2c*` で i2c-1 が表示されないこと
- `/boot/firmware/config.txt` で `dtparam=i2c_arm=on` がコメントアウトされていること
- 再起動後に確認

## 技術スタック

- **言語**: Python 3.13
- **GPIO制御**: gpiozero
- **LEDマトリックス**: rpi-rgb-led-matrix (hzeller)
- **OS**: Raspberry Pi OS (64-bit) Lite

## ライセンス

MIT License

## 作者

- **GitHub**: [@ShigaRyunosuke10](https://github.com/ShigaRyunosuke10)
- **リポジトリ**: https://github.com/ShigaRyunosuke10/janken-machine

## 謝辞

- [hzeller/rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) - RGB LED マトリックス制御ライブラリ
- [gpiozero](https://gpiozero.readthedocs.io/) - Raspberry Pi GPIO制御ライブラリ
