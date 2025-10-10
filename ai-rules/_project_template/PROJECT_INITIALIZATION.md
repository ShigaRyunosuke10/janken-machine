# プロジェクト初期化ガイド

このドキュメントは、**新規プロジェクト**を立ち上げる際の詳細な手順を説明します。

**対象**: 新規プロジェクトの立ち上げ時のみ使用
**既存プロジェクト**: [WORKFLOW.md](WORKFLOW.md) を参照

---

## 概要

新規プロジェクトは以下の3つのフェーズで立ち上げます：

```
Phase 0: プロジェクト企画（ユーザー主導）
    ↓
Phase 1: 初期設定（AI支援）
    ↓
Phase 2: 環境構築（AI支援）
    ↓
Phase 3: 開発フェーズ（通常のワークフロー）
```

---

## Phase 0: プロジェクト企画（ユーザー主導）

### 目的

プロジェクトの方向性を明確にし、必要な情報を準備する段階です。

### ユーザーが実施すること

#### 1. プロジェクト概要の決定

以下の項目を明確にしてください：

- **プロジェクト名**: プロジェクトの名称
- **目的**: 何を実現したいのか
- **ターゲットユーザー**: 誰のためのアプリケーションか
- **主要機能**: 最低限必要な機能のリスト
- **技術スタック**: 使用する技術（フロントエンド、バックエンド、DB等）

#### 2. 参考資料の準備

以下の資料を `reference/` フォルダに配置してください：

**必須資料**:
- 要件定義書（テキスト、PDF、Excel等）
- 主要な機能リスト

**推奨資料**:
- ワイヤーフレーム（画像、Figmaリンク等）
- データモデル/ER図（画像、PDF等）
- API仕様書（既存システムとの連携がある場合）
- サンプルデータ（CSV、JSON等）
- 参考UI/デザイン

**参考資料の配置例**:
```
reference/
├── 要件定義書.pdf
├── ワイヤーフレーム.png
├── ER図.png
├── API仕様書.pdf
└── サンプルデータ.csv
```

詳細: [reference/README.md](../../reference/README.md)

#### 3. 技術スタックの選定

プロジェクトで使用する技術を決定してください：

**フロントエンド**:
- React + Vite
- Next.js
- Vue + Vite
- Svelte
- その他

**バックエンド**:
- FastAPI (Python)
- Express (Node.js)
- Django (Python)
- NestJS (Node.js)
- その他

**データベース**:
- PostgreSQL
- MySQL
- MongoDB
- SQLite
- その他

**その他**:
- 認証方式（JWT、OAuth等）
- デプロイ先（Netlify、Vercel、AWS等）
- 外部API連携の有無

### AI側の確認事項

Phase 0が完了したら、AI側は以下を確認します：

1. `reference/` フォルダに必要な資料があるか
2. 技術スタックが明確になっているか
3. 要件が理解できる状態か

不明点がある場合は、ユーザーに質問します。

---

## Phase 1: 初期設定（AI支援）

### 目的

プロジェクトの基本設定を行い、開発環境を整える準備をする段階です。

### AI側の実施内容

#### 1. 参考資料の確認

```bash
# reference/フォルダの確認
ls reference/

# 各資料の読み込み（PDF、画像、Excel等）
Read reference/要件定義書.pdf
Read reference/ER図.png
Read reference/ワイヤーフレーム.png
```

#### 2. CLAUDE.mdのプレースホルダー更新

ユーザーにヒアリングして以下を設定：

**必須項目**:
- `{{PROJECT_NAME}}` → プロジェクト名
- `{{GITHUB_OWNER}}/{{GITHUB_REPO}}` → GitHubリポジトリ
- `{{FRONTEND_PORT}}` → フロントエンドのポート番号（例: 5173）
- `{{BACKEND_PORT}}` → バックエンドのポート番号（例: 8000）
- `{{TEST_USER_EMAIL}}` → E2Eテスト用のメールアドレス
- `{{CURRENT_DATE}}` → 現在の日付（YYYY-MM-DD形式）

**技術スタック**:
- フロントエンド: [選定した技術]
- バックエンド: [選定した技術]
- データベース: [選定した技術]

**ヒアリング例**:
```
AI: プロジェクト名を教えてください。
User: todo-app

AI: GitHubのリポジトリ名を教えてください（形式: owner/repo）。
User: myname/todo-app

AI: フロントエンドのポート番号を教えてください（デフォルト: 5173）。
User: 5173

AI: バックエンドのポート番号を教えてください（デフォルト: 8000）。
User: 8000

AI: E2Eテスト用のメールアドレスを教えてください。
User: test@example.com
```

#### 3. .mcp.jsonの確認

`.mcp.json` に必要なAPIキーや設定があるか確認：

- GitHub Personal Access Token
- Netlify Personal Access Token（デプロイする場合）
- その他の外部API認証情報

不足している場合は、ユーザーに設定を依頼します。

#### 4. Serenaメモリの初期化

初期状態のメモリファイルを作成：

**必須ファイル**:
- `current_issues_and_priorities.md` - 現在のIssueと優先度
- `session_handover.md` - セッション引き継ぎ情報

**フェーズ管理する場合**:
- `phase_progress.md` - フェーズ進捗管理

**技術仕様がある場合**:
- `database_specifications.md` - データベース詳細仕様
- `api_specifications.md` - API詳細仕様

#### 5. 基本ドキュメントの作成

以下のドキュメントを作成：

**必須**:
- `docs/SETUP.md` - 環境構築手順
- `docs/API.md` - APIエンドポイント仕様（空の雛形）
- `docs/DATABASE.md` - データベーススキーマ定義（空の雛形）

**フェーズ管理する場合**:
- `docs/PHASES.md` - フェーズ管理ドキュメント

### チェックリスト

Phase 1完了時に以下を確認：

- [ ] `reference/` の資料を全て確認した
- [ ] CLAUDE.mdのプレースホルダーを全て更新した
- [ ] .mcp.jsonの設定を確認した（またはユーザーに依頼した）
- [ ] Serenaメモリの初期ファイルを作成した
- [ ] 基本ドキュメントを作成した

---

## Phase 2: 環境構築（AI支援）

### 目的

実際の開発環境をセットアップし、開発を開始できる状態にする段階です。

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

## Phase 3: 開発フェーズへの移行

### 確認事項

Phase 2が完了したら、以下を確認してから開発フェーズに移行します：

1. **環境が正常に動作している**
   - フロントエンド、バックエンド、DBが全て起動する
   - 各サービス間の疎通ができる

2. **ドキュメントが整備されている**
   - docs/SETUP.md に環境構築手順が記載されている
   - docs/DATABASE.md にスキーマ定義が記載されている
   - docs/API.md にAPI仕様の雛形がある

3. **Serenaメモリが初期化されている**
   - 必要なメモリファイルが作成されている
   - 初期状態が記録されている

### 開発フェーズの開始

Phase 3以降は、通常の開発ワークフローに従います：

1. **セッション開始時**: Serenaメモリから状態を読み込む
2. **機能開発**: feature ブランチで作業
3. **テスト**: e2e-tester サブエージェントでテスト
4. **PR作成**: code-reviewer サブエージェントでレビュー
5. **マージ**: docs-updater サブエージェントでドキュメント更新

詳細: [WORKFLOW.md](WORKFLOW.md)

---

## トラブルシューティング

### Phase 1でよくある問題

**Q: GitHubリポジトリがまだ作成されていない**
A: 先にGitHubでリポジトリを作成してから、CLAUDE.mdに記載してください。

**Q: 技術スタックが決まっていない**
A: Phase 0に戻り、要件を整理してから技術選定を行ってください。

**Q: .mcp.jsonにAPIキーがない**
A: ユーザーに設定を依頼し、設定が完了してから次のステップに進んでください。

### Phase 2でよくある問題

**Q: Dockerが起動しない**
A: Dockerがインストールされているか、Docker Desktopが起動しているか確認してください。

**Q: ポートが既に使用されている**
A: 別のポート番号を選定し、CLAUDE.mdとdocker-compose.ymlを更新してください。

**Q: データベース接続エラー**
A: docker-compose.ymlの環境変数とバックエンドの設定が一致しているか確認してください。

---

## まとめ

新規プロジェクトの立ち上げは以下の流れで進めます：

1. **Phase 0**: ユーザーがプロジェクト企画・資料準備
2. **Phase 1**: AIが初期設定を支援（CLAUDE.md更新、ドキュメント作成等）
3. **Phase 2**: AIが環境構築を支援（Docker、プロジェクト初期化等）
4. **Phase 3**: 通常の開発ワークフローに移行

各フェーズのチェックリストを確認しながら、段階的に進めることで、スムーズなプロジェクト立ち上げが可能です。
