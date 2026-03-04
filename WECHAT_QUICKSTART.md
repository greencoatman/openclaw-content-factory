# Content Factory 微信公众号自动发布 - 快速开始

## ✅ 功能已完成

自动将生成的技术文章发布到微信公众号草稿箱！

---

## 🚀 一键使用

```bash
# 生成文章 + 自动发布到草稿箱
python scripts/main.py \
  --topic "Kubernetes架构" \
  --word-count 3000 \
  --publish-wechat
```

**输出**：
- ✅ Word 文档：`./articles/2026-03-04-Kubernetes架构深度分析.docx`
- ✅ 微信草稿箱：文章已添加，可直接在后台编辑发布

---

## 📋 配置步骤

### 1. 获取微信公众号凭证

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. **设置与开发 > 基本配置**
3. 获取 **AppID** 和 **AppSecret**
4. **IP白名单** 添加您的服务器IP

### 2. 编辑配置文件

`config/wechat.yaml`：

```yaml
wechat:
  app_id: "wx235eea23e433b246"
  app_secret: "c077b6f512c034c35d63e4ebd5370057"
```

### 3. 测试

```bash
python scripts/test_wechat.py
```

### 4. 使用

```bash
# 方式1: 命令行
python scripts/main.py --topic "AI架构" --publish-wechat

# 方式2: JSON输入
echo '{"topic": "云原生", "publish_wechat": true}' | python scripts/main.py
```

---

## 🎯 工作流程

```
生成文章 → 转换为HTML → 上传到微信 → 添加到草稿箱
```

1. Content Factory 生成 Word 文档
2. 自动转换为微信公众号 HTML 格式
3. 调用微信 API 上传素材
4. 添加到草稿箱（可在后台编辑后发布）

---

## 📱 查看草稿

登录微信公众号后台：
- **内容管理 > 草稿箱**
- 找到刚生成的文章
- 编辑、预览、发布

---

## 💡 示例

```bash
# 生成并发布
python scripts/main.py \
  --mode auto \
  --domain "技术架构" \
  --publish-wechat

# 输出
✅ 文章已生成: 2026-03-04-OpenClaw技术架构深度分析.docx
✅ 已发布到微信公众号草稿箱
   Media ID: 9fHlMGS-UMMgSi6s2ovRSWSfA27ETlSkctk_g60flbEn6SXKg_T4suqeP24--7HX
```

---

详细文档见：[docs/WECHAT_PUBLISH.md](docs/WECHAT_PUBLISH.md)
