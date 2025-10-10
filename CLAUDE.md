# Claude Code Configuration (janken-machine)

このファイルは、Claude Codeがこのプロジェクトで作業する際の基本設定とワークフローを定義します。

**プロジェクト名**: janken-machine
**最終更新**: 2025-10-10

---

## AI側の最初の確認（セッション開始時に必ず実施）

⚠️ **ユーザーとやり取りする前に、まずプロジェクトの状態を判定してください**

```bash
# 1. プレースホルダーの確認
# → {{PROJECT_NAME}} が残っている = 新規プロジェクト
# → {{PROJECT_NAME}} が実際の名前 = 既存プロジェクト

# 2. reference/ の確認
ls reference/

# 3. Serenaメモリの確認（既存プロジェクトの場合）
mcp__serena__list_memories  # メモリがあるか確認
```

### 判定結果に応じた行動

**新規プロジェクトの場合**:
```
→ [新規プロジェクト立ち上げ手順](#新規プロジェクト立ち上げ手順) へ進む
→ ステップ0から要件定義のヒアリングを開始
```

**既存プロジェクトの場合**:
```
→ [セッション開始時の必須手順](#セッション開始時の必須手順) へ進む
→ Serenaメモリから状態を読み込み、前回の続きから開始
```

⚠️ **禁止事項**:
- ❌ 判定せずにいきなり質問しない
- ❌ ユーザーに「新規ですか？既存ですか？」と聞かない（自動判定）

---

## プロジェクト概要

### 基本情報
- **リポジトリ**: ShigaRyunosuke10/janken-machine
- **デバイス**: Raspberry Pi 4B
- **IPアドレス**: 192.168.1.142
- **SSH接続**: `ssh janken@192.168.1.142`
- **デプロイ**: なし（Raspberry Pi単体で完結）

### 技術スタック
- **言語**: Python 3.13
- **GPIO制御**: gpiozero
- **LEDマトリックス**: rpi-rgb-led-matrix (hzeller)
- **フォント描画**: Pillow (PIL)
- **ハードウェア**:
  - Raspberry Pi 4B
  - RGB LEDマトリックスパネル 64×32 × 2枚（上下配置、総解像度 64×64）
  - ボタン×4（スタート、赤、黄、青）

---

## プロジェクトの状態判定

⚠️ **このテンプレートは新規プロジェクト・既存プロジェクトの両方に対応しています**

### 新規プロジェクトの場合

以下に該当する場合は新規プロジェクトです：
- `{{PROJECT_NAME}}` などのプレースホルダーが残っている
- `reference/` フォルダが空または初期状態
- Serenaメモリが未初期化
- 技術スタックが未定義

→ [新規プロジェクト立ち上げ手順](#新規プロジェクト立ち上げ手順) へ進む

### 既存プロジェクトの場合

以下に該当する場合は既存プロジェクトです：
- CLAUDE.mdのプレースホルダーが設定済み
- Serenaメモリに過去のセッション情報がある
- `docs/` や `reference/` に資料がある

→ [セッション開始時の必須手順](#セッション開始時の必須手順) へ進む

---

## 新規プロジェクト立ち上げ手順

⚠️ **新規プロジェクトの場合のみ、この手順を実施してください**

詳細: [ai-rules/_project_template/PROJECT_INITIALIZATION.md](ai-rules/_project_template/PROJECT_INITIALIZATION.md)

### AI側の初動フロー（最重要）

**ユーザーから「新規プロジェクトを始めたい」と言われたら**:

```bash
# 1. PROJECT_INITIALIZATION.mdを読み込む
Read ai-rules/_project_template/PROJECT_INITIALIZATION.md

# 2. ステップ0から開始
# → 要件定義のヒアリングを開始（技術スタック選定は後）
```

⚠️ **禁止事項**:
- ❌ いきなり技術スタックを質問しない（要件定義が先）
- ❌ 「要件定義書を配置してください」と言わない（AIが支援して作成）
- ❌ 受け身で「教えてください」と待たない（AIが能動的にヒアリング）

### 全体フロー

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
[実装フェーズ開始] ← 通常のワークフロー開始
  - Phase 1（MVP実装）
  - Phase 2（追加機能）
  - ...（フェーズ管理する場合）
```

### ステップ0: 要件定義（AI主導でヒアリング）

**目的**: AIとの対話で要件を明確化し、要件定義書を作成する

#### AI側の実施内容

⚠️ **このステップはAIが主導**してヒアリングを進めます

**Phase 1: プロジェクト概要のヒアリング**

以下を順番に質問して、プロジェクトの全体像を把握します：

1. **プロジェクトの目的**
   - 「このアプリケーションで何を実現したいですか？」
   - 「解決したい課題は何ですか？」

2. **ターゲットユーザー**
   - 「誰が使うアプリケーションですか？」
   - 「ユーザーの特徴（年齢層、ITリテラシー等）は？」

3. **主要機能のリストアップ（ざっくり）**
   - 「必須の機能を教えてください」
   - 「優先度の高い機能から順に教えてください」

**Phase 2: 機能要件の詳細化**

各機能について詳しくヒアリング：

- 「〇〇機能の具体的な仕様を教えてください」
- 「画面遷移やフローはどうなりますか？」
- 「データモデル（保存するデータ）はどういうイメージですか？」
- 「優先度（MVP、Phase 1、Phase 2等）はどうしますか？」

**Phase 3: 非機能要件の確認**

- **パフォーマンス**: 「応答時間や同時接続数の要件はありますか？」
- **セキュリティ**: 「認証方式や権限管理の要件は？」
- **可用性**: 「稼働時間やバックアップの要件は？」
- **拡張性**: 「将来的な機能追加の予定は？」

**Phase 4: 参考資料の確認**

既存の資料があれば確認：

```bash
ls reference/
Read reference/仕様書.pdf  # あれば
Read reference/ER図.png     # あれば
```

**成果物**: 要件定義書を `reference/requirements.md` として作成

### ステップ1: 技術選定・資料準備

**目的**: 要件に基づいて技術スタックを選定する

⚠️ **このステップで初めて技術スタックを検討**します

#### AI側の実施内容

**技術スタックの提案**:

要件定義の内容を基に、以下を提案：

- **フロントエンド候補**: React, Vue, Svelte等から選定理由と共に提案
- **バックエンド候補**: FastAPI, Express, Django等から選定理由と共に提案
- **データベース候補**: PostgreSQL, MySQL, MongoDB等から選定理由と共に提案
- **その他**: 認証方式、デプロイ先、外部API連携等

**資料整理**:

- 追加の参考資料があれば `reference/` に配置を依頼
- ワイヤーフレーム、ER図、サンプルデータ等

**成果物**: 技術選定理由書（Serenaメモリまたはdocs/に記録）

### ステップ2: ルール・ワークフロー策定（AI支援）

**目的**: プロジェクト固有のルールとワークフローを決める

**AI側の実施内容**:
- **プロジェクト固有ルールの策定**: コーディング規約、ブランチ戦略、コミットメッセージ形式、レビュー基準
- **ワークフローのカスタマイズ**: 実装フェーズ管理の要否、Issue管理方法、PR・レビュープロセス、デプロイフロー
- **ai-rules/ のカスタマイズ**: プロジェクト固有ガイドラインの作成、テンプレートのカスタマイズ

**成果物**: カスタマイズされたai-rules/ドキュメント

### ステップ3: 初期設定・ドキュメント整備（AI支援）

**目的**: プロジェクト設定とドキュメントを整備する

**AI側の実施内容**:
- **CLAUDE.mdのプレースホルダー更新**: {{PROJECT_NAME}}, {{GITHUB_OWNER}}/{{GITHUB_REPO}}, ポート番号、技術スタック等
- **.mcp.jsonの確認**: APIキー等の設定確認（不足時はユーザーに依頼）
- **Serenaメモリの初期化**: current_issues_and_priorities.md, session_handover.md, phase_progress.md等
- **基本ドキュメントの作成**: docs/REQUIREMENTS.md, docs/SETUP.md, docs/API.md, docs/DATABASE.md等

### ステップ4: 環境構築（AI支援）

**目的**: 実際の開発環境をセットアップする

**AI側の実施内容**:
- **Dockerセットアップ**: docker-compose.ymlの作成・設定
- **フロントエンド初期化**: Vite/Next.js/etc のプロジェクト作成
- **バックエンド初期化**: FastAPI/Express/etc のプロジェクト作成
- **データベース設定**: スキーマ定義・マイグレーション
- **開発サーバー起動確認**: `docker-compose up -d` で起動、各サービスの動作確認

詳細: [ai-rules/_project_template/PROJECT_INITIALIZATION.md](ai-rules/_project_template/PROJECT_INITIALIZATION.md)

---

## よくある質問（新規プロジェクト）

### Q1: 既に要件定義書がある場合は？

A: ステップ0の **Phase 4: 参考資料の確認** で読み込みます。AIが内容を確認して不足があれば追加ヒアリングします。

```bash
# 既存の要件定義書を配置
reference/要件定義書.pdf

# AIが読み込んで確認
Read reference/要件定義書.pdf
```

### Q2: 要件が曖昧な状態でも開始できる？

A: はい。ステップ0でAIが順番にヒアリングしながら要件を明確化します。最初は「ざっくり」でも構いません。

### Q3: 技術スタックが決まっていない場合は？

A: ステップ0で要件を明確化した後、ステップ1でAIが要件に基づいて技術スタックを提案します。

### Q4: ステップ途中で中断しても大丈夫？

A: はい。Serenaメモリに進捗を記録するので、次のセッションで続きから再開できます

### 実装フェーズへ

ステップ4が完了したら、[開発ワークフロー](#開発ワークフロー) に従って実装を進めます。

**実装フェーズ管理する場合**:
- Phase 1: MVP実装
- Phase 2: 追加機能実装
- Phase 3: ...

詳細: [docs/PHASES.md](docs/PHASES.md) （フェーズ管理時）

---

## セッション開始時の必須手順

⚠️ **既存プロジェクト・Phase 3以降の新規プロジェクトで使用**

### 1. 参考資料の確認

⚠️ **開発開始前に必ず確認**

```bash
# reference/ 内の資料を確認
ls reference/

# 必要に応じてPDF、Excel、画像等を読み込む
Read reference/仕様書.pdf
Read reference/ER図.png
```

詳細: [reference/README.md](reference/README.md)

### 2. Serenaメモリから状態を読み込み

⚠️ **毎セッション開始時に必ず実施**

```bash
# 1. プロジェクトをアクティベート
mcp__serena__activate_project
  project: "janken-machine"

# 2. 利用可能なメモリを確認
mcp__serena__list_memories

# 3. 現在の優先度を把握
mcp__serena__read_memory
  memory_file_name: "current_issues_and_priorities.md"

# 4. セッション引き継ぎ情報を確認
mcp__serena__read_memory
  memory_file_name: "session_handover.md"

# 5. フェーズ進捗を確認（フェーズ管理時）
mcp__serena__read_memory
  memory_file_name: "phase_progress.md"
```

詳細: [ai-rules/_project_template/SETUP_AND_MCP.md](ai-rules/_project_template/SETUP_AND_MCP.md)

### 3. ブランチ確認

```bash
git fetch --quiet
git status
```

---

## 開発ワークフロー

詳細: [ai-rules/_project_template/WORKFLOW.md](ai-rules/_project_template/WORKFLOW.md)

### 全体フロー

```
[セッション開始]
    ↓
[Serenaメモリ読み込み] ← 必須
    ↓
[ブランチ作成] (feat-*, fix-*, docs-*, refactor-*)
    ↓
[実装・修正]
    ↓
[e2e-tester サブエージェント実行] ← 必須（コミット前）
    ├─[成功] → [コミット]
    └─[失敗] → [修正] → ループ
    ↓
[push]
    ↓
[PR作成]
    ↓
[code-reviewer サブエージェント レビュー] ← 必須
    ↓
[レビュー対応]
    ├─[マージ可] → [マージ] → [docs-updater サブエージェント] ← 必須
    └─[要修正] → [修正] → 再レビュー
```

---

## サブエージェント

### code-reviewer

**用途**: PR作成直後の必須レビュー

```
> code-reviewerサブエージェントを使用してPR #[番号]をレビューしてください
```

**実行内容**:
- コード品質チェック
- セキュリティ確認
- パフォーマンス検証
- 命名規則準拠確認
- Critical/Major/Minor分類での問題報告

詳細: [.claude/agents/code-reviewer.md](.claude/agents/code-reviewer.md)

### e2e-tester

**用途**: コミット前の必須E2Eテスト

```
> e2e-tester サブエージェントを使用してE2Eテストを実施
```

**実行内容**:
- 変更ファイルからテスト対象を推測
- 正常系・異常系・エッジケースのテストシナリオ作成
- Playwright MCPでテスト実行
- スクリーンショット保存
- テスト結果レポート出力

詳細: [.claude/agents/e2e-tester.md](.claude/agents/e2e-tester.md)

### docs-updater

**用途**: マージ後の必須ドキュメント更新

```
> docs-updaterサブエージェントを使用してドキュメント更新を実施
```

**実行内容**:
- docs/ の人間用ドキュメント更新
- Serenaメモリの詳細仕様更新
- 一貫性確認
- 自動コミット・プッシュ

詳細: [.claude/agents/docs-updater.md](.claude/agents/docs-updater.md)

---

## MCP設定

### 有効なMCPサーバー

#### GitHub
- **用途**: リポジトリ操作
- **リポジトリ**: ShigaRyunosuke10/janken-machine
- **操作**: PR作成、Issue管理、マージ

#### Serena（オプション）
- **用途**: コードベース管理とメモリ
- **プロジェクト**: janken-machine
- **代替手段**: `docs/` 配下のローカルファイルで管理
- **メモリファイル**:
  - `current_issues_and_priorities.md` - Issue・優先度
  - `session_handover.md` - セッション引き継ぎ
  - `project_initialization_progress.md` - 初期化進捗
  - `created_files_registry.md` - 作成ファイル管理

### 未使用MCPサーバー

このプロジェクトでは以下のMCPは使用しません（.mcp.jsonのプレースホルダーはそのまま）:

- **Context7**: 最新ライブラリ情報不要（安定版使用）
- **Playwright**: E2Eテスト不要（物理デバイステスト）
- **Netlify**: デプロイ先なし（Raspberry Pi単体動作）

詳細: [ai-rules/_project_template/SETUP_AND_MCP.md](ai-rules/_project_template/SETUP_AND_MCP.md)

---

## 重要なルール

### 必須事項

#### セッション開始時
- ✅ Serenaメモリから状態を読み込む
- ✅ フェーズ・仕様を確認してから作業開始
- ✅ 不明点はユーザーに質問

#### 実装時
- ✅ 専用ブランチで作業（mainブランチ直接作業禁止）
- ✅ [命名規則](ai-rules/common/NAMING_CONVENTIONS.md) に準拠
- ✅ 影響範囲を確認してから修正

#### コミット前
- ✅ e2e-tester サブエージェントでE2Eテスト実施
- ✅ すべてのテストがパスすることを確認
- ✅ デバッグコード・不要コメントを削除

#### PR作成後
- ✅ code-reviewer サブエージェント レビューを依頼
- ✅ Critical問題は必ず修正してからマージ
- ✅ レビュー対応は即座に実施（Issue化は例外的）

#### マージ後
- ✅ docs-updater サブエージェントでドキュメント更新
- ✅ docs/ と Serenaメモリの両方を更新
- ✅ PR作成→レビュー→マージ→ドキュメント更新を1セットで完了

### 禁止事項

- ❌ mainブランチへの直接作業
- ❌ テスト未実施でのコミット
- ❌ Critical問題が残ったままのマージ
- ❌ ドキュメント更新なしでの作業完了
- ❌ デバッグコード・不要コメントのコミット
- ❌ git config の変更
- ❌ 破壊的gitコマンド（push --force, hard reset等、ユーザー明示指示除く）

---

## ドキュメント構成

### 参考資料（reference/）
- 仕様書・設計書（PDF、Excel等）
- サンプルデータ（CSV、JSON等）
- ワイヤーフレーム・ER図（画像）
- 外部API仕様書

詳細: [reference/README.md](reference/README.md)

### 人間用ドキュメント（docs/）
- `docs/DATABASE.md` - データベーススキーマ定義
- `docs/API.md` - API エンドポイント仕様
- `docs/SETUP.md` - 環境構築手順
- `docs/PHASES.md` - フェーズ管理（フェーズ管理時）

### AI用詳細仕様（Serenaメモリ）
- `database_specifications.md` - DB詳細仕様
- `api_specifications.md` - API詳細仕様
- `phase_progress.md` - フェーズ進捗
- `current_issues_and_priorities.md` - Issue・優先度

詳細: [ai-rules/common/DOCUMENTATION_GUIDE.md](ai-rules/common/DOCUMENTATION_GUIDE.md)

---

## コミットメッセージ形式

詳細: [ai-rules/common/COMMIT_GUIDELINES.md](ai-rules/common/COMMIT_GUIDELINES.md)

```
<type>: <subject>

<body>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Type**:
- `feat`: 新機能追加
- `fix`: バグ修正
- `docs`: ドキュメントのみの変更
- `refactor`: バグ修正や機能追加を含まないコードの変更
- `test`: テストの追加・修正
- `chore`: ビルドプロセスやツールの変更

---

## セッション管理

⚠️ AI側から適切なタイミングでセッション切り替えを提案します

詳細: [ai-rules/common/SESSION_MANAGEMENT.md](ai-rules/common/SESSION_MANAGEMENT.md)

### セッション切り替えタイミング
- トークン使用量が予算の70%を超えた場合
- 大きなマイルストーン完了時
- コンテキストが複雑になった場合

### セッション終了時の手順
1. Serenaメモリを更新（session_handover.md等）
2. 完了内容と次のタスクを記録
3. ユーザーに切り替えを提案

---

## AI用ガイドライン

### プロジェクト固有（ai-rules/_project_template/）
- [WORKFLOW.md](ai-rules/_project_template/WORKFLOW.md) - 開発ワークフロー
- [SETUP_AND_MCP.md](ai-rules/_project_template/SETUP_AND_MCP.md) - 環境構築・MCP設定
- [TESTING.md](ai-rules/_project_template/TESTING.md) - テストガイドライン
- [PR_AND_REVIEW.md](ai-rules/_project_template/PR_AND_REVIEW.md) - PR・レビュープロセス
- [ISSUE_GUIDELINES.md](ai-rules/_project_template/ISSUE_GUIDELINES.md) - Issue管理
- [DOCUMENTATION_GUIDE.md](ai-rules/_project_template/DOCUMENTATION_GUIDE.md) - ドキュメント管理

### 汎用（ai-rules/common/）
- [WORKFLOW.md](ai-rules/common/WORKFLOW.md) - 汎用ワークフロー
- [SESSION_MANAGEMENT.md](ai-rules/common/SESSION_MANAGEMENT.md) - セッション管理
- [PHASE_MANAGEMENT.md](ai-rules/common/PHASE_MANAGEMENT.md) - フェーズ管理
- [DOCUMENTATION_GUIDE.md](ai-rules/common/DOCUMENTATION_GUIDE.md) - ドキュメント管理
- [COMMIT_GUIDELINES.md](ai-rules/common/COMMIT_GUIDELINES.md) - コミットメッセージ
- [NAMING_CONVENTIONS.md](ai-rules/common/NAMING_CONVENTIONS.md) - 命名規則
- [ISSUE_GUIDELINES.md](ai-rules/common/ISSUE_GUIDELINES.md) - Issue管理
- [PR_PROCESS.md](ai-rules/common/PR_PROCESS.md) - PRプロセス
- [SETTINGS_JSON_GUIDE.md](ai-rules/common/SETTINGS_JSON_GUIDE.md) - settings.json設定

---

## 最終更新履歴

- {{CURRENT_DATE}}: 初期作成
