# 環境構築ガイド

**プロジェクト**: janken-machine
**最終更新**: 2025-10-10

このドキュメントは、じゃんけんマシンの開発・実行環境を構築する手順を記載します。

---

## 前提条件

### ハードウェア
- **Raspberry Pi 4B**
- **RGB LEDマトリックスパネル**: 64×32 × 2枚（P4ピッチ、HUB75インターフェース）
- **外部電源**: 5V 8A（LED用）
- **ボタン**: LED内蔵 × 4個（スタート、赤、黄、青）
- **microSDカード**: 32GB以上推奨
- **開発PC**: Windows/Mac/Linux

### ネットワーク
- WiFiまたはEthernet接続
- 固定IPアドレス推奨（現在: 192.168.1.142）

---

## 1. SDカード準備

詳細手順: [SD_CARD_SETUP.md](SD_CARD_SETUP.md)

### 概要
1. Raspberry Pi Imagerをダウンロード・インストール
2. Raspberry Pi OS (64-bit) Lite を選択
3. 設定（歯車アイコン）:
   - ホスト名: `janken-pi`
   - ユーザー名: `janken`
   - パスワード: 任意の強固なパスワードを設定（リポジトリには記載しない）
   - WiFi設定（SSID・パスワード）
   - SSH有効化（パスワード認証）
4. 書き込み実行

### 初回起動・SSH接続

```bash
# IPアドレス確認（ルーターの管理画面 or Angryなど）
# 例: 192.168.1.142

# SSH接続
ssh janken@192.168.1.142
# パスワード: SDカード書き込み時に設定したもの
```

---

## 2. システム更新

```bash
# パッケージリスト更新
sudo apt update

# インストール済みパッケージを最新版に更新
sudo apt upgrade -y

# 再起動（カーネル更新時）
sudo reboot
```

---

## 3. 必要パッケージのインストール

### Python開発環境

```bash
# Python 3 開発ツール
sudo apt install -y python3-dev python3-pip python3-venv

# gpiozero（GPIO制御ライブラリ）
sudo apt install -y python3-gpiozero

# Pillow依存パッケージ（フォント描画用）
sudo apt install -y libjpeg-dev zlib1g-dev libfreetype6-dev
```

### ビルドツール（rgbmatrix用）

```bash
# C/C++コンパイラ、make、git等
sudo apt install -y build-essential git
```

---

## 4. rpi-rgb-led-matrix ライブラリのインストール

hzellerのrgbmatrixライブラリをビルド・インストールします。

### リポジトリクローン

```bash
cd ~
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
```

### ビルド

```bash
# ライブラリ本体をビルド
make -C lib

# Python バインディングをビルド・インストール
cd bindings/python
sudo python3 setup.py install
```

### 動作確認

```bash
# サンプルプログラム実行（要sudo）
cd ~/rpi-rgb-led-matrix/examples-api-use
sudo ./demo -D0 --led-rows=32 --led-cols=64 --led-chain=2
```

正常に動作すれば、LED マトリックスにデモアニメーションが表示されます。

---

## 5. I2C無効化（GPIO 0/1使用のため）

このプロジェクトではGPIO 0/1をボタン入力に使用するため、デフォルトで有効なI2Cを無効化します。

### /boot/config.txt 編集

```bash
sudo nano /boot/config.txt
```

以下の行を探してコメントアウト（先頭に `#` を追加）:

```
# dtparam=i2c_arm=on
```

保存して終了（Ctrl+O → Enter → Ctrl+X）

### 再起動

```bash
sudo reboot
```

### 確認

```bash
# I2Cデバイスが表示されなければOK
ls /dev/i2c* 2>/dev/null
```

---

## 6. プロジェクトディレクトリ作成

```bash
# ホームディレクトリにプロジェクトフォルダ作成
mkdir -p ~/janken-machine/src

# Pythonソースコード配置先
cd ~/janken-machine
```

---

## 7. 開発用：GitHubリポジトリとの連携

### リポジトリクローン（初回）

```bash
cd ~
git clone https://github.com/ShigaRyunosuke10/janken-machine.git
cd janken-machine
```

### 既存ディレクトリでGit初期化

```bash
cd ~/janken-machine
git init
git remote add origin https://github.com/ShigaRyunosuke10/janken-machine.git
git pull origin main
```

---

## 8. リモート開発環境

詳細手順: [REMOTE_DEVELOPMENT.md](REMOTE_DEVELOPMENT.md)

### 開発PCからRaspberry Piへファイル転送

```bash
# 単一ファイル転送
scp src/main.py janken@192.168.1.142:~/janken-machine/src/

# ディレクトリ全体転送
scp -r src/ janken@192.168.1.142:~/janken-machine/
```

### リモート実行

```bash
# SSH経由でプログラム実行（要sudo）
ssh janken@192.168.1.142 "cd ~/janken-machine && sudo python3 src/main.py"
```

---

## 9. GPIO ピン配置

詳細: [reference/gpio_pinout.md](../reference/gpio_pinout.md)

### ボタン（入力）
- GPIO 0: スタートボタン
- GPIO 1: 赤ボタン（グー）
- GPIO 16: 黄ボタン（チョキ）
- GPIO 26: 青ボタン（パー）

### ボタンLED（出力）
- GPIO 2: スタートボタンLED
- GPIO 3: 赤ボタンLED
- GPIO 14: 黄ボタンLED
- GPIO 15: 青ボタンLED

### LED マトリックス
- HUB75インターフェース（rgbmatrixライブラリがデフォルトピンを使用）

---

## 10. 動作確認

### ボタン入力テスト

```python
# test_button.py
from gpiozero import Button
from signal import pause

start_btn = Button(0)
start_btn.when_pressed = lambda: print("Start pressed!")

print("Press start button...")
pause()
```

実行:
```bash
sudo python3 test_button.py
```

### ボタンLED出力テスト

```python
# test_led.py
from gpiozero import LED
from time import sleep

start_led = LED(2)
start_led.on()
sleep(1)
start_led.off()
```

実行:
```bash
sudo python3 test_led.py
```

---

## トラブルシューティング

### SSH接続できない

- WiFi接続確認（ルーターの管理画面でIPアドレス確認）
- Ethernet接続を試す
- SDカードを再書き込み（WiFi設定・SSH設定を再確認）

### LED マトリックスが表示されない

- 電源電圧確認（5V 8A）
- HUB75ケーブル接続確認
- デモプログラムで動作確認
- パネル設定確認（`--led-rows=32 --led-cols=64 --led-chain=2`）

### GPIO 0/1 が反応しない

- I2C無効化確認（`ls /dev/i2c*` で何も表示されないこと）
- `/boot/config.txt` の `dtparam=i2c_arm=on` がコメントアウトされていること
- 再起動後に確認

---

## 次のステップ

環境構築が完了したら、実装フェーズに進みます：

1. ボタン入力制御の実装
2. ボタンLED制御の実装
3. LED マトリックス表示の実装
4. ゲームロジックの実装
5. 統合テスト

詳細: [DEVELOPMENT.md](DEVELOPMENT.md)（実装時に作成）
