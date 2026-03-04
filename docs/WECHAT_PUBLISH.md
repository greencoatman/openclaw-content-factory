# 微信公众号自动发布功能使用指南

> 自动将生成的文章发布到微信公众号草稿箱

---

## 🎯 功能说明

Content Factory 现已支持**一键发布到微信公众号草稿箱**！

生成文章后，自动：
1. ✅ 将 Word 文档转换为 HTML 格式
2. ✅ 上传到微信公众号素材库
3. ✅ 添加到草稿箱，等待发布

---

## 📋 前提条件

### 1. 获取微信公众号凭证

访问 [微信公众平台](https://mp.weixin.qq.com/)：

1. 登录公众号后台
2. 进入 **设置与开发 > 基本配置**
3. 获取 **AppID** 和 **AppSecret**
4. 配置 **IP白名单**（添加您的服务器IP）

### 2. 配置文件

编辑 `config/wechat.yaml`：

```yaml
wechat:
  app_id: "wx235eea23e433b246"          # 您的 AppID
  app_secret: "c077b6f512c034c35d63e4ebd5370057"  # 您的 AppSecret
  account_type: "subscription"          # 订阅号

publish:
  mode: "draft"  # 草稿箱模式
  defaults:
    author: "技术架构观察"  # 默认作者
```

---

## 🚀 使用方法

### 方式1：命令行参数

```bash
# 生成文章并发布到草稿箱
python scripts/main.py \
  --topic "Kubernetes架构" \
  --publish-wechat

# 完整参数
python scripts/main.py \
  --topic "DeepSeek V4架构揭秘" \
  --style tech_architecture \
  --word-count 3000 \
  --publish-wechat
```

### 方式2：JSON输入

```bash
echo '{
  "topic": "云原生架构",
  "style": "tech_architecture",
  "word_count": 3000,
  "publish_wechat": true
}' | python scripts/main.py
```

### 方式3：OpenClaw 自然语言

```
"运行 content-factory，生成 AI 架构文章，发布到公众号"

"写一篇关于 Kubernetes 的文章，字数 3000，发布到微信草稿箱"
```

---

## 🧪 测试功能

运行测试脚本：

```bash
cd scripts
python test_wechat.py
```

测试流程：
1. ✅ 测试获取 Access Token
2. ✅ 测试 Word 转 HTML
3. ✅ 测试发布到草稿箱（可选）

---

## 📤 发布流程

### 完整工作流程

```bash
# Step 1: 生成文章 + 自动发布
python scripts/main.py \
  --mode auto \
  --domain "技术架构" \
  --publish-wechat

# Step 2: 前往公众号后台
# 登录 https://mp.weixin.qq.com/
# 进入 "内容管理 > 草稿箱"
# 查看并编辑文章
# 点击 "发布" 即可推送给粉丝
```

### 输出示例

```json
{
  "status": "success",
  "message": "文章生成成功，已发布到微信公众号草稿箱",
  "data": {
    "filename": "2026-03-04-Kubernetes架构深度分析.docx",
    "path": "./articles/2026-03-04-Kubernetes架构深度分析.docx",
    "topic": "Kubernetes架构",
    "word_count": 3125,
    "wechat": {
      "media_id": "xxxx",
      "draft_id": "yyyy",
      "published_at": "2026-03-04 17:30:00"
    }
  }
}
```

---

## ⚙️ 高级配置

### 自定义文章样式

编辑 `config/wechat.yaml`：

```yaml
content:
  style:
    font_family: "PingFang SC, Microsoft YaHei, sans-serif"
    font_size: "16px"
    line_height: "1.8"
    
    heading:
      h1:
        font_size: "28px"
        color: "#1a1a1a"
      h2:
        font_size: "24px"
        color: "#2c3e50"
```

### 默认作者和评论设置

```yaml
publish:
  defaults:
    author: "您的公众号名称"
    is_original: 1              # 1-原创，0-非原创
    need_open_comment: 1        # 1-打开评论，0-关闭
    only_fans_can_comment: 0    # 1-仅粉丝可评论，0-所有人
```

---

## 🔧 故障排查

### 问题1：Access Token 获取失败

```
错误: 40013 - invalid appid
```

**解决**:
- 检查 `config/wechat.yaml` 中的 `app_id` 是否正确
- 确认公众号类型（订阅号/服务号）

---

### 问题2：IP白名单错误

```
错误: 61004 - access denied
```

**解决**:
1. 进入公众号后台
2. **设置与开发 > 基本配置 > IP白名单**
3. 添加您的服务器IP地址

---

### 问题3：素材上传失败

```
错误: 40007 - invalid media_id
```

**解决**:
- 检查图片格式（支持 jpg, png）
- 图片大小不超过 2MB
- 封面图尺寸建议 900x383

---

### 问题4：HTML转换问题

如果发布后格式不正确，可以：

1. 检查 Word 文档的样式
2. 调整 `config/wechat.yaml` 中的 HTML 样式配置
3. 手动在草稿箱中编辑调整

---

## 📅 定时自动发布

### 每日自动生成并发布

```bash
# 编辑 crontab
crontab -e

# 每天早上 9:00 自动生成并发布
0 9 * * * cd ~/content-factory-skill && echo '{"mode":"auto","domain":"AI架构","publish_wechat":true}' | python scripts/main.py
```

### Windows 计划任务

```powershell
# 创建每日任务
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\scripts\main.py --mode auto --publish-wechat"
$trigger = New-ScheduledTaskTrigger -Daily -At "9:00AM"
Register-ScheduledTask -TaskName "ContentFactoryDaily" -Action $action -Trigger $trigger
```

---

## 💡 最佳实践

### 1. 分离生成和发布

```bash
# 先生成，不发布
python scripts/main.py --topic "AI架构"

# 检查文章质量后，单独发布
python scripts/wechat_publisher.py \
  ./articles/2026-03-04-AI架构深度分析.docx \
  "AI架构深度分析"
```

### 2. 批量发布

```python
# batch_publish.py
from wechat_publisher import WeChatPublisher
import os

publisher = WeChatPublisher()
articles_dir = "./articles"

for filename in os.listdir(articles_dir):
    if filename.endswith('.docx'):
        docx_path = os.path.join(articles_dir, filename)
        title = filename.replace('.docx', '')
        
        html = publisher.convert_docx_to_html(docx_path)
        publisher.publish_article(title, html)
        
        print(f"✅ 已发布: {title}")
```

---

## 📊 API 调用限制

微信公众号 API 限制：
- Access Token 有效期：**2小时**
- 每日调用上限：根据公众号类型不同
- 建议使用缓存机制（已内置）

---

## 🎉 完整示例

```bash
# 1. 配置公众号信息（一次性）
nano config/wechat.yaml

# 2. 测试连接
python scripts/test_wechat.py

# 3. 生成并发布文章
python scripts/main.py \
  --mode auto \
  --domain "云原生" \
  --publish-wechat

# 4. 查看草稿箱
# 访问 https://mp.weixin.qq.com/
# 内容管理 > 草稿箱

# 5. 编辑并发布
# 点击文章 > 编辑 > 发布
```

---

## 🔗 相关资源

- [微信公众平台文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [素材管理接口](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html)
- [草稿箱接口](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html)

---

**祝您使用愉快！** 🚀

如有问题，请提交 [GitHub Issue](https://github.com/greencoatman/openclaw-content-factory/issues)
