# プロジェクト初期化進捗

**プロジェクト名**: janken-machine
**最終更新**: 2025-10-10
**現在のステップ**: ステップ3 (初期設定・ドキュメント整備) - ほぼ完了

---

## ステップ-1: Serenaメモリ初期化
- [x] プロジェクトアクティベート
- [x] 初期化進捗メモリ作成
- [x] 作成ファイル管理台帳作成
- [x] TodoList作成

## ステップ0: 要件定義
- [x] Phase 1: プロジェクト概要のヒアリング
- [x] Phase 2: 機能要件の詳細化
- [x] Phase 3: 非機能要件の確認
- [x] Phase 4: 参考資料の確認
- [x] requirements.md作成
- [x] gpio_pinout.md作成

## ステップ1: 技術選定・資料準備
- [x] Python 3 + rgbmatrix + gpiozero で決定
- [x] 技術選定理由を記録
- [x] SD_CARD_SETUP.md作成
- [x] REMOTE_DEVELOPMENT.md作成

## 物理作業（並行実施、フローB採用）
- [x] SDカード書き込み手順書作成
- [x] リモート開発手順書作成
- [x] SDカード書き込み完了
- [x] Raspberry Pi起動
- [x] SSH接続確立（janken@192.168.1.142）
- [x] システム更新完了

## ステップ2: ルール・ワークフロー策定
- [x] プロジェクト固有ルールの確認（シンプルなプロジェクトのため最小限）
- [x] ワークフローのカスタマイズ（フローB: 物理優先）
- [x] ai-rules/のカスタマイズ（必要に応じて）

## ステップ3: 初期設定・ドキュメント整備
- [x] Step 3-1: プロジェクト固有要件のヒアリング
  - [x] GitHub設定確認（ShigaRyunosuke10/janken-machine）
  - [x] デプロイ先確認（なし、Raspberry Pi単体）
  - [x] 外部サービス確認（Context7/Playwright不要）
- [x] Step 3-2: .mcp.json設定
  - [x] GitHub Token設定
  - [x] 不要なMCP（Context7, Playwright, Netlify）はプレースホルダー維持
- [x] Step 3-3: CLAUDE.mdのプレースホルダー更新
  - [x] {{PROJECT_NAME}} → janken-machine
  - [x] {{GITHUB_OWNER}}/{{GITHUB_REPO}} → ShigaRyunosuke10/janken-machine
  - [x] 技術スタック記載
  - [x] MCP設定セクション更新
- [x] Step 3-4: Serenaメモリ初期化（ローカルファイル代替）
- [ ] Step 3-5: 基本ドキュメントの作成
  - [ ] docs/SETUP.md（環境構築手順）
  - [ ] docs/DEVELOPMENT.md（開発ガイド、必要に応じて）

## ステップ4: 環境構築
- [x] Raspberry Pi OS起動
- [x] SSH接続確立
- [x] システム更新（apt update/upgrade）
- [ ] 必要パッケージのインストール
  - [ ] Python開発環境
  - [ ] GPIO関連
  - [ ] ビルドツール
- [ ] rgbmatrixライブラリのインストール
- [ ] I2C無効化（GPIO 0/1使用のため）
- [ ] プロジェクトディレクトリ作成

## 実装フェーズ
- [ ] MVP実装
  - [ ] ボタン入力テスト
  - [ ] ボタンLED出力テスト
  - [ ] LEDマトリックス表示テスト
  - [ ] ゲームロジック実装
  - [ ] 統合テスト

---

## 採用した開発フロー

**フローB: 物理優先（ハードウェアプロジェクト向け）**

理由: ユーザーがSDカード書き込み等の物理作業を優先したため、フローBを採用。
ステップ2・3はステップ4と並行して実施。
