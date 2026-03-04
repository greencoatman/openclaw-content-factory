# OpenClaw Content Factory

> 智能内容生成助手 - 专为技术架构师打造的自动化内容生产工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.ai)

## 🎯 项目简介

Content Factory 是一个 OpenClaw Skill，专为技术公众号运营者设计。它能够自动搜索技术热点，生成深度技术文章，并输出可直接发布的 Word 文档。

### 核心特性

- 🔍 **多平台热点监控** - 自动搜索国内外技术热点（知乎、掘金、GitHub、Hacker News）
- ✍️ **深度文章生成** - 基于技术架构视角生成专业分析文章
- 📊 **自动排版输出** - 生成可直接发布的 Word 文档（.docx格式）
- 🎨 **多种文章风格** - 支持技术深度分析、资讯简报等多种风格
- ⚡ **一键式操作** - 输入主题，自动生成完整文章

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
```

### 在 OpenClaw 中使用

```
"运行 content-factory，生成今天的技术架构文章"

"帮我写一篇关于云原生架构的深度分析"

"搜索最近的AI架构热点并整理成文档"
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

配置文件位于 `config/default.yaml`，可以自定义：

- **搜索源** - 知乎、掘金、GitHub、Hacker News 等
- **文章风格** - 技术深度分析、资讯简报
- **输出格式** - Word 文档（.docx）
- **字数范围** - 默认 3000 字

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

适合技术公众号的深度技术文章，结构包括：
1. 引言（背景+问题+价值）
2. 技术原理
3. 实战案例
4. 对比分析
5. 总结与展望

### 资讯简报

简洁明快的技术资讯汇总，结构包括：
1. 今日热点
2. 要点速览
3. 详细解读
4. 影响分析

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
