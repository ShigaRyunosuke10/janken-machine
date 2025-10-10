# リモート開発環境セットアップ

**対象**: じゃんけんマシンプロジェクト
**環境**: ローカルPC（Windows） → Raspberry Pi 4B

---

## 1. 概要

Claude CodeがローカルPC（Windows）からSSH経由でRaspberry Piに接続し、コードの作成・転送・実行・デバッグを直接実施します。

### 開発フロー

```
[ローカルPC]
  ├─ コード作成（Python）
  ├─ Git管理
  └─ SSH経由でラズパイ操作
      ↓
[Raspberry Pi]
  ├─ コード受信（git pull / scp）
  ├─ 実行（sudo python3）
  └─ ログ確認
```

---

## 2. 事前準備

### 2.1 Raspberry Pi側の設定

#### (1) SSH有効化

```bash
# ラズパイで実行
sudo raspi-config
# Interface Options → SSH → Enable
```

または

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

#### (2) IPアドレス確認

```bash
# ラズパイで実行
hostname -I
# 例: 192.168.1.100
```

#### (3) ユーザー名確認

デフォルトユーザー（通常 `pi`）またはカスタムユーザー名を確認

---

### 2.2 ローカルPC（Windows）側の設定

#### (1) SSH接続テスト

PowerShellまたはコマンドプロンプトで実行：

```powershell
ssh pi@192.168.1.100
# パスワード入力
```

**接続成功したら準備完了**

#### (2) SSH鍵認証設定（任意、推奨）

パスワード入力を省略するため：

```powershell
# ローカルPCで鍵生成
ssh-keygen -t ed25519 -C "janken-machine"
# Enterキー連打（デフォルト設定）

# 公開鍵をラズパイにコピー
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh pi@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

#### (3) SSH接続エイリアス設定（任意）

`~/.ssh/config` に追加（VSCodeやSSHクライアント用）：

```
Host janken-pi
    HostName 192.168.1.100
    User pi
    IdentityFile ~/.ssh/id_ed25519
```

接続テスト：

```powershell
ssh janken-pi
```

---

## 3. Raspberry Pi環境構築

### 3.1 システム更新

```bash
# ラズパイで実行
sudo apt update
sudo apt upgrade -y
```

### 3.2 必要パッケージのインストール

#### Python 3とpip

```bash
sudo apt install -y python3 python3-pip python3-dev python3-pillow
```

#### GPIO関連

```bash
sudo apt install -y python3-gpiozero python3-rpi.gpio
```

#### ビルドツール（rgbmatrix用）

```bash
sudo apt install -y build-essential git cmake
```

### 3.3 rgbmatrixライブラリのインストール

```bash
# ホームディレクトリに移動
cd ~

# リポジトリクローン
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix

# ビルド
make -C lib

# Pythonバインディングのインストール
cd bindings/python
make build-python
sudo make install-python
```

#### 動作確認

```bash
# サンプル実行（要sudo）
cd ~/rpi-rgb-led-matrix/examples-api-use
sudo python3 runtext.py --led-cols=64 --led-rows=64 --text="TEST"
```

**LEDマトリックスに "TEST" が表示されれば成功**

---

## 4. プロジェクトディレクトリ作成

### 4.1 ラズパイ側

```bash
# ホームディレクトリにプロジェクト用ディレクトリ作成
mkdir -p ~/janken-machine
cd ~/janken-machine

# Gitリポジトリ初期化
git init
```

### 4.2 ローカルPC側

既存のプロジェクトディレクトリ:

```
c:\Users\shiga\Desktop\Dev\janken-machine\
```

---

## 5. Claude Codeによるリモート操作方法

### 5.1 SSH経由でコマンド実行

Claude CodeはBashツールを使用してSSH経由でラズパイを操作します：

```bash
# ローカルPCから実行（Claude Codeが実行）
ssh pi@192.168.1.100 "コマンド"

# 例: ラズパイのPythonバージョン確認
ssh pi@192.168.1.100 "python3 --version"
```

### 5.2 ファイル転送（scp）

#### ローカル → ラズパイ

```bash
scp c:\Users\shiga\Desktop\Dev\janken-machine\src\main.py pi@192.168.1.100:~/janken-machine/
```

#### ディレクトリごと転送

```bash
scp -r c:\Users\shiga\Desktop\Dev\janken-machine\src pi@192.168.1.100:~/janken-machine/
```

### 5.3 Git経由での同期

#### ローカル → GitHub → ラズパイ

```bash
# ローカルでコミット・プッシュ（Claude Code）
git add .
git commit -m "feat: add main game logic"
git push origin main

# ラズパイでプル
ssh pi@192.168.1.100 "cd ~/janken-machine && git pull"
```

---

## 6. 実行・デバッグ

### 6.1 プログラム実行

```bash
# SSH経由で実行（Claude Code）
ssh pi@192.168.1.100 "cd ~/janken-machine && sudo python3 src/main.py"
```

### 6.2 ログ確認

```bash
# 標準出力をリアルタイム表示
ssh pi@192.168.1.100 "cd ~/janken-machine && sudo python3 src/main.py 2>&1 | tee output.log"
```

### 6.3 プロセス停止

```bash
# Ctrl+C が効かない場合
ssh pi@192.168.1.100 "sudo pkill -f main.py"
```

---

## 7. systemdサービス化（自動起動）

### 7.1 サービスファイル作成

```bash
# ラズパイで実行
sudo nano /etc/systemd/system/janken-machine.service
```

**内容**:

```ini
[Unit]
Description=Janken Machine
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/janken-machine
ExecStart=/usr/bin/python3 /home/pi/janken-machine/src/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 7.2 サービス有効化

```bash
# サービス登録
sudo systemctl daemon-reload
sudo systemctl enable janken-machine.service

# 起動
sudo systemctl start janken-machine.service

# 状態確認
sudo systemctl status janken-machine.service

# ログ確認
journalctl -u janken-machine.service -f
```

---

## 8. トラブルシューティング

### 8.1 SSH接続エラー

**エラー**: `Permission denied (publickey,password)`

**対処**:
```bash
# パスワード認証が無効の場合
ssh -o PreferredAuthentications=password pi@192.168.1.100
```

### 8.2 rgbmatrix実行時エラー

**エラー**: `Can't open /dev/mem: Permission denied`

**対処**:
```bash
# sudoで実行
sudo python3 main.py
```

### 8.3 GPIO使用中エラー

**エラー**: `GPIO already in use`

**対処**:
```bash
# 既存プロセスを停止
sudo pkill -f python3
```

---

## 9. 開発時のワークフロー

### Claude Codeの標準フロー

1. **コード作成**: ローカルPCで `src/main.py` を作成・編集
2. **ファイル転送**: `scp` でラズパイに転送
3. **実行**: SSH経由で `sudo python3 main.py` 実行
4. **ログ確認**: 出力を確認
5. **修正**: エラーがあればローカルで修正し、ループ
6. **コミット**: 動作確認後にGitコミット

### コマンド例

```bash
# 1. ファイル転送
scp c:\Users\shiga\Desktop\Dev\janken-machine\src\main.py pi@192.168.1.100:~/janken-machine/src/

# 2. 実行
ssh pi@192.168.1.100 "cd ~/janken-machine && sudo python3 src/main.py"

# 3. ログ確認（リアルタイム）
ssh pi@192.168.1.100 "journalctl -u janken-machine.service -f"
```

---

## 10. 必要情報チェックリスト

Claude Codeがリモート操作を開始する前に、以下の情報を確認してください：

- [ ] **ラズパイのIPアドレス**: `192.168.1.XXX`
- [ ] **ユーザー名**: `pi` または他
- [ ] **パスワード** または **SSH鍵パス**
- [ ] **SSH接続テスト完了**: `ssh user@ip` で接続成功
- [ ] **rgbmatrixライブラリインストール済み**
- [ ] **プロジェクトディレクトリ作成済み**: `~/janken-machine`

---

## 変更履歴

| 日付 | 変更内容 | 担当 |
|------|----------|------|
| 2025-10-10 | 初版作成 | AI |
