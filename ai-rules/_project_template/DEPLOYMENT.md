# デプロイ・リリースガイド（{{PROJECT_NAME}} 専用）

このドキュメントでは、デプロイとリリースのフローを定義します。

**プロジェクト固有**: このファイルは {{PROJECT_NAME}} プロジェクト専用の設定を含みます。

**最終更新**: {{CURRENT_DATE}}

---

## 概要

### デプロイ環境

- **開発環境（Development）**: ローカル開発環境（Docker）
- **ステージング環境（Staging）**: 本番同等の検証環境
- **本番環境（Production）**: エンドユーザー向け環境

### デプロイ方法

- **Netlify MCP**: フロントエンドのデプロイ
- **[バックエンドのデプロイ方法]**: {{BACKEND_DEPLOY_METHOD}}（例: AWS, Vercel, Heroku等）
- **[データベース]**: {{DATABASE_DEPLOY_METHOD}}

---

## 1. ステージング環境へのデプロイ

### 1.1 前提条件

- [ ] main ブランチが最新状態
- [ ] 全テストが通過（E2E含む）
- [ ] code-reviewer レビュー完了
- [ ] ドキュメント更新完了

### 1.2 フロントエンドデプロイ（Netlify）

```bash
# Netlify MCP を使用してステージング環境にデプロイ

# 1. ビルド確認
cd frontend
npm run build

# 2. Netlify へデプロイ
mcp__netlify__create_deploy
  site_id: "{{STAGING_SITE_ID}}"
  deploy_dir: "frontend/dist"
  draft: true  # ドラフトデプロイ（本番前確認用）

# 3. デプロイURL確認
# → 返却されたURLで動作確認
```

### 1.3 バックエンドデプロイ

```bash
# [プロジェクト固有のデプロイ方法]
# 例: Heroku, AWS, Vercel等

# TODO: バックエンドのデプロイ方法を記載
```

### 1.4 データベースマイグレーション

```bash
# ステージング環境でマイグレーション実行

# 1. バックアップ取得（必須）
# [バックアップコマンド]

# 2. マイグレーション実行
# [マイグレーションコマンド]

# 3. 動作確認
# [確認コマンド]
```

### 1.5 ステージング動作確認

- [ ] 全機能の動作確認
- [ ] E2Eテスト実行（ステージング環境）
- [ ] パフォーマンステスト
- [ ] セキュリティチェック
- [ ] レスポンシブデザイン確認
- [ ] ブラウザ互換性確認

---

## 2. 本番環境へのデプロイ

⚠️ **重要**: 本番デプロイは慎重に実施してください

### 2.1 前提条件

- [ ] ステージング環境で全確認完了
- [ ] リリースノート作成完了
- [ ] バックアップ取得完了
- [ ] ロールバック手順確認済み
- [ ] 関係者への通知完了

### 2.2 リリースノート作成

```markdown
# Release v{{VERSION}} - {{RELEASE_DATE}}

## 新機能
- [機能名]: [説明]
- [機能名]: [説明]

## 改善
- [改善内容]: [説明]

## バグ修正
- [修正内容]: [説明]

## 破壊的変更
- [変更内容]: [影響範囲と対応方法]

## 既知の問題
- [問題]: [回避方法]
```

リリースノートは `docs/RELEASES/` に保存

### 2.3 バージョンタグ作成

```bash
# セマンティックバージョニング: MAJOR.MINOR.PATCH
# - MAJOR: 破壊的変更
# - MINOR: 後方互換性のある機能追加
# - PATCH: 後方互換性のあるバグ修正

git checkout main
git pull
git tag -a v{{VERSION}} -m "Release v{{VERSION}}"
git push origin v{{VERSION}}
```

### 2.4 フロントエンドデプロイ（本番）

```bash
# 1. ビルド
cd frontend
npm run build

# 2. Netlify 本番デプロイ
mcp__netlify__create_deploy
  site_id: "{{PRODUCTION_SITE_ID}}"
  deploy_dir: "frontend/dist"
  draft: false  # 本番デプロイ

# 3. デプロイ完了確認
mcp__netlify__get_site
  site_id: "{{PRODUCTION_SITE_ID}}"
```

### 2.5 バックエンドデプロイ（本番）

```bash
# [プロジェクト固有のデプロイ方法]

# TODO: 本番バックエンドのデプロイ方法を記載
```

### 2.6 データベースマイグレーション（本番）

⚠️ **超重要**: 必ずバックアップを取得してから実施

```bash
# 1. バックアップ取得（必須）
# [バックアップコマンド]
# → バックアップファイル保存先: [パス]

# 2. メンテナンスモード開始（必要に応じて）
# [メンテナンスモード開始コマンド]

# 3. マイグレーション実行
# [マイグレーションコマンド]

# 4. 動作確認
# [確認コマンド]

# 5. メンテナンスモード解除
# [メンテナンスモード解除コマンド]
```

### 2.7 本番動作確認

- [ ] トップページ表示確認
- [ ] 主要機能の動作確認（5分以内）
- [ ] エラーログ確認
- [ ] パフォーマンス確認
- [ ] 外部API連携確認（ある場合）

### 2.8 デプロイ完了報告

```
# 関係者へ通知

件名: [{{PROJECT_NAME}}] v{{VERSION}} リリース完了

本文:
{{PROJECT_NAME}} v{{VERSION}} のリリースが完了しました。

- リリース日時: {{RELEASE_DATETIME}}
- デプロイURL: {{PRODUCTION_URL}}
- リリースノート: [リンク]

主な変更内容:
- [変更1]
- [変更2]

何か問題があればご連絡ください。
```

---

## 3. 環境変数・シークレット管理

### 3.1 環境変数の追加・変更

```bash
# Netlify 環境変数設定
mcp__netlify__update_env_vars
  site_id: "{{SITE_ID}}"
  env_vars: {
    "API_URL": "{{API_URL}}",
    "API_KEY": "{{API_KEY}}"  # シークレット
  }

# バックエンド環境変数
# [プロジェクト固有の設定方法]
```

### 3.2 シークレット管理のベストプラクティス

⚠️ **絶対禁止**:
- ❌ Git にコミットしない
- ❌ コード内にハードコーディングしない
- ❌ ログに出力しない

✅ **推奨**:
- 環境変数で管理
- .env.example を用意（値は空）
- Netlify/AWS等のシークレット管理機能を使用
- ローカルは .env.local（.gitignore 済み）

### 3.3 環境変数一覧

| 変数名 | 用途 | 環境 |
|--------|------|------|
| `{{ENV_VAR_1}}` | [説明] | Development, Staging, Production |
| `{{ENV_VAR_2}}` | [説明] | Production のみ |

---

## 4. ロールバック手順

### 4.1 フロントエンドロールバック

```bash
# Netlify で以前のデプロイに戻す
mcp__netlify__rollback_deploy
  site_id: "{{PRODUCTION_SITE_ID}}"
  deploy_id: "{{PREVIOUS_DEPLOY_ID}}"

# または、以前のコミットを再デプロイ
git checkout v{{PREVIOUS_VERSION}}
cd frontend && npm run build
mcp__netlify__create_deploy
  site_id: "{{PRODUCTION_SITE_ID}}"
  deploy_dir: "frontend/dist"
```

### 4.2 バックエンドロールバック

```bash
# [プロジェクト固有のロールバック方法]

# TODO: バックエンドのロールバック方法を記載
```

### 4.3 データベースロールバック

⚠️ **超注意**: データ損失のリスクあり

```bash
# 1. メンテナンスモード開始
# [メンテナンスモード開始コマンド]

# 2. バックアップから復元
# [復元コマンド]

# 3. マイグレーションロールバック（必要に応じて）
# [ロールバックコマンド]

# 4. 動作確認
# [確認コマンド]

# 5. メンテナンスモード解除
# [メンテナンスモード解除コマンド]
```

---

## 5. デプロイチェックリスト

### ステージングデプロイ前

- [ ] main ブランチが最新
- [ ] 全テスト通過
- [ ] code-reviewer レビュー完了
- [ ] ドキュメント更新完了
- [ ] 環境変数設定確認

### 本番デプロイ前

- [ ] ステージング環境で全確認完了
- [ ] リリースノート作成
- [ ] バージョンタグ作成
- [ ] バックアップ取得
- [ ] ロールバック手順確認
- [ ] 関係者への通知

### デプロイ後

- [ ] 本番動作確認
- [ ] エラーログ確認
- [ ] パフォーマンス確認
- [ ] デプロイ完了報告
- [ ] 監視アラート確認（1時間）

---

## 6. トラブルシューティング

### デプロイ失敗時

1. **エラーログ確認**
   ```bash
   # Netlify ログ確認
   mcp__netlify__get_deploy
     deploy_id: "{{DEPLOY_ID}}"
   ```

2. **原因特定**
   - ビルドエラー → ログから原因特定
   - 環境変数ミス → 設定確認
   - 依存関係エラー → package.json 確認

3. **対応**
   - 修正 → 再デプロイ
   - または ロールバック

### 本番障害時

1. **即座にロールバック**（復旧優先）
2. **原因調査**（ログ、モニタリング）
3. **修正**（hotfix ブランチ）
4. **再デプロイ**
5. **ポストモーテム作成**

詳細: [OPERATIONS.md](./OPERATIONS.md)

---

## 7. 継続的デプロイ（CI/CD）設定

### 7.1 自動デプロイ設定（オプション）

```yaml
# GitHub Actions 例（.github/workflows/deploy.yml）

name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
      - name: Build
        run: |
          cd frontend
          npm ci
          npm run build
      - name: Deploy to Netlify
        # Netlify CLI または MCP 使用
```

### 7.2 自動テスト設定

```yaml
# GitHub Actions 例（.github/workflows/test.yml）

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run E2E Tests
        run: npm run test:e2e
```

---

## 関連ドキュメント

- **[HOTFIX.md](./HOTFIX.md)**: 緊急修正フロー
- **[OPERATIONS.md](./OPERATIONS.md)**: 運用フロー（監視、バックアップ等）
- **[SECURITY.md](./SECURITY.md)**: セキュリティ対応フロー
- **[WORKFLOW.md](./WORKFLOW.md)**: 通常の開発ワークフロー

---

## 注意事項

- ⚠️ **本番デプロイは必ずステージング確認後に実施**
- ⚠️ **データベースマイグレーションは必ずバックアップ後に実施**
- ⚠️ **環境変数・シークレットは Git にコミットしない**
- ⚠️ **ロールバック手順を事前に確認**
- ⚠️ **デプロイ後は必ず動作確認**
