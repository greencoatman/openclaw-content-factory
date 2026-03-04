# 安全配置指南

## ⚠️ 重要安全提示

**永远不要将以下信息提交到 Git 或公开到 GitHub：**

- ❌ AppID 和 AppSecret
- ❌ Access Token
- ❌ 任何 API 密钥
- ❌ 数据库密码
- ❌ 服务器凭证

---

## 🔐 正确的配置方式

### 方法1：使用示例配置文件（推荐）

```bash
# 1. 复制示例配置
cp config/wechat.yaml.example config/wechat.yaml

# 2. 编辑配置文件，填入真实密钥
nano config/wechat.yaml

# 3. 确认配置文件已被 .gitignore 排除
git status  # 不应该看到 wechat.yaml
```

### 方法2：使用环境变量

```bash
# 设置环境变量
export WECHAT_APP_ID="your_app_id"
export WECHAT_APP_SECRET="your_app_secret"

# 代码中读取
import os
app_id = os.getenv('WECHAT_APP_ID')
app_secret = os.getenv('WECHAT_APP_SECRET')
```

### 方法3：使用密钥管理服务

- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- 阿里云密钥管理服务

---

## 🛡️ 如果密钥已泄露怎么办？

### 立即行动清单

1. ✅ **立即重置密钥**
   - 登录微信公众平台
   - 重置 AppSecret
   - 更新本地配置

2. ✅ **检查异常访问**
   - 查看公众号后台日志
   - 检查是否有异常操作

3. ✅ **更新代码**
   - 从 Git 历史中移除敏感信息
   - 更新 .gitignore
   - 强制推送

4. ✅ **通知相关人员**
   - 如果是团队项目，通知所有成员

---

## 📋 .gitignore 检查清单

确保以下内容在 `.gitignore` 中：

```gitignore
# 敏感配置
config/wechat.yaml
config/*.local.yaml
.env
.env.local

# Token 缓存
.wechat_token_cache.json
*.token
*.secret

# 密钥文件
*.key
*.pem
*.p12
```

---

## 🔍 Git 历史清理（如果已经提交）

### 方法1：使用 BFG Repo-Cleaner（推荐）

```bash
# 安装 BFG
brew install bfg  # macOS
# 或下载：https://rtyley.github.io/bfg-repo-cleaner/

# 清理敏感文件
bfg --delete-files wechat.yaml
bfg --replace-text passwords.txt  # 替换密码文本

# 清理并推送
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### 方法2：使用 git filter-branch

```bash
# 从历史中移除文件
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config/wechat.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送
git push origin --force --all
git push origin --force --tags
```

---

## ✅ 最佳实践总结

1. **使用示例配置**
   - `.example` 文件提交到 Git
   - 真实配置文件加入 .gitignore

2. **定期轮换密钥**
   - 每3个月更换一次 AppSecret
   - 旧密钥过期前更新

3. **最小权限原则**
   - 只授予必要的 API 权限
   - 为不同环境使用不同密钥

4. **监控异常访问**
   - 定期检查 API 调用日志
   - 设置告警通知

5. **团队协作**
   - 使用密钥管理服务
   - 不通过聊天工具传递密钥

---

## 📞 如有疑问

- GitHub 安全指南：https://docs.github.com/en/code-security
- 微信公众平台文档：https://developers.weixin.qq.com/doc/

**记住：安全无小事，密钥泄露后果严重！**
