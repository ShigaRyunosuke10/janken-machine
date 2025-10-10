# Claude Code プロジェクトテンプレート

**バージョン**: 2.0  
**最終更新**: 2025-10-10

## 📋 概要

Claude Codeを使った開発プロジェクトのテンプレートリポジトリです。このテンプレートをクローンして、**新規プロジェクトの立ち上げ**または**既存プロジェクトへの適用**ができます。

### 🎯 特徴

1. **新規・既存の両対応**: 新規プロジェクト立ち上げ手順と既存プロジェクト運用の両方に対応
2. **ai-rulesが充実**: 共通ルール11個 + プロジェクト固有8個のテンプレート
3. **段階的な立ち上げ**: Phase 0（企画）→ Phase 1（初期設定）→ Phase 2（環境構築）→ Phase 3（開発）
4. **カスタマイズ可能**: プロジェクトに合わせてai-rulesを追加・編集
5. **サブエージェント完備**: code-reviewer、e2e-tester、docs-updater

---

## 🚀 クイックスタート

### プロジェクトタイプを選択

このテンプレートは2つの使い方があります：

#### 🆕 新規プロジェクト

ゼロからプロジェクトを立ち上げる場合

→ [新規プロジェクト立ち上げ手順](#-新規プロジェクト立ち上げ手順) へ

#### 📂 既存プロジェクト

既に開発が進んでいるプロジェクトにClaude Code環境を導入する場合

→ [既存プロジェクトへの適用](#-既存プロジェクトへの適用) へ

---

## 🆕 新規プロジェクト立ち上げ手順

### 1. リポジトリをクローン

```bash
git clone <このリポジトリのURL> my-project
cd my-project
```

### 2. MCP設定ファイル編集

**.mcp.json** を編集して、MCPサーバーのAPIキーを設定：

```json
{
  "mcpServers": {
    "context7": {
      "args": ["--api-key", "your-context7-api-key-here"]
    },
    "github": {
      "headers": {
        "Authorization": "Bearer your-github-token-here"
      }
    }
  }
}
```

**重要**: .mcp.jsonは機密情報を含むため、.gitignoreに追加されています。

### 3. Gitリポジトリ初期化

```bash
# 既存のgit履歴を削除して新規初期化
rm -rf .git
git init
git add .
git commit -m "chore: initial commit from template"

# GitHubリポジトリと接続（事前にGitHub上でリポジトリ作成）
git remote add origin git@github.com:YourUsername/my-project.git
git push -u origin main
```

### 4. Claude Codeセッション開始 & テンプレート設定

```bash
# VSCode でプロジェクトを開く
code .

# Claude Code 拡張機能でセッション開始
```

#### 🔹 初回セッション開始プロンプト（重要）

Claude Codeセッションを開始したら、**以下のプロンプトを送信**します。Claude Codeが対話的に質問し、自動的にすべてのテンプレート変数を置換します：

```
このプロジェクトのテンプレート設定を開始します。

以下の情報を対話形式で1つずつ質問してください。
回答を受け取ったら、ai-rules/_project_template/、.claude/agents/、docker-compose.yml 内の全ファイルの {{...}} 変数を置換してください：

**プロジェクト情報**:
1. プロジェクト名（英数字・ハイフン、例: my-webapp）
2. GitHubオーナー名（例: YourUsername）
3. GitHubリポジトリ名（通常はプロジェクト名と同じ）

**開発環境**:
4. フロントエンドポート（デフォルト: 3000、Enterでスキップ可）
5. バックエンドポート（デフォルト: 8000、Enterでスキップ可）
6. Docker使用の有無（yes/no、noの場合はdocker-compose.ymlをスキップ）

**テストユーザー**:
7. テストユーザーメール（例: qa+test@example.com）
8. テストユーザーパスワード（8文字以上推奨）
9. テストユーザー名（例: qa_test）
10. テストユーザーID（UUID形式、Enterで自動生成）

すべての情報を受け取ったら：
1. ai-rules/_project_template/、.claude/agents/、docker-compose.yml 内の全ファイルの {{...}} を実際の値に一括置換
2. {{CURRENT_DATE}} は今日の日付（2025-10-10形式）に置換
3. ai-rules/_project_template を ai-rules/[プロジェクト名] にリネーム
4. Docker不使用の場合はdocker-compose.ymlを削除
5. 完了したら「✅ テンプレート設定完了」と報告

⚠️ **注意**: .mcp.jsonのAPIキーは機密情報のため、この対話では扱いません。別途手動で編集してください。

それでは質問を開始してください。
```

このプロンプトにより、手動での置換作業が不要になります。

### 5. プロジェクト企画を開始

Phase 0（プロジェクト企画）から開始します。詳細は以下を参照：

→ [新規プロジェクト開発フロー](#-新規プロジェクト開発フロー-phase-0-3) へ

---

## 📂 既存プロジェクトへの適用

既存プロジェクトにClaude Code環境を導入する手順です。

### 1. このテンプレートから必要なファイルをコピー

```bash
# 既存プロジェクトのルートで実行
cp -r <テンプレートのパス>/.claude .
cp -r <テンプレートのパス>/ai-rules .
cp <テンプレートのパス>/CLAUDE.md .
cp <テンプレートのパス>/.mcp.json .mcp.json.example
```

### 2. CLAUDE.mdのプレースホルダー更新

既存プロジェクトの情報に合わせて更新：

- `{{PROJECT_NAME}}` → 実際のプロジェクト名
- `{{GITHUB_OWNER}}/{{GITHUB_REPO}}` → GitHubリポジトリ
- `{{FRONTEND_PORT}}`, `{{BACKEND_PORT}}` → 実際のポート番号
- `{{TEST_USER_EMAIL}}` → テストユーザーのメール
- 技術スタック欄を実際の技術に更新

### 3. .mcp.json設定

`.mcp.json.example` をコピーして `.mcp.json` を作成し、APIキーを設定します。

### 4. Serenaメモリの初期化

既存プロジェクトの状態をSerenaメモリに記録します：

```
> 既存プロジェクトの状態をSerenaメモリに初期化してください。
>
> 以下の情報を確認して、Serenaメモリファイルを作成してください：
> 1. 現在の実装状況（どこまで完成しているか）
> 2. 未解決のIssue
> 3. 今後の予定
> 4. データベーススキーマ
> 5. APIエンドポイント仕様
```

### 5. ドキュメント整備

既存のコードベースを確認して、docs/フォルダに必要なドキュメントを作成します：

```
> 既存コードベースを確認し、以下のドキュメントを作成してください：
> - docs/SETUP.md（環境構築手順）
> - docs/DATABASE.md（データベーススキーマ）
> - docs/API.md（APIエンドポイント仕様）
```

### 6. 通常の開発ワークフローへ

ドキュメント整備が完了したら、通常の開発ワークフローに従います：

→ [既存プロジェクト開発フロー](#-既存プロジェクト開発フロー) へ

---

## 🆕 新規プロジェクト開発フロー (Phase 0-3)

新規プロジェクトは段階的に立ち上げます：

```
Phase 0: プロジェクト企画（ユーザー主導）
    ↓
Phase 1: 初期設定（AI支援）
    ↓
Phase 2: 環境構築（AI支援）
    ↓
Phase 3: 開発フェーズ（通常のワークフロー）
```

詳細: [ai-rules/_project_template/PROJECT_INITIALIZATION.md](ai-rules/_project_template/PROJECT_INITIALIZATION.md)

### Phase 0: プロジェクト企画（ユーザー主導）

#### ユーザーが実施すること

1. **プロジェクト概要の決定**
   - プロジェクト名、目的、ターゲットユーザー
   - 主要機能リスト
   - 技術スタック選定

2. **参考資料の準備**
   - 要件定義書を `reference/` フォルダに配置
   - ワイヤーフレーム、ER図、API仕様書等を配置
   - サンプルデータがあれば配置

### Phase 1: 初期設定（AI支援）

```
> Phase 1を開始します。
> reference/フォルダの資料を確認し、
> CLAUDE.mdのプレースホルダーを更新してください。
> その後、Serenaメモリと基本ドキュメントを初期化してください。
```

AI側が実施：
- reference/フォルダの資料確認
- CLAUDE.mdのプレースホルダー更新
- .mcp.json設定確認
- Serenaメモリ初期化
- 基本ドキュメント作成（docs/SETUP.md等）

チェックリスト: [PROJECT_INITIALIZATION_CHECKLIST.md](ai-rules/_project_template/PROJECT_INITIALIZATION_CHECKLIST.md)

### Phase 2: 環境構築（AI支援）

```
> Phase 2を開始します。
> Docker環境をセットアップし、
> フロントエンド・バックエンドプロジェクトを初期化してください。
```

AI側が実施：
- docker-compose.yml作成
- フロントエンドプロジェクト初期化
- バックエンドプロジェクト初期化
- データベーススキーマ定義
- 開発サーバー起動確認

### Phase 3: 開発フェーズへ移行

Phase 2が完了したら、通常の開発ワークフローに従います。

→ [既存プロジェクト開発フロー](#-既存プロジェクト開発フロー) へ

---

## 📂 既存プロジェクト開発フロー

Phase 3以降、または既存プロジェクトで使用するワークフローです。

### Phase 0: 要件定義（既存プロジェクトではスキップ可）

#### 1. 要件定義開始
```
> ai-rules/my-project/REQUIREMENTS_PROMPT.md を確認し、
> 要件定義を行ってください。対話形式で質問に答えながら
> REQUIREMENTS.md を作成してください。
```

#### 2. ai-rulesテンプレートのカスタマイズ

要件定義が完了したら、プロジェクト固有のai-rulesファイルを編集・追加：

**ai-rules/の2層構造**:
- **common/** - 汎用ルール（変数なし、そのまま使える）
  - どのプロジェクトでも共通の開発ルール
  - 例: コミット規約、命名規則、汎用ワークフロー
  - 編集不要、そのまま参照

- **_project_template/** → **my-project/** - プロジェクト固有（変数あり）
  - {{変数}} を実際の値に置換したプロジェクト専用ルール
  - 例: テストユーザー情報、ポート番号、MCP設定
  - 初回セッションで自動置換・リネーム済み
  - プロジェクトに応じてさらにカスタマイズ可能

```
> 要件定義が完了しました。
> 以下のai-rulesファイルをプロジェクトに合わせて更新してください：
>
> 1. SETUP_AND_MCP.md - テストユーザー情報、ポート番号を設定
> 2. TESTING.md - E2Eテストシナリオを追加
> 3. 必要に応じて新しいルールファイルを追加
>    例: セキュリティガイドライン、API設計規約など
```

**追加推奨ファイル**（プロジェクトに応じて）：
- `SECURITY_GUIDELINES.md` - セキュリティ要件
- `API_DESIGN_RULES.md` - API設計規約
- `UI_UX_GUIDELINES.md` - UI/UX設計ガイド
- `DATA_PRIVACY.md` - データプライバシーポリシー

#### 3. docs/フォルダの準備
```
> docs/README.md, docs/DATABASE.md, docs/API.md を
> 初期状態で作成してください。プロジェクト概要を記載してください。
```

### Phase 1-N: 機能実装

#### 4. 各Phaseの実装サイクル

```
> Phase 1を開始します。
> ai-rules/my-project/REQUIREMENTS.md を確認し、
> Phase 1の実装計画を立ててください。
```

**実装サイクル**：
1. ブランチ作成 → 実装  
2. E2Eテスト（`e2e-tester`） → コミット  
3. PR作成 → code-reviewerレビュー  
4. 修正対応 → マージ  
5. docs-updaterでドキュメント更新

#### 5. Phase完了チェック
```
> Phase 1が完了しました。
> 仕様との整合性を確認し、次のPhaseの準備をしてください。
```

### Phase Final: デプロイ

#### 6. デプロイ準備
```
> 本番環境へのデプロイ準備を開始してください。
>
> 1. 環境変数の本番設定確認
> 2. セキュリティチェック
> 3. パフォーマンステスト
> 4. ドキュメント最終確認
```

#### 7. フロントエンドデプロイ（Vercel等）
```
> フロントエンドをVercelにデプロイしてください。
> デプロイ後の動作確認も実施してください。
```

#### 8. バックエンドデプロイ（AWS EC2等）
```
> バックエンドをAWS EC2にデプロイしてください。
> Dockerイメージのビルドとデプロイを実施してください。
```

#### 9. 本番環境E2Eテスト
```
> 本番環境でE2Eテストを実施してください。
> すべての主要機能が正常に動作することを確認してください。
```

#### 10. デプロイ完了とドキュメント更新
```
> デプロイが完了しました。
> docs/DEPLOYMENT.md を作成し、デプロイ手順とURL情報を記載してください。
```

---

## 📁 ディレクトリ構造

```
.
├── .claude/
│   ├── settings.json          # Claude Code設定（編集推奨）
│   ├── settings.local.json    # ローカル設定（gitignore）
│   └── agents/                # サブエージェント設定
├── ai-rules/
│   ├── common/                # プロジェクト横断の共通ルール（11ファイル）
│   └── _project_template/     # プロジェクト固有ルール（要リネーム・編集）
│       ├── REQUIREMENTS_PROMPT.md      # 要件定義プロンプト
│       ├── REQUIREMENTS_ASSISTANT.md   # 要件定義アシスタント
│       ├── DOCUMENTATION_GUIDE.md      # ドキュメント管理
│       ├── ISSUE_GUIDELINES.md         # Issue管理
│       ├── PR_AND_REVIEW.md            # PRレビュープロセス
│       ├── SETUP_AND_MCP.md            # 環境構築・MCP設定
│       ├── TESTING.md                  # テストガイドライン
│       └── WORKFLOW.md                 # 開発ワークフロー
├── docs/                      # 人間用ドキュメント（要作成）
└── README.md                  # このファイル
```

---

## 🛠️ 含まれるai-rules

### common/（プロジェクト横断）
- `COMMIT_GUIDELINES.md` - コミットメッセージ規約
- `DOCUMENTATION_GUIDE.md` - ドキュメント管理（共通版）
- `ISSUE_GUIDELINES.md` - Issue管理（共通版）
- `NAMING_CONVENTIONS.md` - 命名規則
- `PHASE_MANAGEMENT.md` - フェーズ管理
- `PR_PROCESS.md` - PRプロセス（共通版）
- `SESSION_MANAGEMENT.md` - セッション管理
- `SETTINGS_JSON_GUIDE.md` - settings.json設定ガイド
- `WORKFLOW.md` - 開発ワークフロー（共通版）
- `DOCUMENT_CLEANUP.md` - ドキュメントクリーンアップ
- `DOCUMENT_CONSISTENCY.md` - ドキュメント一貫性

### _project_template/（プロジェクト固有、要カスタマイズ）
- `REQUIREMENTS_PROMPT.md` - 要件定義プロンプト
- `REQUIREMENTS_ASSISTANT.md` - 要件定義アシスタント
- `DOCUMENTATION_GUIDE.md` - ドキュメント管理（プロジェクト版）
- `ISSUE_GUIDELINES.md` - Issue管理（プロジェクト版）
- `PR_AND_REVIEW.md` - PRレビュープロセス
- `SETUP_AND_MCP.md` - 環境構築・MCP設定
- `TESTING.md` - テストガイドライン
- `WORKFLOW.md` - 開発ワークフロー（プロジェクト版）

---

## ⚙️ 推奨設定

### .gitignore に追加推奨
```.gitignore
# Claude Code local settings
.claude/settings.local.json

# Environment variables
.env
.env.local
backend/.env
frontend/.env.local

# Dependencies
node_modules/
__pycache__/
```

### MCP サーバー設定

必要に応じて `.mcp.json` を作成してMCPサーバーを設定：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-github-token"
      }
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "your-context7-api-key"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

---

## 📖 使い方のヒント

### 1. 要件定義は対話的に
Claude Codeに「REQUIREMENTS_PROMPT.mdに従って要件定義を行ってください」と指示すると、対話形式で要件を整理できます。

### 2. ai-rulesは段階的にカスタマイズ
最初は共通ルールだけで開始し、プロジェクトが進むにつれて固有ルールを追加・調整します。

### 3. Serenaメモリの活用
セッション開始時に必ずSerenaメモリから前回の状態を読み込むよう、WORKFLOWに記載されています。

### 4. サブエージェントの活用
- **code-reviewer**: PR作成後に必ず実行
- **e2e-tester**: コミット前に必ず実行
- **docs-updater**: マージ後に必ず実行

### 5. デプロイは段階的に
- まずステージング環境でテスト
- E2Eテスト合格後に本番デプロイ
- デプロイ後も必ず動作確認

---

## 🤝 コントリビューション

このテンプレート自体への改善提案は Issue/PR でお願いします。

---

## 📄 ライセンス

MIT License

---

**このテンプレートを使って、素早くClaude Codeプロジェクトを開始しましょう！**
