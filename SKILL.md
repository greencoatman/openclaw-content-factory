# Content Factory - 智能内容生成助手

> 专为技术架构师打造的自动化内容生产工具
> 作者：@greencoatman
> 版本：1.0.0

## Description

Content Factory 是一个智能内容生成 Skill，专为技术公众号运营者设计。它能够：

- 🔍 **多平台热点监控**：自动搜索国内外技术热点
- ✍️ **深度文章生成**：基于技术架构视角生成专业分析
- 📊 **自动排版输出**：生成可直接发布的Word文档
- 🎯 **风格可选**：支持技术深度分析、资讯简报等多种风格

## Usage

### 基础使用
```
"运行content-factory，生成今天的技术架构文章"
"帮我写一篇关于云原生架构的深度分析"
"搜索最近的AI架构热点并整理成文档"
```

### 高级使用
```
"生成文章，主题Kubernetes，风格技术深度分析，字数3000"
"搜索热点，领域AI架构，输出到./articles，生成Word文档"
```

## Tools

- `web_search` - 网络搜索（国内外多平台）
- `file_system` - 文件读写
- `docx_generator` - Word文档生成
- `json_parser` - JSON数据处理
- `datetime` - 时间处理

## Permissions

- `internet_access` - 需要访问国内外搜索引擎
- `file_read` - 读取模板文件
- `file_write` - 写入生成的文章
- `subprocess` - 调用外部工具（搜索、文档生成）

## Configuration

配置文件：`config/default.yaml`

```yaml
# 搜索配置
search:
  sources:
    - zhihu          # 知乎
    - juejin         # 稀土掘金
    - weibo          # 微博热点
    - google         # Google News
    - hackernews     # Hacker News
    - github         # GitHub Trending
  max_results: 10
  timeout: 30

# 文章生成配置
generation:
  default_word_count: 3000
  style: "tech_architecture"  # 技术架构深度分析
  min_word_count: 2000
  max_word_count: 5000

# 输出配置
output:
  format: "docx"  # 输出Word文档
  default_dir: "./articles"
  template_dir: "./templates"
  
# 风格模板
styles:
  tech_architecture:
    name: "技术架构深度分析"
    structure:
      - introduction    # 引言（背景+问题+价值）
      - principle       # 技术原理
      - practice        # 实战案例
      - comparison      # 对比分析
      - conclusion      # 总结展望
    tone: "professional"
    code_examples: true
    tables: true
    
  news_brief:
    name: "资讯简报"
    structure:
      - headline        # 头条
      - summary         # 摘要
      - details         # 详情
      - impact          # 影响分析
    tone: "concise"
    code_examples: false
    tables: false

# 通知配置（可选）
notification:
  enabled: false
  # feishu_webhook: ""
  # wechat_webhook: ""
```

## Installation

### 方式1：通过ClawdHub安装
```bash
clawdhub install content-factory
```

### 方式2：手动安装
```bash
# 克隆仓库
git clone https://github.com/greencoatman/openclaw-content-factory.git

# 复制到OpenClaw skills目录
cp -r openclaw-content-factory ~/.openclaw/skills/

# 安装依赖
pip install -r requirements.txt
```

## Dependencies

```
python >= 3.8
python-docx >= 0.8.11
requests >= 2.28.0
pyyaml >= 6.0
beautifulsoup4 >= 4.11.0
```

## Examples

### 示例1：生成技术架构文章
```bash
# 输入
{
  "topic": "Kubernetes服务网格",
  "style": "tech_architecture",
  "word_count": 3000
}

# 输出
{
  "status": "success",
  "message": "文章生成成功",
  "data": {
    "filename": "2026-03-04-Kubernetes服务网格深度分析.docx",
    "path": "./articles/2026-03-04-Kubernetes服务网格深度分析.docx",
    "word_count": 3125,
    "topic": "Kubernetes服务网格",
    "sources": ["知乎", "掘金", "GitHub"]
  }
}
```

### 示例2：搜索热点自动生成
```bash
# 输入
{
  "mode": "auto",
  "domain": "AI架构",
  "style": "tech_architecture"
}

# 输出
{
  "status": "success",
  "message": "热点搜索并生成文章成功",
  "data": {
    "filename": "2026-03-04-AI架构最新趋势.docx",
    "hot_topics": ["DeepSeek V4", "MoE架构", "多模态AI"],
    "word_count": 3280
  }
}
```

## Project Structure

```
openclaw-content-factory/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── config/
│   └── default.yaml           # 默认配置
├── scripts/
│   ├── main.py                # 主入口
│   ├── searcher.py            # 搜索模块
│   ├── analyzer.py            # 分析模块
│   ├── writer.py              # 写作模块
│   ├── formatter.py           # 排版模块
│   └── utils.py               # 工具函数
├── templates/
│   ├── tech_architecture.md   # 技术架构模板
│   └── news_brief.md          # 资讯简报模板
├── tests/
│   └── test_main.py          # 测试用例
└── .gitignore
```

## Development

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

## License

MIT License - 详见 [LICENSE](LICENSE)

## Author

- GitHub: [@greencoatman](https://github.com/greencoatman)
- 公众号：技术架构观察

## Contributing

欢迎提交Issue和PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## Changelog

### v1.0.0 (2026-03-04)
- ✨ 初始版本发布
- 🔍 支持多平台热点搜索
- ✍️ 技术架构深度分析文章生成
- 📄 Word文档自动排版输出
- 🎨 支持多种文章风格模板

## Roadmap

- [ ] 接入飞书/钉钉通知
- [ ] 支持定时任务（Cron）
- [ ] 添加更多文章风格模板
- [ ] 支持图片自动插入
- [ ] 数据分析与报表功能
