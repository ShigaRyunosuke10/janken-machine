# 引き継ぎガイド（新しい開発PCのセットアップ）

このプロジェクトを新しいPC・新しい担当者で引き継ぐための手順。

## 全体像

- コードの正本は GitHub（ShigaRyunosuke10/janken-machine）の main ブランチ
- 実機は Raspberry Pi 4B（`ssh janken@192.168.1.142`、**SSH鍵認証のみ**・パスワード認証は無効）
- 開発ルール・ワークショップ運用は [CLAUDE.md](../CLAUDE.md) に集約（Claude Codeが自動で読む）

## 新PCのセットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/ShigaRyunosuke10/janken-machine.git
```

※ push するには GitHub リポジトリのコラボレータ権限が必要（前任者に招待してもらう）

### 2. SSH鍵の作成とPiへの登録

```bash
# 新PCで鍵を作成（Git Bash / PowerShell どちらでも）
ssh-keygen -t ed25519
```

公開鍵（`~/.ssh/id_ed25519.pub` の中身）をPiの `~/.ssh/authorized_keys` に追記する。方法は2つ:

- **旧PCがまだ使える場合**（推奨・1分で終わる）: 旧PCから
  ```bash
  cat 新PCの公開鍵.pub | ssh janken@192.168.1.142 "cat >> ~/.ssh/authorized_keys"
  ```
- **旧PCがない場合**: PiにHDMIモニタ（micro-HDMI端子）とUSBキーボードをつないでログインし、
  `echo '公開鍵の中身' >> ~/.ssh/authorized_keys` を実行

### 3. 接続確認

```bash
ssh janken@192.168.1.142 echo OK   # OKが返れば成功
bash scripts/deploy.sh             # 実機反映が動けば開発環境は完成
```

### 4. 旧PCの鍵を無効化（セキュリティ）

引き継ぎが完了したら、Piの `~/.ssh/authorized_keys` から旧PCの鍵の行を削除する。

## 引き継ぎ時にやること（チェックリスト）

- [ ] GitHubのコラボレータに後任者を追加（github.com のリポジトリ Settings → Collaborators）
- [ ] Piのユーザーパスワードを後任者に共有（不明なら Pi のコンソールで `sudo passwd janken` で再設定）
- [ ] 新PCで上記セットアップ（クローン・鍵登録・deploy.sh確認）
- [ ] 旧PCの鍵を authorized_keys から削除
- [ ] [docs/WORKSHOP.md](WORKSHOP.md)（イベント進行）と [CLAUDE.md](../CLAUDE.md)（運用ルール）を一読

## 機材・構成の要点

- Pi上のプロジェクトは `~/janken-machine`（git clone、mainと同期して運用）
- `~/janken-machine-old` は旧環境の温存バックアップ（リポジトリ未収録の実験スクリプトあり。消さない）
- ゲームは systemd の `janken-machine.service` で自動起動（root起動→LEDライブラリがdaemonユーザーに権限を落とす）
- 記録ファイル `data/records.json` は daemon 所有・git管理外。`/home/janken` は 711 にしてある
- ハードウェア制約（I2C無効化・マトリックス設定値など）は [CLAUDE.md](../CLAUDE.md) 参照

## 未完了事項（2026-07-15時点）

- [ ] 実機での動作確認2件: 勝利時の「しんきろく」画面 / スタート10秒長押しの記録リセット
- [ ] ワークショップ用ゲームランチャー構想（メニューでゲーム切替、[WORKSHOP.md](WORKSHOP.md) の4時間プラン参照）は未実装
