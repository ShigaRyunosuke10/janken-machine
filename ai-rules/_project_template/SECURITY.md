# セキュリティ対応ガイド（{{PROJECT_NAME}} 専用）

このドキュメントでは、セキュリティインシデントへの対応フローと予防策を定義します。

**プロジェクト固有**: このファイルは {{PROJECT_NAME}} プロジェクト専用の設定を含みます。

**最終更新**: {{CURRENT_DATE}}

---

## 概要

### セキュリティの基本方針

1. **予防第一**: 脆弱性を作り込まない
2. **早期検知**: 問題を早く見つける
3. **迅速な対応**: インシデント発生時は即座に対応
4. **継続的改善**: 学びを次に活かす

---

## 1. セキュリティベストプラクティス

### 1.1 コーディング時の注意事項

#### ✅ すべきこと

**入力検証**:
```typescript
// バリデーション必須
function createUser(email: string, password: string) {
  if (!isValidEmail(email)) {
    throw new Error("Invalid email");
  }
  if (!isStrongPassword(password)) {
    throw new Error("Password too weak");
  }
  // ...
}
```

**出力エスケープ**:
```typescript
// XSS 対策
<div>{escapeHtml(userInput)}</div>

// React は自動エスケープ（dangerouslySetInnerHTML は避ける）
```

**認証・認可**:
```typescript
// API エンドポイントは必ず認証チェック
router.get('/api/user/profile', authenticate, (req, res) => {
  // ...
});

// 権限チェック
router.delete('/api/admin/users/:id', authenticate, authorize('admin'), (req, res) => {
  // ...
});
```

**シークレット管理**:
```typescript
// 環境変数で管理（Git にコミットしない）
const apiKey = process.env.API_KEY;

// ❌NG
const apiKey = "sk_live_abcd1234"; // ハードコーディング禁止
```

#### ❌ してはいけないこと

**SQL インジェクション**:
```typescript
// ❌NG: 文字列連結
const query = `SELECT * FROM users WHERE email = '${email}'`;

// ✅OK: プレースホルダー使用
const query = 'SELECT * FROM users WHERE email = $1';
db.query(query, [email]);
```

**パスワード平文保存**:
```typescript
// ❌NG
user.password = password;

// ✅OK: ハッシュ化
user.password = await bcrypt.hash(password, 10);
```

**機密情報のログ出力**:
```typescript
// ❌NG
console.log('User password:', password);
console.log('API key:', apiKey);

// ✅OK
console.log('User authenticated:', userId);
```

### 1.2 依存関係の管理

#### 定期的な脆弱性チェック（週次）

```bash
# npm
npm audit
npm audit fix

# pip
pip list --outdated
pip-audit
```

#### 自動化（推奨）

```yaml
# .github/workflows/security.yml

name: Security Scan

on:
  schedule:
    - cron: '0 0 * * 0'  # 毎週日曜日

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run security audit
        run: npm audit --audit-level=moderate
```

---

## 2. セキュリティインシデント対応

### 2.1 インシデントの種類

| 種別 | 例 | 緊急度 |
|------|-----|--------|
| **データ漏洩** | ユーザー情報流出 | Critical |
| **不正アクセス** | アカウント乗っ取り | Critical |
| **脆弱性発見** | SQLインジェクション発見 | High |
| **DDoS攻撃** | サービス停止攻撃 | High |
| **マルウェア感染** | サーバー感染 | Critical |

### 2.2 インシデント対応フロー

```
[インシデント検知]
    ↓
[初動対応（5分以内）]
  - 影響範囲確認
  - 緊急度判定
    ↓
[封じ込め（15分以内）]
  - 攻撃遮断
  - サービス停止判断
    ↓
[根絶（1時間以内）]
  - 脆弱性修正
  - 不正アクセス排除
    ↓
[復旧]
  - サービス再開
  - 動作確認
    ↓
[事後対応]
  - ユーザー通知
  - 関係機関への報告
  - インシデントレポート作成
```

### 2.3 初動対応チェックリスト

- [ ] **検知（0分）**: インシデント確認
- [ ] **影響範囲（5分）**: どこまで影響しているか
- [ ] **封じ込め（15分）**: 被害拡大を防ぐ
- [ ] **証拠保全（30分）**: ログ・データ保存
- [ ] **通知判断（1時間）**: ユーザー・関係機関への通知要否
- [ ] **根絶（4時間）**: 脆弱性修正・攻撃者排除
- [ ] **復旧（24時間）**: サービス完全復旧
- [ ] **レポート（48時間）**: インシデントレポート作成

---

## 3. 脆弱性対応

### 3.1 脆弱性発見時の対応

#### 自社発見の場合

1. **影響範囲確認**
   - 本番環境に存在するか
   - 悪用された形跡はないか

2. **緊急度判定**
   - Critical: 即座に Hotfix
   - High: 当日中に修正
   - Medium: 計画的に修正

3. **修正・デプロイ**
   ```bash
   # Hotfix として対応
   git checkout -b hotfix-security-{{VULNERABILITY}}
   # 修正...
   # テスト...
   # デプロイ
   ```

4. **検証**
   - 脆弱性が修正されたか確認
   - 他の脆弱性がないか確認

#### 外部報告の場合

```
# セキュリティレポート受領テンプレート

件名: Re: セキュリティ脆弱性のご報告

ご報告ありがとうございます。
以下の内容で確認させていただきます。

- 脆弱性の種類: {{TYPE}}
- 影響範囲: {{SCOPE}}
- 再現手順: {{STEPS}}
- 修正予定: {{SCHEDULE}}

修正完了次第、ご連絡いたします。
```

### 3.2 Common Vulnerabilities（よくある脆弱性）

#### SQLインジェクション

**悪い例**:
```typescript
const query = `SELECT * FROM users WHERE id = ${userId}`;
```

**良い例**:
```typescript
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

#### XSS（クロスサイトスクリプティング）

**悪い例**:
```typescript
<div dangerouslySetInnerHTML={{__html: userInput}} />
```

**良い例**:
```typescript
<div>{userInput}</div>  // React は自動エスケープ

// または
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userInput)}} />
```

#### CSRF（クロスサイトリクエストフォージェリ）

**対策**:
```typescript
// CSRF トークン検証
app.use(csrf());

// SameSite Cookie
res.cookie('session', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});
```

#### 認証バイパス

**悪い例**:
```typescript
if (req.body.isAdmin) {  // クライアントから送信可能
  // 管理者権限付与
}
```

**良い例**:
```typescript
const user = await getUserFromToken(req.headers.authorization);
if (user.role === 'admin') {  // サーバー側で検証
  // 管理者権限付与
}
```

---

## 4. 認証・認可

### 4.1 パスワードポリシー

**最小要件**:
- 8文字以上
- 大文字・小文字・数字を含む
- 特殊文字を推奨

**実装例**:
```typescript
function isStrongPassword(password: string): boolean {
  if (password.length < 8) return false;
  if (!/[a-z]/.test(password)) return false;
  if (!/[A-Z]/.test(password)) return false;
  if (!/[0-9]/.test(password)) return false;
  return true;
}
```

### 4.2 JWT トークン管理

```typescript
// トークン生成
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }  // 有効期限必須
);

// トークン検証
try {
  const payload = jwt.verify(token, process.env.JWT_SECRET);
} catch (error) {
  // トークン無効
}
```

### 4.3 セッション管理

```typescript
// セッションタイムアウト
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    maxAge: 3600000,  // 1時間
    httpOnly: true,
    secure: true,  // HTTPS のみ
    sameSite: 'strict'
  },
  resave: false,
  saveUninitialized: false
}));
```

---

## 5. データ保護

### 5.1 データ暗号化

**保存時の暗号化**:
```typescript
// パスワード
const hashedPassword = await bcrypt.hash(password, 10);

// 機密データ
import crypto from 'crypto';
const encrypted = crypto.createCipheriv('aes-256-cbc', key, iv).update(data, 'utf8', 'hex');
```

**転送時の暗号化**:
- HTTPS 必須
- TLS 1.2 以上

### 5.2 個人情報の取り扱い

**最小化の原則**:
- 必要最小限のデータのみ収集
- 不要になったら削除

**アクセス制御**:
```typescript
// 自分の情報のみアクセス可能
router.get('/api/user/profile', authenticate, (req, res) => {
  if (req.user.id !== req.params.userId) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  // ...
});
```

---

## 6. 監視・検知

### 6.1 セキュリティログ

**記録すべきイベント**:
- ログイン成功・失敗
- パスワード変更
- 権限変更
- データアクセス（機密情報）
- API呼び出し（異常パターン）

**実装例**:
```typescript
// 監査ログ
logger.info('User login', {
  userId: user.id,
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  timestamp: new Date()
});
```

### 6.2 異常検知

**アラート条件**:
- ログイン失敗5回以上（10分以内）
- 同一IPから100リクエスト/分以上
- 深夜の管理者権限使用
- 大量データダウンロード

---

## 7. アクセス制御

### 7.1 最小権限の原則

```typescript
// ロール定義
enum Role {
  USER = 'user',
  MODERATOR = 'moderator',
  ADMIN = 'admin'
}

// 権限チェック
function authorize(requiredRole: Role) {
  return (req, res, next) => {
    if (!hasRole(req.user, requiredRole)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// 使用例
router.delete('/api/users/:id', authenticate, authorize(Role.ADMIN), deleteUser);
```

### 7.2 APIレート制限

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15分
  max: 100,  // 100リクエスト
  message: 'Too many requests'
});

app.use('/api/', limiter);
```

---

## 8. セキュリティチェックリスト

### 開発時

- [ ] 入力バリデーション実装
- [ ] 出力エスケープ実装
- [ ] 認証・認可実装
- [ ] シークレット環境変数化
- [ ] HTTPS 使用
- [ ] CSRF トークン実装
- [ ] SQLインジェクション対策
- [ ] XSS 対策

### コミット前

- [ ] シークレットがコミットされていないか確認
- [ ] 脆弱性スキャン実行（`npm audit`）
- [ ] code-reviewer でセキュリティチェック

### デプロイ前

- [ ] 環境変数設定確認
- [ ] HTTPS 設定確認
- [ ] セキュリティヘッダー設定確認
- [ ] ファイアウォール設定確認

### 定期確認（週次）

- [ ] 依存関係の脆弱性スキャン
- [ ] セキュリティログレビュー
- [ ] アクセス権限レビュー

---

## 9. インシデントレポート

### 9.1 レポート作成

`docs/SECURITY_INCIDENTS/{{DATE}}-{{INCIDENT}}.md`

```markdown
# セキュリティインシデントレポート: {{概要}}

## 基本情報
- 発生日時: {{DATETIME}}
- 検知方法: {{方法}}
- インシデント種別: {{種別}}
- 影響範囲: {{範囲}}
- 個人情報漏洩: {{有無}}

## 経緯
<詳細なタイムライン>

## 原因
<技術的な根本原因>

## 対応内容
<実施した対応>

## 影響を受けたユーザー
- 人数: {{NUMBER}}
- 影響内容: {{IMPACT}}
- 通知状況: {{STATUS}}

## 再発防止策
1. <防止策1>
2. <防止策2>
3. <防止策3>

## 学んだこと
<今後に活かすこと>

## 関係機関への報告
- [ ] 個人情報保護委員会（必要な場合）
- [ ] 警察（必要な場合）
```

### 9.2 ユーザー通知テンプレート

```
件名: 【重要】セキュリティインシデントのお知らせ

{{PROJECT_NAME}} をご利用いただきありがとうございます。

この度、{{DATE}}に発生したセキュリティインシデントに関してご報告いたします。

■ 発生した事象
{{INCIDENT_SUMMARY}}

■ 影響範囲
{{IMPACT}}

■ 対応状況
{{ACTION}}

■ お客様へのお願い
{{USER_ACTION}}

ご不明点がございましたら、お問い合わせください。

ご不便をおかけし、誠に申し訳ございません。
```

---

## 10. セキュリティリソース

### 参考資料

- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **CWE Top 25**: https://cwe.mitre.org/top25/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework

### ツール

- **脆弱性スキャン**: npm audit, Snyk, Dependabot
- **静的解析**: ESLint security plugin, Bandit (Python)
- **動的解析**: OWASP ZAP, Burp Suite

---

## 関連ドキュメント

- **[DEPLOYMENT.md](./DEPLOYMENT.md)**: デプロイ・リリースフロー
- **[HOTFIX.md](./HOTFIX.md)**: 緊急修正フロー
- **[OPERATIONS.md](./OPERATIONS.md)**: 運用フロー
- **[WORKFLOW.md](./WORKFLOW.md)**: 通常の開発ワークフロー

---

## 注意事項

- ⚠️ **シークレットは絶対にGitにコミットしない**
- ⚠️ **脆弱性発見時は即座に対応**
- ⚠️ **個人情報漏洩は法的報告義務あり**
- ⚠️ **定期的なセキュリティレビュー実施**
- ⚠️ **ユーザーへの迅速な通知が重要**
