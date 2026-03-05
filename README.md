# OpenClaw Content Factory

> 智能内容生成助手 - 专为技术架构师打造的自动化内容生产工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.ai)

## 🎯 项目简介

Content Factory 是一个 OpenClaw Skill，专为技术公众号运营者设计。它能够自动搜索技术热点，生成深度技术文章，并输出可直接发布的 Word 文档。

### 核心特性

- 🔥 **爆款选题引擎** - 自动发现高热度话题，分析爆款潜力（NEW!）
- 🔍 **多平台热点监控** - 自动搜索国内外技术热点（知乎、掘金、GitHub）
- ✍️ **自然语言写作** - 生成流畅易读的文章，无AI痕迹（NEW!）
- 🖼️ **丰富内容形式** - 案例、数据、对比、建议、配图提示（NEW!）
- 📊 **自动排版输出** - 生成可直接发布的 Word 文档（.docx格式）
- 🎨 **多种文章风格** - 支持技术深度分析、资讯简报等多种风格
- ⚡ **一键式操作** - 输入主题，自动生成完整文章
- 📱 **微信公众号自动发布** - 一键发布到草稿箱（NEW!）

## 📦 安装

### 方式1：通过 ClawdHub 安装（推荐）

```bash
clawdhub install content-factory
```

### 方式2：手动安装

```bash
# 克隆仓库
git clone https://github.com/greencoatman/openclaw-content-factory.git

# 进入目录
cd openclaw-content-factory

# 安装依赖
pip install -r requirements.txt

# 复制到 OpenClaw skills 目录
cp -r . ~/.openclaw/skills/content-factory
```

## 🚀 使用

### 基础用法

```bash
# 输入主题，自动生成文章
echo '{"topic": "Kubernetes服务网格"}' | python scripts/main.py

# 指定风格和字数
echo '{"topic": "DeepSeek架构", "style": "tech_architecture", "word_count": 3000}' | python scripts/main.py

# 爆款选题模式（自动搜索热点）
python scripts/main.py --mode auto --domain "AI架构"

# 生成并发布到微信公众号
python scripts/main.py --mode auto --domain "AI架构" --publish-wechat
```

### 在 OpenClaw 中使用

```
"运行 content-factory，生成今天的技术架构文章"

"帮我写一篇关于云原生架构的深度分析"

"搜索AI架构热点，自动生成爆款文章并发布到微信"
```

## 📁 项目结构

```
openclaw-content-factory/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── LICENSE                     # 许可证
├── config/
│   └── default.yaml           # 默认配置
├── scripts/
│   ├── main.py                # 主入口
│   ├── searcher.py            # 搜索模块
│   ├── writer.py              # 写作模块
│   └── utils.py               # 工具函数
├── templates/
│   ├── tech_architecture.md   # 技术架构模板
│   └── news_brief.md          # 资讯简报模板
└── tests/
    └── test_main.py          # 测试用例
```

## ⚙️ 配置

### 基础配置

配置文件位于 `config/default.yaml`，可以自定义：

- **搜索源** - 知乎、掘金、GitHub 等
- **文章风格** - 技术深度分析、资讯简报
- **输出格式** - Word 文档（.docx）
- **字数范围** - 默认 2000 字

### 微信公众号配置（可选）

如需一键发布到微信公众号，请配置 `config/wechat.yaml`：

```yaml
wechat:
  app_id: "your-app-id"          # 从微信公众平台获取
  app_secret: "your-app-secret"  # 从微信公众平台获取
  account_type: "subscription"   # 订阅号
```

配置步骤：
1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 开发 > 基本配置 > 获取 AppID 和 AppSecret
3. 设置服务器 IP 白名单
4. 复制 `config/wechat.yaml.example` 为 `config/wechat.yaml`
5. 填入你的 AppID 和 AppSecret

## 🛠️ 开发

### 本地测试

```bash
# 进入目录
cd openclaw-content-factory

# 安装依赖
pip install -r requirements.txt

# 运行测试
echo '{"topic": "测试主题", "style": "tech_architecture"}' | python scripts/main.py

# 运行单元测试
python -m pytest tests/
```

### 调试模式

```bash
# 开启调试日志
DEBUG=1 python scripts/main.py
```

## 📝 文章风格

### 技术架构深度分析（默认）

适合技术公众号的深度技术文章，爆款结构包括：
1. **吸睛开场** - 钩子语句，引发共鸣
2. **痛点分析** - 三大核心挑战
3. **[配图提示]** - 整体架构图占位
4. **技术原理** - 分层讲解（基础设施/服务编排/应用层）
5. **实战案例** - 大厂真实场景
   - 案例背景
   - 解决方案
   - 踩坑记录
   - 数据成果
6. **方案对比** - 单体/微服务/Serverless 对比表
7. **总结与展望** - 行动清单 + 2026趋势
8. **互动引导** - 评论区话题

### 资讯简报

简洁明快的技术资讯汇总，结构包括：
1. 今日热点
2. 要点速览
3. 详细解读
4. 影响分析

---

## 🎨 内容特色

### 自然语言写作
- 无 Markdown 标记（**、##、- 等）
- 口语化表达，降低 AI 感
- 流畅易读，像真人写作

### 丰富内容形式
- 📊 **数据支撑** - 百分比、性能指标
- 🏢 **大厂案例** - 真实场景，有细节
- ⚠️ **踩坑记录** - 具体问题和解决方案
- ✅ **行动清单** - 可执行的建议
- 💬 **互动引导** - 提高评论互动

### 配图提示
文章中自动插入配图位置提示：
```
[配图：整体架构图]
[配图：分层架构详图]
[配图：改造前后对比图]
```

## 📄 输出示例

生成的 Word 文档包含：
- 专业的标题和元信息
- 清晰的章节结构
- 自动排版（字体、行距、缩进）
- 参考资料列表
- 页脚作者信息

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📜 许可证

[MIT](LICENSE) © 2026 @greencoatman

---

## 📋 更新日志

### v1.1.0 (2026-03-05)
- ✨ **爆款选题引擎** - 自动追踪热点，分析爆款潜力
- ✨ **微信公众号发布** - 一键发布到草稿箱
- ✨ **自然语言写作** - 移除 Markdown 标记，降低 AI 感
- ✨ **丰富内容结构** - 案例、踩坑、数据、对比、建议
- ✨ **图片占位提示** - 自动提示插入配图位置
- 🔧 **修复编码问题** - 解决中文乱码
- 🔧 **修复微信限制** - 标题/摘要长度自动适配

### v1.0.0 (2026-03-04)
- ✨ 初始版本发布
- 🔍 支持多平台热点搜索
- ✍️ 技术架构深度分析文章生成
- 📄 Word文档自动排版输出

---

## 👤 作者

- **GitHub**: [@greencoatman](https://github.com/greencoatman)
- **公众号**: 二进制跳动

## 🙏 致谢

- [OpenClaw](https://openclaw.ai) - 强大的 AI Agent 平台
- [python-docx](https://python-docx.readthedocs.io/) - Word 文档生成库
- 所有开源社区贡献者

## 📮 联系

如有问题或建议，欢迎通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/greencoatman/openclaw-content-factory/issues)
- 关注公众号：技术架构观察

---

**如果这个项目对你有帮助，请给个 Star ⭐ 支持一下！**
