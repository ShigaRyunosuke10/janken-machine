# テンプレート削除前のTODOリスト

このファイルは、テンプレートを実際のプロジェクトに適用する際の最終チェックリストです。
**全ての項目を完了したら、このファイルを削除してください。**

---

## ステップ0〜2: プロジェクト立ち上げ準備

### ✅ ステップ0: プロジェクト企画

- [ ] プロジェクト名を決定
- [ ] 作りたいものを明確化
- [ ] 参考資料を `reference/` に配置
- [ ] 技術スタック候補を選定

### ✅ ステップ0.5: 要件定義詳細化（AIとやり取り）

- [ ] 参考資料をAIと確認
- [ ] 機能要件を詳細化
- [ ] 非機能要件を整理
- [ ] 技術スタックを最終決定
- [ ] 開発スケジュールを策定

### ✅ ステップ1: ルール・ワークフロー策定

- [ ] コーディング規約を決定
- [ ] Git運用ルールを決定
- [ ] レビュー基準を定義
- [ ] フェーズ管理の要否を決定
- [ ] `ai-rules/_project_template/` をカスタマイズ

### ✅ ステップ2: 初期設定・ドキュメント整備

#### CLAUDE.md プレースホルダー更新

- [ ] `{{PROJECT_NAME}}` → 実際のプロジェクト名
- [ ] `{{GITHUB_OWNER}}/{{GITHUB_REPO}}` → GitHubリポジトリ
- [ ] `{{FRONTEND_PORT}}` → フロントエンドポート番号
- [ ] `{{BACKEND_PORT}}` → バックエンドポート番号
- [ ] `{{TEST_USER_EMAIL}}` → テストユーザーメールアドレス
- [ ] `{{CURRENT_DATE}}` → 現在の日付（YYYY-MM-DD形式）
- [ ] 技術スタックを記載（フロントエンド、バックエンド、DB）

#### DEPLOYMENT.md プレースホルダー更新

- [ ] `{{STAGING_SITE_ID}}` → Netlify ステージングサイトID
- [ ] `{{PRODUCTION_SITE_ID}}` → Netlify 本番サイトID
- [ ] `{{BACKEND_DEPLOY_METHOD}}` → バックエンドデプロイ方法
- [ ] `{{DATABASE_DEPLOY_METHOD}}` → データベースデプロイ方法
- [ ] バックアップコマンドを記載
- [ ] マイグレーションコマンドを記載
- [ ] ロールバックコマンドを記載

#### OPERATIONS.md プレースホルダー更新

- [ ] `{{MONITORING_TOOL}}` → 監視ツール名
- [ ] `{{ERROR_TRACKING}}` → エラートラッキングツール名
- [ ] `{{LOG_STORAGE}}` → ログ保存先
- [ ] `{{BACKUP_STORAGE}}` → バックアップ保存先
- [ ] `{{SLACK_CHANNEL}}` → Slack通知チャンネル
- [ ] `{{ALERT_EMAIL}}` → アラート通知メール
- [ ] バックアップスクリプトを作成

#### .mcp.json 確認

- [ ] GitHub Personal Access Token 設定済み
- [ ] Netlify Personal Access Token 設定済み
- [ ] その他必要なAPIキー設定済み

#### Serenaメモリ初期化

- [ ] `current_issues_and_priorities.md` 作成
- [ ] `session_handover.md` 作成
- [ ] `requirements_specifications.md` 作成（要件定義内容）
- [ ] `phase_progress.md` 作成（フェーズ管理する場合）
- [ ] `database_specifications.md` 作成（必要に応じて）
- [ ] `api_specifications.md` 作成（必要に応じて）

#### 基本ドキュメント作成

- [ ] `docs/REQUIREMENTS.md` 作成（要件定義書）
- [ ] `docs/SETUP.md` 作成（環境構築手順の雛形）
- [ ] `docs/API.md` 作成（空の雛形）
- [ ] `docs/DATABASE.md` 作成（空の雛形）
- [ ] `docs/PHASES.md` 作成（フェーズ管理する場合）
- [ ] `docs/DEVELOPMENT_RULES.md` 作成（任意）

### ✅ ステップ3: 環境構築

- [ ] `docker-compose.yml` 作成
- [ ] フロントエンドプロジェクト初期化
- [ ] バックエンドプロジェクト初期化
- [ ] データベーススキーマ定義
- [ ] 開発サーバー起動確認
- [ ] 各サービス間の疎通確認
- [ ] `docs/SETUP.md` に環境構築手順を記載

---

## プロジェクト固有のカスタマイズ

### 必須カスタマイズ

#### WORKFLOW.md

- [ ] ブランチ命名規則をプロジェクトに合わせてカスタマイズ
- [ ] コミットメッセージ形式をカスタマイズ（必要に応じて）

#### NAMING_CONVENTIONS.md

- [ ] プロジェクト固有の命名規則を追加
- [ ] 技術スタック固有の規則を追加

#### TESTING.md

- [ ] プロジェクト固有のテスト戦略を記載
- [ ] テストカバレッジ目標を設定

---

## デプロイ・運用設定

### Netlify 設定

- [ ] ステージング環境サイト作成
- [ ] 本番環境サイト作成
- [ ] 環境変数設定
- [ ] ビルド設定
- [ ] デプロイ通知設定

### バックエンドデプロイ設定

- [ ] デプロイ先決定（AWS, Heroku, Vercel等）
- [ ] デプロイスクリプト作成
- [ ] 環境変数設定
- [ ] CI/CD 設定（オプション）

### 監視・アラート設定

- [ ] エラートラッキングツール導入（Sentry等）
- [ ] 監視ツール設定
- [ ] アラート通知先設定（Slack, Email等）
- [ ] ログ保存設定

### バックアップ設定

- [ ] データベースバックアップスクリプト作成
- [ ] cron設定（自動バックアップ）
- [ ] バックアップ保存先設定
- [ ] 復旧手順の動作確認

---

## セキュリティ設定

- [ ] HTTPS 設定
- [ ] CORS 設定
- [ ] CSRFトークン実装
- [ ] レート制限実装
- [ ] 環境変数・シークレット管理確認
- [ ] 脆弱性スキャン設定（週次）

---

## ドキュメント整備

### 必須ドキュメント

- [ ] `docs/REQUIREMENTS.md` - 要件定義が記載されている
- [ ] `docs/SETUP.md` - 環境構築手順が記載されている
- [ ] `docs/DATABASE.md` - DBスキーマが記載されている
- [ ] `docs/API.md` - API仕様が記載されている（雛形のみでもOK）

### フェーズ管理する場合

- [ ] `docs/PHASES.md` - フェーズ定義が記載されている
- [ ] Serenaメモリ `phase_progress.md` が作成されている

### 環境変数ドキュメント（推奨）

- [ ] `docs/ENV_VARS.md` - 環境変数一覧を作成
  ```markdown
  # 環境変数一覧

  | 変数名 | 用途 | 環境 | 例 |
  |--------|------|------|-----|
  | API_KEY | 外部API認証 | Production | sk_live_xxx |
  | DATABASE_URL | DB接続 | All | postgresql://... |
  ```

---

## テスト・品質確認

- [ ] E2Eテストが動作する
- [ ] e2e-tester サブエージェントが使用可能
- [ ] code-reviewer サブエージェントが使用可能
- [ ] docs-updater サブエージェントが使用可能
- [ ] ローカルでビルドが通る
- [ ] ステージング環境でデプロイが成功する

---

## 最終チェック

### 設定ファイル

- [ ] `.gitignore` が正しく設定されている
- [ ] `.env.example` を作成（値は空）
- [ ] `.mcp.json` に必要なAPIキーが設定されている
- [ ] `package.json` のスクリプトが正しい

### ドキュメント

- [ ] README.md が更新されている
- [ ] CLAUDE.md のプレースホルダーが全て更新されている
- [ ] 各種 TODO や FIXME コメントを確認
- [ ] reference/ に必要な資料が配置されている

### Git

- [ ] GitHubリポジトリが作成されている
- [ ] main ブランチが保護されている（設定推奨）
- [ ] 初回コミット・プッシュ完了

---

## 削除すべきファイル（完了後）

このチェックリストが全て完了したら、以下のファイルを削除してください：

- [ ] `TODO_BEFORE_DELETE.md`（このファイル）
- [ ] `ai-rules/_project_template/PROJECT_INITIALIZATION_CHECKLIST.md`（重複）

---

## 実装フェーズ開始の準備完了確認

全てのチェックリストが完了したら、以下を最終確認：

- [ ] 開発環境が正常に動作する
- [ ] ドキュメントが整備されている
- [ ] Serenaメモリが初期化されている
- [ ] デプロイフローが確立している
- [ ] 運用フローが確立している

✅ **全て完了したら、実装フェーズ（Phase 1）を開始できます！**

詳細: [ai-rules/_project_template/WORKFLOW.md](ai-rules/_project_template/WORKFLOW.md)

---

## 備考

- このテンプレートは Claude Code で AI と協働開発することを前提に設計されています
- 不明点があれば CLAUDE.md や各ガイドラインを参照してください
- プロジェクト固有のルールは積極的にカスタマイズしてください
