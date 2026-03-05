# 微信公众号发布最佳实践

> 基于 content-factory 实战经验总结

---

## ⚠️ 重要限制（必须遵守）

### 字段长度限制

| 字段 | 最大长度 | 错误码 | 说明 |
|------|---------|--------|------|
| **标题 (title)** | **12 字符** | 45003 | 中英文统一计算，超过即报错 |
| **作者 (author)** | **8 字符** | - | 建议简短 |
| **摘要 (digest)** | **20 字符** | 45004 | 超过会报错 |
| 内容 (content) | 无明确限制 | - | 建议合理长度 |

### 其他限制

- **封面图**：必须有 media_id（需先上传）
- **IP白名单**：必须配置服务器IP
- **Access Token**：有效期2小时，需缓存

---

## 🐛 常见错误与解决方案

### 错误码 45003 - 标题超长

```
错误：title size out of limit
原因：标题超过 12 字符
解决：
  - 截断标题为 10 字符 + ".."
  - 示例：'AI大模型推理优化深度分析' → 'AI大模型推理优化深..'
```

**代码修复**：
```python
if len(title) > 12:
    title = title[:10] + ".."
```

---

### 错误码 45004 - 摘要超长

```
错误：description size out of limit
原因：摘要超过 20 字符
解决：
  - 自动提取时限制 20 字符
  - 或手动指定更精准的摘要
```

**代码修复**：
```python
# 自动提取摘要
text = re.sub(r'<style[^>]*>.*?</style>', '', content_html, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'\s+', ' ', text).strip()
digest = text[:20] + "..." if len(text) > 20 else text
```

---

### 错误码 40007 - 无效的 media_id

```
错误：invalid media_id
原因：
  1. 封面图未上传
  2. media_id 过期或错误
解决：
  - 确保先上传封面图获取 media_id
  - 检查封面图上传是否成功
```

---

### 错误码 40164 - IP不在白名单

```
错误：invalid ip not in whitelist
原因：服务器IP未添加到白名单
解决：
  1. 登录微信公众平台
  2. 设置与开发 > 基本配置
  3. IP白名单 > 添加服务器IP
```

---

### 错误码 45106 - API不支持

```
错误：This API has been unsupported
原因：订阅号不支持某些API
解决：
  - 订阅号使用 draft/add 接口
  - 不要使用 add_news 接口
```

---

## ✅ 最佳实践

### 1. 标题处理

```python
# ✅ 正确做法
title = "AI大模型推理优化"  # 9字符，符合要求

# ❌ 错误做法
title = "AI大模型推理优化深度分析"  # 13字符，超出限制

# ✅ 自动截断
if len(title) > 12:
    title = title[:10] + ".."
```

### 2. 摘要提取

```python
# ✅ 正确做法 - 移除 style 标签再提取
text = re.sub(r'<style[^>]*>.*?</style>', '', content_html, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '', text)
text = re.sub(r'\s+', ' ', text).strip()
digest = text[:20] + "..." if len(text) > 20 else text

# ❌ 错误做法 - 直接提取会包含 style 内容
text = re.sub('<[^<]+?>', '', content_html)  # style 内容会残留
```

### 3. 作者设置

```python
# ✅ 正确做法
author = "CC"  # 2字符

# ❌ 错误做法
author = "技术架构观察"  # 6字符，超出建议

# ✅ 自动截断
if len(author) > 8:
    author = author[:8]
```

### 4. 封面图处理

```python
# ✅ 正确做法 - 先上传获取 media_id
thumb_media_id = upload_permanent_image(image_path)

# 然后再添加到文章
article = {
    "title": title,
    "thumb_media_id": thumb_media_id,  # 必须是有效的 media_id
    ...
}
```

### 5. Access Token 管理

```python
# ✅ 正确做法 - 缓存 + 提前刷新
class TokenManager:
    def get_token(self):
        # 检查缓存
        if self.cache and not self.is_expired():
            return self.cache['token']
        
        # 获取新 token
        token = self.fetch_new_token()
        
        # 缓存（提前5分钟过期）
        self.cache_token(token, expires_in=7200-300)
        return token

# ❌ 错误做法 - 每次都请求新 token
def get_token():
    return fetch_new_token()  # 频繁请求会被限流
```

---

## 📋 发布前检查清单

### 必查项目

- [ ] 标题 ≤ 12 字符
- [ ] 作者 ≤ 8 字符
- [ ] 摘要 ≤ 20 字符
- [ ] 封面图已上传
- [ ] thumb_media_id 有效
- [ ] IP白名单已配置
- [ ] Access Token 有效

### 可选优化

- [ ] 内容格式正确（HTML）
- [ ] 图片已上传（如有）
- [ ] 原文链接已填写（如有）
- [ ] 评论设置正确

---

## 🔧 调试技巧

### 1. 打印完整请求

```python
import json
print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")
```

### 2. 测试不同长度

```python
# 测试标题限制
for length in [10, 11, 12, 13, 14]:
    title = "A" * length
    test_publish(title=title)
```

### 3. 查看错误详情

```python
try:
    result = publish_article(...)
except Exception as e:
    print(f"错误详情: {e}")
    # 查看微信返回的错误码和消息
```

---

## 📚 参考资源

### 微信官方文档

- [草稿箱管理](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html)
- [素材管理](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html)
- [错误码说明](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Global_Return_Code.html)

### 相关文件

- `scripts/wechat_publisher.py` - 发布模块
- `config/wechat.yaml` - 配置文件
- `SECURITY.md` - 安全指南

---

## 💡 经验总结

### 关键发现

1. **标题限制最严格** - 12 字符是硬限制
2. **摘要也有限制** - 约 20 字符
3. **订阅号API受限** - 使用 draft/add 而非 add_news
4. **必须配置IP白名单** - 否则无法调用API
5. **封面图必须有** - 需要先上传获取 media_id

### 开发建议

1. **先测试再上线** - 用极简数据测试接口
2. **逐个验证限制** - 不要一次性发送所有字段
3. **保留调试日志** - 方便排查问题
4. **缓存 Access Token** - 减少API调用

---

**更新时间**: 2026-03-05
**版本**: v1.1.1
