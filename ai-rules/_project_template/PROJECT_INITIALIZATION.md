# プロジェクト初期化ガイド

このドキュメントは、**新規プロジェクト**を立ち上げる際の詳細な手順を説明します。

**対象**: 新規プロジェクトの立ち上げ時のみ使用
**既存プロジェクト**: [WORKFLOW.md](WORKFLOW.md) を参照

---

## AI側の初動フロー（最重要）

⚠️ **ユーザーから「新規プロジェクトを始めたい」と言われたら**:

```bash
# 1. このファイルを読み込む（既に読み込み済み）
# 2. ステップ0から開始
# → 要件定義のヒアリングを開始（技術スタック選定は後）
```

**禁止事項**:
- ❌ いきなり技術スタックを質問しない（要件定義が先）
- ❌ 「要件定義書を配置してください」と言わない（AIが支援して作成）
- ❌ 受け身で「教えてください」と待たない（AIが能動的にヒアリング）

---

## 概要

新規プロジェクトは以下のステップで立ち上げます：

```
[ステップ0: 要件定義（AI主導でヒアリング）]
    ↓
[ステップ1: 技術選定・資料準備]
    ↓
[ステップ2: ルール・ワークフロー策定]
    ↓
[ステップ3: 初期設定・ドキュメント整備]
    ↓
[ステップ4: 環境構築]
    ↓
[実装フェーズ開始（通常のワークフロー）]
  - Phase 1（MVP実装）
  - Phase 2（追加機能）
  - ...（フェーズ管理する場合）
```

---

## ステップ0: 要件定義（AI主導でヒアリング）

### 目的

AIとの対話で要件を明確化し、要件定義書を作成する段階です。

⚠️ **このステップはAIが主導**してヒアリングを進めます。

### AI側の実施内容

#### Phase 1: プロジェクト概要のヒアリング

以下を順番に質問して、プロジェクトの全体像を把握します：

**1. プロジェクトの目的**

質問例:
- 「このアプリケーションで何を実現したいですか？」
- 「解決したい課題は何ですか？」
- 「なぜこのアプリケーションが必要ですか？」

**2. ターゲットユーザー**

質問例:
- 「誰が使うアプリケーションですか？」
- 「ユーザーの特徴（年齢層、ITリテラシー等）は？」
- 「ユーザー数の想定は？」

**3. 主要機能のリストアップ（ざっくり）**

質問例:
- 「必須の機能を教えてください」
- 「優先度の高い機能から順に教えてください」
- 「MVP（最小限の製品）に含める機能は何ですか？」

#### Phase 2: 機能要件の詳細化

各機能について詳しくヒアリング：

質問例:
- 「〇〇機能の具体的な仕様を教えてください」
- 「画面遷移やフローはどうなりますか？」
- 「データモデル（保存するデータ）はどういうイメージですか？」
- 「優先度（MVP、Phase 1、Phase 2等）はどうしますか？」
- 「エッジケースや例外処理はどう扱いますか？」

#### Phase 3: 非機能要件の確認

質問例:

- **パフォーマンス**: 「応答時間や同時接続数の要件はありますか？」
- **セキュリティ**: 「認証方式や権限管理の要件は？個人情報の取り扱いは？」
- **可用性**: 「稼働時間やバックアップの要件は？ダウンタイムの許容範囲は？」
- **拡張性**: 「将来的な機能追加の予定は？ユーザー数の増加は想定していますか？」

#### Phase 4: 参考資料の確認

既存の資料があれば確認：

```bash
ls reference/
Read reference/仕様書.pdf  # あれば
Read reference/ER図.png     # あれば
Read reference/ワイヤーフレーム.png  # あれば
```

資料がない場合は、ヒアリング内容を基に要件定義書を作成します。

#### Phase 5: 要件定義書の作成

ヒアリング内容を基に、以下の構成で要件定義書を作成：

```markdown
# {{PROJECT_NAME}} 要件定義書

## 1. プロジェクト概要
- 目的
- ターゲットユーザー
- 期待される効果

## 2. 機能要件
### 2.1 MVP（必須機能）
- [機能名]: [説明]
- ...

### 2.2 Phase 1（優先度：高）
- [機能名]: [説明]
- ...

### 2.3 Phase 2（優先度：中）
- ...

## 3. 非機能要件
- パフォーマンス
- セキュリティ
- 可用性
- 拡張性

## 4. データモデル概要
- [エンティティ名]: [説明]
- ...

## 5. 画面遷移・フロー
- [画面名] → [画面名]
- ...

## 6. 懸念事項・リスク
- [リスク]: [対策]
- ...
```

**保存先**: `reference/requirements.md`

### 成果物

- ✅ 要件定義書（reference/requirements.md）
- ✅ ユーザーとの合意形成

---

## ステップ1: 技術選定・資料準備

### 目的

要件に基づいて技術スタックを選定する段階です。

⚠️ **このステップで初めて技術スタックを検討**します。

### AI側の実施内容

#### 1. 技術スタックの提案

要件定義の内容を基に、以下を提案：

**フロントエンド候補**:
- React + Vite: [選定理由]
- Next.js: [選定理由]
- Vue + Vite: [選定理由]
- Svelte: [選定理由]

**バックエンド候補**:
- FastAPI (Python): [選定理由]
- Express (Node.js): [選定理由]
- Django (Python): [選定理由]
- NestJS (Node.js): [選定理由]

**データベース候補**:
- PostgreSQL: [選定理由]
- MySQL: [選定理由]
- MongoDB: [選定理由]

**その他**:
- 認証方式: JWT、OAuth等
- デプロイ先: Netlify、Vercel、AWS等
- 外部API連携: [必要なAPI]

#### 2. 資料整理

追加の参考資料があれば `reference/` に配置を依頼：

- ワイヤーフレーム（画像、Figmaリンク等）
- データモデル/ER図（画像、PDF等）
- API仕様書（既存システムとの連携がある場合）
- サンプルデータ（CSV、JSON等）
- 参考UI/デザイン

詳細: [reference/README.md](../../reference/README.md)

### 成果物

- ✅ 技術選定理由書（Serenaメモリまたはdocs/に記録）
- ✅ 参考資料の整理

---

## ステップ1: ルール・ワークフロー策定（AI支援）

### 目的

プロジェクト固有のルールとワークフローを決める段階です。

### AI側の実施内容

#### 1. プロジェクト固有ルールの策定

ユーザーと相談しながら以下を決定：

**コーディング規約**:
- 命名規則（変数、関数、クラス等）
- ディレクトリ構成
- ファイル命名規則
- コメントルール

**Git運用ルール**:
- ブランチ命名規則（feat-*, fix-*, docs-*等）
- コミットメッセージ形式のカスタマイズ
- PR作成ルール
- マージ戦略

**レビュー基準**:
- Critical/Major/Minorの定義
- 必須チェック項目
- コードレビューの粒度

#### 2. ワークフローのカスタマイズ

**フェーズ管理**:
- フェーズ分けの要否
- 各フェーズの定義と目標
- フェーズ間の移行基準

**Issue管理**:
- Issueテンプレートのカスタマイズ
- ラベル体系
- 優先度管理方法

**デプロイフロー**:
- 開発環境・ステージング・本番の構成
- デプロイタイミング
- ロールバック方針

#### 3. ai-rules/ のカスタマイズ

プロジェクト固有のガイドラインを作成：

- `ai-rules/_project_template/` 内のファイルをカスタマイズ
- プロジェクト固有の命名規則を追加
- 技術スタック固有のルールを追加

#### 4. 成果物

- カスタマイズされたai-rules/ドキュメント
- 開発ルール定義書（docs/ または Serenaメモリに記録）

---

## ステップ2: 初期設定・ドキュメント整備（AI支援）

### 目的

プロジェクト設定とドキュメントを整備する段階です。

### AI側の実施内容

#### 1. CLAUDE.mdのプレースホルダー更新

Phase 0.5で決定した内容を元に、以下を設定：

**必須項目**:
- `{{PROJECT_NAME}}` → プロジェクト名
- `{{GITHUB_OWNER}}/{{GITHUB_REPO}}` → GitHubリポジトリ
- `{{FRONTEND_PORT}}` → フロントエンドのポート番号（例: 5173）
- `{{BACKEND_PORT}}` → バックエンドのポート番号（例: 8000）
- `{{TEST_USER_EMAIL}}` → E2Eテスト用のメールアドレス
- `{{CURRENT_DATE}}` → 現在の日付（YYYY-MM-DD形式）

**技術スタック（確定版）**:
- フロントエンド: [Phase 0.5で決定した技術]
- バックエンド: [Phase 0.5で決定した技術]
- データベース: [Phase 0.5で決定した技術]

#### 2. .mcp.jsonの確認

`.mcp.json` に必要なAPIキーや設定があるか確認：

- GitHub Personal Access Token
- Netlify Personal Access Token（デプロイする場合）
- その他の外部API認証情報

不足している場合は、ユーザーに設定を依頼します。

#### 3. Serenaメモリの初期化

初期状態のメモリファイルを作成：

**必須ファイル**:
- `current_issues_and_priorities.md` - 現在のIssueと優先度
- `session_handover.md` - セッション引き継ぎ情報
- `requirements_specifications.md` - Phase 0.5で整理した詳細要件

**フェーズ管理する場合**:
- `phase_progress.md` - フェーズ進捗管理

**技術仕様がある場合**:
- `database_specifications.md` - データベース詳細仕様
- `api_specifications.md` - API詳細仕様

#### 4. 基本ドキュメントの作成

以下のドキュメントを作成：

**必須**:
- `docs/REQUIREMENTS.md` - 要件定義書（Phase 0.5の内容を整理）
- `docs/SETUP.md` - 環境構築手順（雛形）
- `docs/API.md` - APIエンドポイント仕様（空の雛形）
- `docs/DATABASE.md` - データベーススキーマ定義（空の雛形）

**フェーズ管理する場合**:
- `docs/PHASES.md` - フェーズ管理ドキュメント

**Phase 1で決定したルールを記載**:
- `docs/DEVELOPMENT_RULES.md` - 開発ルール（任意）

### チェックリスト

Phase 2完了時に以下を確認：

- [ ] CLAUDE.mdのプレースホルダーを全て更新した
- [ ] .mcp.jsonの設定を確認した（またはユーザーに依頼した）
- [ ] Serenaメモリの初期ファイルを作成した
- [ ] 基本ドキュメントを作成した
- [ ] Phase 0.5とPhase 1の決定事項がドキュメント化されている

---

## ステップ3: 環境構築（AI支援）

### 目的

実際の開発環境をセットアップし、実装を開始できる状態にする段階です。

### AI側の実施内容

#### 1. Dockerセットアップ

**docker-compose.yml** の作成：

```yaml
version: '3.8'

services:
  # フロントエンド
  frontend:
    build: ./frontend
    ports:
      - "{{FRONTEND_PORT}}:{{FRONTEND_PORT}}"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:{{BACKEND_PORT}}

  # バックエンド
  backend:
    build: ./backend
    ports:
      - "{{BACKEND_PORT}}:{{BACKEND_PORT}}"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/dbname

  # データベース
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 2. フロントエンド初期化

選定した技術に応じてプロジェクトを作成：

**React + Vite**:
```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
```

**Next.js**:
```bash
npx create-next-app@latest frontend --typescript --tailwind --app
```

**Vue + Vite**:
```bash
cd frontend
npm create vite@latest . -- --template vue-ts
npm install
```

#### 3. バックエンド初期化

選定した技術に応じてプロジェクトを作成：

**FastAPI**:
```bash
cd backend
# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 必要なパッケージのインストール
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv

# main.pyの作成
```

**Express**:
```bash
cd backend
npm init -y
npm install express cors dotenv pg
npm install -D typescript @types/node @types/express ts-node
npx tsc --init
```

#### 4. データベース設定

**スキーマ定義**:
- ER図を基にテーブル定義を作成
- マイグレーションファイルを作成（Alembic、Prisma等）
- 初期データのシードファイルを作成

**docs/DATABASE.md** への記載：
- テーブル構造
- リレーション
- インデックス
- 制約

#### 5. 開発サーバー起動確認

```bash
# Docker環境の起動
docker-compose up -d

# ログ確認
docker-compose logs -f

# 各サービスの動作確認
# - フロントエンド: http://localhost:{{FRONTEND_PORT}}
# - バックエンド: http://localhost:{{BACKEND_PORT}}
# - データベース: 接続確認
```

### チェックリスト

Phase 2完了時に以下を確認：

- [ ] docker-compose.ymlを作成した
- [ ] フロントエンドプロジェクトを初期化した
- [ ] バックエンドプロジェクトを初期化した
- [ ] データベーススキーマを定義した
- [ ] 開発サーバーが正常に起動することを確認した
- [ ] 各サービス間の疎通を確認した
- [ ] docs/SETUP.mdに環境構築手順を記載した

---

## 実装フェーズへの移行

### 確認事項

ステップ3が完了したら、以下を確認してから実装フェーズに移行します：

1. **環境が正常に動作している**
   - フロントエンド、バックエンド、DBが全て起動する
   - 各サービス間の疎通ができる

2. **ドキュメントが整備されている**
   - docs/SETUP.md に環境構築手順が記載されている
   - docs/DATABASE.md にスキーマ定義が記載されている
   - docs/API.md にAPI仕様の雛形がある
   - docs/REQUIREMENTS.md に要件が記載されている

3. **Serenaメモリが初期化されている**
   - 必要なメモリファイルが作成されている
   - 初期状態が記録されている

4. **開発ルールが確定している**
   - ai-rules/ のカスタマイズが完了している
   - ブランチ戦略・レビュー基準が決定している

### 実装フェーズの開始

実装フェーズ以降は、通常の開発ワークフローに従います：

1. **セッション開始時**: Serenaメモリから状態を読み込む
2. **機能開発**: feature ブランチで作業
3. **テスト**: e2e-tester サブエージェントでテスト
4. **PR作成**: code-reviewer サブエージェントでレビュー
5. **マージ**: docs-updater サブエージェントでドキュメント更新

**実装フェーズ管理する場合**:
- Phase 1: MVP実装
- Phase 2: 追加機能実装
- Phase 3: ...

詳細: [WORKFLOW.md](WORKFLOW.md)

---

## トラブルシューティング

### ステップ0〜1でよくある問題

**Q: 技術スタックが決まらない**
A: ステップ0.5で要件を明確化してから、要件に合った技術を選定してください。AIに相談も可能です。

**Q: 要件が曖昧すぎる**
A: reference/ に参考資料を追加するか、ステップ0.5でAIと対話しながら要件を詰めてください。

### ステップ2でよくある問題

**Q: GitHubリポジトリがまだ作成されていない**
A: 先にGitHubでリポジトリを作成してから、CLAUDE.mdに記載してください。

**Q: .mcp.jsonにAPIキーがない**
A: ユーザーに設定を依頼し、設定が完了してから次のステップに進んでください。

### ステップ3でよくある問題

**Q: Dockerが起動しない**
A: Dockerがインストールされているか、Docker Desktopが起動しているか確認してください。

**Q: ポートが既に使用されている**
A: 別のポート番号を選定し、CLAUDE.mdとdocker-compose.ymlを更新してください。

**Q: データベース接続エラー**
A: docker-compose.ymlの環境変数とバックエンドの設定が一致しているか確認してください。

---

## まとめ

新規プロジェクトの立ち上げは以下の流れで進めます：

**立ち上げステップ（準備段階）**:
1. **ステップ0**: ユーザーがプロジェクト企画・資料準備
2. **ステップ0.5**: AIと要件定義を詳細化
3. **ステップ1**: AIとルール・ワークフローを策定
4. **ステップ2**: AIが初期設定を支援（CLAUDE.md更新、ドキュメント作成等）
5. **ステップ3**: AIが環境構築を支援（Docker、プロジェクト初期化等）

**実装フェーズ（開発段階）**:
- Phase 1: MVP実装
- Phase 2: 追加機能実装
- Phase 3: ...（フェーズ管理する場合）

各ステップのチェックリストを確認しながら、段階的に進めることで、スムーズなプロジェクト立ち上げが可能です。
