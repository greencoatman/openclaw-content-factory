# Content Factory - 使用指南

## 调用方式总览

| 方式 | 适用场景 | 难度 |
|------|---------|------|
| 1. Python直接运行 | 本地测试、调试 | ⭐ |
| 2. OpenClaw自然语言 | 日常对话使用 | ⭐⭐ |
| 3. OpenClaw CLI | 脚本化、自动化 | ⭐⭐ |
| 4. 定时任务(Cron) | 每日自动生成 | ⭐⭐⭐ |
| 5. API调用 | 集成到其他系统 | ⭐⭐⭐ |

---

## 方式1：Python直接运行（最简单）

### 安装依赖

```bash
cd openclaw-content-factory
pip install -r requirements.txt
```

### 基础调用

```bash
# 方式A：通过stdin传入JSON
echo '{"topic": "Kubernetes服务网格"}' | python scripts/main.py

# 方式B：通过命令行参数
python scripts/main.py --topic "DeepSeek架构" --style tech_architecture --word-count 3000

# 方式C：指定输出目录
python scripts/main.py --topic "云原生架构" --output-dir ./my-articles
```

### 高级用法

```bash
# 自动生成（搜索热点）
echo '{"mode": "auto", "domain": "AI架构"}' | python scripts/main.py

# 完整参数
echo '{
  "topic": "微服务架构",
  "style": "tech_architecture",
  "word_count": 3000,
  "output_dir": "./articles"
}' | python scripts/main.py
```

### 输出结果

```json
{
  "status": "success",
  "message": "文章生成成功",
  "data": {
    "filename": "2026-03-04-微服务架构深度分析.docx",
    "path": "./articles/2026-03-04-微服务架构深度分析.docx",
    "topic": "微服务架构",
    "word_count": 3125
  }
}
```

---

## 方式2：OpenClaw自然语言（最方便）

### 前提条件

```bash
# 1. 将Skill复制到OpenClaw目录
cp -r openclaw-content-factory ~/.openclaw/skills/

# 或者创建软链接
ln -s ~/openclaw-content-factory ~/.openclaw/skills/content-factory
```

### 自然语言调用

在 OpenClaw 对话中直接说：

```
"运行 content-factory，生成今天的技术架构文章"

"帮我写一篇关于 Kubernetes 的深度分析"

"搜索最近的 AI 架构热点并整理成文档"

"生成文章，主题 DeepSeek-V4，风格技术深度分析，字数 3000"

"自动搜索云原生热点，生成资讯简报"
```

OpenClaw 会自动解析您的意图，调用 Skill 并返回结果。

---

## 方式3：OpenClaw CLI（适合脚本）

```bash
# 直接调用 Skill
openclaw skill run content-factory --topic "云原生架构"

# 带参数
openclaw skill run content-factory \
  --topic "微服务架构" \
  --style tech_architecture \
  --word-count 3000
```

---

## 方式4：定时任务 - Cron（自动化）

### 编辑定时任务

```bash
crontab -e
```

### 添加定时任务

```bash
# 每天早上 9:00 自动生成文章
0 9 * * * cd ~/openclaw-content-factory && echo '{"mode":"auto","domain":"AI架构"}' | python scripts/main.py >> /var/log/content-factory.log 2>&1

# 每周一早上 8:00 生成周报
0 8 * * 1 cd ~/openclaw-content-factory && echo '{"mode":"auto","domain":"技术架构","style":"news_brief"}' | python scripts/main.py

# 每天下午 6:00 生成日报
0 18 * * * cd ~/openclaw-content-factory && python scripts/main.py --mode auto --domain "云原生"
```

---

## 方式5：API调用（系统集成）

### 作为 Python 模块调用

```python
import sys
sys.path.insert(0, '/path/to/openclaw-content-factory/scripts')

from searcher import HotSearcher
from writer import ArticleWriter
from utils import ConfigLoader

# 加载配置
config = ConfigLoader.load()

# 搜索热点
searcher = HotSearcher(config)
sources = searcher.search("Kubernetes", limit=5)

# 生成文章
writer = ArticleWriter(config)
article = writer.generate(
    topic="Kubernetes架构",
    style="tech_architecture",
    word_count=3000,
    sources=sources
)

# 保存文档
filepath = writer.save_to_docx(article, "./articles")
print(f"文章已生成: {filepath}")
```

---

## 快速开始（推荐步骤）

### Step 1: 克隆仓库

```bash
git clone https://github.com/greencoatman/openclaw-content-factory.git
cd openclaw-content-factory
```

### Step 2: 安装依赖

```bash
pip install -r requirements.txt
```

### Step 3: 试运行

```bash
echo '{"topic": "测试主题", "word_count": 1000}' | python scripts/main.py
```

### Step 4: 查看输出

```bash
ls -la articles/
# 应该能看到生成的 .docx 文件
```

---

## 常用配置修改

### 修改默认输出目录

编辑 `config/default.yaml`：

```yaml
output:
  default_dir: "./articles"  # 改成您的目录
```

### 修改搜索源

```yaml
search:
  sources:
    zhihu:
      enabled: true
    juejin:
      enabled: true
    github:
      enabled: true
```

---

## 故障排查

### 问题1：找不到模块

```bash
pip install -r requirements.txt
```

### 问题2：中文显示乱码

```bash
export PYTHONIOENCODING=utf-8
```

### 问题3：Word生成失败

```bash
pip install python-docx
```
