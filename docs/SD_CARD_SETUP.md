# Raspberry Pi OS - SDカード書き込み手順

**対象**: じゃんけんマシンプロジェクト（Raspberry Pi 4B）
**OS**: Raspberry Pi OS (64-bit)

---

## 1. 必要なもの

### ハードウェア
- **microSDカード**: 16GB以上推奨（32GB以上が理想）
- **SDカードリーダー**: PC接続用
- **Raspberry Pi 4B**

### ソフトウェア
- **Raspberry Pi Imager**: 公式書き込みツール
- **Windows PC**: 書き込み作業用

---

## 2. SSH鍵の生成（推奨）

### 2.1 SSH鍵ペアの生成

セキュアな接続のため、SSH鍵認証を推奨します。

PowerShellまたはコマンドプロンプトで実行：

```powershell
# Ed25519形式の鍵を生成（推奨）
ssh-keygen -t ed25519 -C "janken-machine"
```

実行結果：

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (C:\Users\shiga/.ssh/id_ed25519):
```

→ **Enterキー**を押す（デフォルトパスを使用）

```
Enter passphrase (empty for no passphrase):
```

→ **Enterキー**を押す（パスフレーズなし、または任意のパスフレーズを入力）

```
Enter same passphrase again:
```

→ 再度**Enterキー**（または同じパスフレーズ）

```
Your identification has been saved in C:\Users\shiga/.ssh/id_ed25519
Your public key has been saved in C:\Users\shiga/.ssh/id_ed25519.pub
```

**鍵生成完了！**

### 2.2 公開鍵の確認

公開鍵の内容を表示：

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub
```

**出力例**:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx janken-machine
```

→ この内容を**コピー**しておく（Raspberry Pi Imagerで使用）

---

## 3. Raspberry Pi Imager のインストール

### 3.1 ダウンロード

公式サイトからダウンロード:
https://www.raspberrypi.com/software/

**Windows版**: `imager_latest.exe`

### 3.2 インストール

1. ダウンロードした `imager_latest.exe` を実行
2. インストールウィザードに従って進む
3. インストール完了後、Raspberry Pi Imagerを起動

---

## 4. SDカードの書き込み

### 4.1 SDカードをPCに接続

1. microSDカードをSDカードリーダーに挿入
2. PCのUSBポートに接続
3. Windowsがドライブを認識するのを待つ

### 4.2 Raspberry Pi Imagerで書き込み

#### (1) OSを選択

Raspberry Pi Imagerを起動し、以下を選択：

1. **「デバイスを選択」** → **Raspberry Pi 4**
2. **「OSを選択」** → **Raspberry Pi OS (64-bit)** (推奨)
   - フルパス: `Raspberry Pi OS (other)` → `Raspberry Pi OS (64-bit)`

**推奨**: Raspberry Pi OS (64-bit) Lite（デスクトップ環境なし、軽量）
- じゃんけんマシンはGUI不要のため、Lite版で十分

#### (2) ストレージを選択

3. **「ストレージを選択」** → **挿入したmicroSDカード**を選択
   - 容量を確認して間違えないように注意

#### (3) 詳細設定（重要）

4. **歯車アイコン（⚙️）** または **「設定を編集する」** をクリック

以下を設定：

##### ホスト名
- ☑ **ホスト名を設定する**: `janken-pi`（任意の名前）

##### ユーザー名とパスワード
- ☑ **ユーザー名とパスワードを設定する**
  - **ユーザー名**: `pi`（推奨）または任意
  - **パスワード**: 任意の強固なパスワード

##### Wi-Fi設定
- ☑ **Wi-Fiを設定する**
  - **SSID**: 自宅/会場のWi-Fi名
  - **パスワード**: Wi-Fiパスワード
  - **ワイヤレスLANの国**: `JP`（日本）

##### ロケール設定
- ☑ **ロケール設定をする**
  - **タイムゾーン**: `Asia/Tokyo`
  - **キーボードレイアウト**: `jp`

##### SSH有効化（重要）
- ☑ **SSHを有効化する**
  - **公開鍵認証のみを許可する** を選択（推奨、セキュア）
  - または **パスワード認証を使う**（簡単だがセキュリティ低）

**公開鍵認証を選択する場合（推奨）**:
1. **事前にSSH鍵ペアを生成**（下記「SSH鍵の生成」参照）
2. 公開鍵（`~/.ssh/id_ed25519.pub`の内容）をコピー
3. Raspberry Pi Imagerの設定画面に貼り付け

#### (4) 書き込み開始

5. **「次へ」** → **「はい」** をクリック
6. 「既存データが消去されます」の警告 → **「はい」** をクリック
7. 書き込み開始（数分〜10分程度）
8. 「書き込みが成功しました」と表示されたら完了

### 4.3 SDカードを取り出し

1. **「続ける」** をクリック
2. SDカードをPCから安全に取り外し
3. Raspberry Pi 4BのmicroSDカードスロットに挿入

---

## 5. Raspberry Pi の初回起動

### 5.1 電源投入

1. microSDカードをRaspberry Piに挿入
2. 電源（5V 3A）を接続
3. 緑LEDが点滅開始（起動中）
4. 初回起動は1〜2分かかる

### 5.2 IPアドレス確認

#### 方法1: ルーター管理画面で確認
1. ルーター管理画面にアクセス
2. 接続デバイス一覧から `janken-pi` を探す
3. IPアドレスをメモ（例: `192.168.1.100`）

#### 方法2: ラズパイにモニター・キーボード接続
1. HDMIモニターとUSBキーボードを接続
2. ログイン（ユーザー名: `pi`、パスワード: 設定したもの）
3. 以下コマンドを実行:
   ```bash
   hostname -I
   ```
4. 表示されたIPアドレスをメモ

#### 方法3: ネットワークスキャン（Advanced IP Scanner等）
1. Advanced IP Scannerをダウンロード・起動
2. 同一ネットワークをスキャン
3. `janken-pi` または `raspberrypi` を探す

---

## 6. SSH接続テスト

### 6.1 ローカルPCからSSH接続（鍵認証）

公開鍵を設定した場合、パスワード不要で接続できます：

PowerShellまたはコマンドプロンプトで実行：

```powershell
ssh pi@192.168.1.100
# IPアドレスは実際のものに置き換え
```

#### 初回接続時の警告

```
The authenticity of host '192.168.1.100' can't be established.
ECDSA key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

→ **`yes`** を入力してEnter

#### パスワード入力

```
pi@192.168.1.100's password:
```

→ 設定したパスワードを入力

#### 接続成功

```
Linux janken-pi 6.1.0-rpi7-rpi-v8 #1 SMP PREEMPT Debian 1:6.1.63-1+rpt1 (2023-11-24) aarch64
...
pi@janken-pi:~ $
```

**接続成功！** プロンプトが表示されたら成功です。

---

## 7. 初期設定（オプション）

### 7.1 システム更新

SSH接続後、以下を実行：

```bash
sudo apt update
sudo apt upgrade -y
```

### 7.2 I2C無効化（GPIO 0/1を使用するため）

ボタン入力にGPIO 0/1を使用するため、I2Cを無効化：

```bash
sudo raspi-config
```

- **Interface Options** → **I2C** → **No**

または、直接設定ファイルを編集：

```bash
sudo nano /boot/config.txt
```

以下を追加：

```
dtparam=i2c_arm=off
```

保存して再起動：

```bash
sudo reboot
```

### 7.3 タイムゾーン確認

```bash
timedatectl
```

`Time zone: Asia/Tokyo` となっていればOK

---

## 8. トラブルシューティング

### 8.1 SSH接続できない

#### 確認事項
- [ ] ラズパイの電源が入っているか（緑LED点滅確認）
- [ ] Wi-Fi設定が正しいか（SSID/パスワード）
- [ ] IPアドレスが正しいか
- [ ] SSHが有効化されているか

#### 対処法

**モニター・キーボードを接続して確認**:

```bash
# SSH状態確認
sudo systemctl status ssh

# SSHが無効の場合、有効化
sudo systemctl enable ssh
sudo systemctl start ssh

# IPアドレス確認
hostname -I

# Wi-Fi接続確認
iwconfig
```

### 8.2 Wi-Fi接続できない

#### 手動でWi-Fi設定

```bash
sudo raspi-config
```

- **System Options** → **Wireless LAN**
- SSIDとパスワードを入力

または：

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

以下を追加：

```
network={
    ssid="Wi-Fi名"
    psk="パスワード"
    key_mgmt=WPA-PSK
}
```

再起動：

```bash
sudo reboot
```

### 7.3 書き込みエラー

#### 確認事項
- [ ] SDカードが正常か（別のSDカードで試す）
- [ ] SDカードリーダーが正常か
- [ ] 書き込み中にケーブルが抜けなかったか

#### 対処法
- SDカードをフォーマット（FAT32）してから再度書き込み
- 別のSDカードリーダーを使用

---

## 8. 次のステップ

SDカードの書き込みとSSH接続が完了したら、次のステップへ：

1. **[リモート開発環境セットアップ](REMOTE_DEVELOPMENT.md)** - SSH経由での開発環境構築
2. **Raspberry Pi環境構築** - 必要パッケージのインストール
3. **プロジェクトディレクトリ作成**
4. **実装開始**

---

## 変更履歴

| 日付 | 変更内容 | 担当 |
|------|----------|------|
| 2025-10-10 | 初版作成 | AI |
