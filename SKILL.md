# Content Factory - 智能内容生成助手

> 专为技术架构师打造的自动化内容生产工具  
> 支持热点追踪、爆款文章生成、微信公众号一键发布  
> 作者：@greencoatman  
> 版本：1.1.0

---

## Description

Content Factory 是一个智能内容生成 Skill，专为技术公众号运营者设计。它能够：

- 🔥 **爆款选题引擎**：自动发现高热度话题，分析爆款潜力
- ✍️ **自然语言写作**：生成流畅易读的文章，无AI痕迹
- 🖼️ **丰富内容形式**：案例、数据、对比、建议、配图提示
- 📱 **微信一键发布**：自动排版，直接发布到公众号草稿箱
- 🎯 **风格可选**：技术深度分析、资讯简报等多种风格

---

## What's New in v1.1.0

### 爆款选题引擎
- 自动追踪 AI架构/云原生/架构设计/AI工具 热点
- 分析选题潜力（时效性、实用性、话题性、稀缺性）
- 智能推荐标签和目标读者

### 微信公众号发布
- 直接发布到草稿箱
- 自动处理标题、摘要长度限制
- 内联样式排版，支持手机阅读

### 自然语言写作
- 移除所有 Markdown 标记（**、##、- 等）
- 模拟真人写作风格
- 口语化表达，降低AI感

### 丰富内容结构
- 吸睛开场（钩子语句）
- 痛点分析
- 大厂实战案例
- 踩坑记录
- 数据成果对比
- 方案对比分析
- 行动建议清单
- 互动引导

---

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
"自动模式，发布到微信公众号"
```

### 微信公众号发布
```bash
# 自动生成热点文章并发布到微信
python scripts/main.py --mode auto --domain "AI架构" --publish-wechat

# 指定主题发布
python scripts/main.py --topic "Kubernetes" --word-count 2000 --publish-wechat
```

---

## Configuration

配置文件：`config/default.yaml`

```yaml
# 搜索配置
search:
  sources:
    - zhihu          # 知乎
    - juejin         # 稀土掘金
    - github         # GitHub Trending
  max_results: 10
  timeout: 30

# 文章生成配置
generation:
  default_word_count: 2000
  style: "tech_architecture"
  min_word_count: 1500
  max_word_count: 5000

# 爆款选题配置
viral_topics:
  AI架构:
    - "DeepSeek R1 推理优化"
    - "GPT-5 架构揭秘"
    - "AI Agent 工作流设计"
    - "大模型成本控制实战"

# 输出配置
output:
  format: "docx"
  default_dir: "./articles"
  template_dir: "./templates"

# 微信公众号配置（config/wechat.yaml）
wechat:
  app_id: "your-app-id"
  app_secret: "your-app-secret"
  account_type: "subscription"
```

---

## Content Structure

### 文章结构（爆款模板）

```
标题：[爆款标题，如"Kubernetes 2026新特性实战踩坑"]

引言
├── 钩子开场（"最近很多读者问我..."）
├── 背景引入
├── [配图：整体架构图]
├── 痛点分析（三大挑战）
├── 文章价值预告
└── 参考来源说明

技术原理
├── [配图：分层架构图]
├── 基础设施层
│   ├── 核心组件
│   ├── 性能指标
│   └── [配图：基础设施详图]
├── 服务编排层
│   ├── 设计哲学
│   └── 架构师建议
└── 应用层
    └── 前端优化策略

实战案例
├── 案例背景（大厂真实场景）
├── [配图：架构对比图]
├── 解决方案（三阶段实施）
├── 踩坑记录
│   ├── 坑1：微服务拆分过细
│   └── 坑2：服务发现性能瓶颈
└── 实施成果（数据对比）

对比分析
├── 方案一：单体架构
├── 方案二：微服务架构
├── 方案三：Serverless架构
├── [配图：架构对比示意图]
└── 选型建议

总结与展望
├── 核心总结
├── 架构师行动清单（5条）
├── 2026年趋势展望（4点）
└── 互动引导
```

---

## WeChat Publishing

### 微信公众号限制

| 字段 | 限制 | 说明 |
|------|------|------|
| **标题** | ≤ 12 字符 | 超过会报错 45003 |
| **作者** | ≤ 8 字符 | 建议简短 |
| **摘要** | ≤ 20 字符 | 超过会报错 45004 |
| **内容** | 无明确限制 | 支持 HTML 内联样式 |

### 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 40007 | invalid media_id | 检查封面图是否正确上传 |
| 45003 | title size out of limit | 标题超长，限制12字符内 |
| 45004 | description size out of limit | 摘要超长，限制20字符内 |
| 40164 | invalid ip not in whitelist | IP不在白名单，需添加 |

### 最佳实践

1. **标题处理**
   - 自动截断到 12 字符
   - 使用爆款关键词（实战、踩坑、揭秘、趋势）

2. **摘要提取**
   - 自动提取正文前 20 字符
   - 或手动指定更精准的摘要

3. **封面图**
   - 使用默认封面图
   - 建议尺寸 900x383（2.35:1）

4. **IP白名单**
   - 在微信公众平台后台配置
   - 添加服务器出口IP

---

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

# 配置微信公众号（可选）
cp config/wechat.yaml.example config/wechat.yaml
# 编辑 wechat.yaml 填入你的 AppID 和 AppSecret
```

---

## Dependencies

```
python >= 3.8
python-docx >= 0.8.11
requests >= 2.28.0
pyyaml >= 6.0
beautifulsoup4 >= 4.11.0
Pillow >= 9.0.0  # 图片处理
```

---

## Examples

### 示例1：生成爆款文章并发布

```bash
# 运行命令
python scripts/main.py --mode auto --domain "AI架构" --word-count 2000 --publish-wechat

# 输出示例
启动爆款选题引擎...
爆款选题: DeepSeek R1 推理优化实战
爆款潜力: 93/100
推荐标签: AI, 大模型, 人工智能, 架构设计
目标读者: 架构师, 技术经理, 全栈开发

搜索到 5 条相关资料
文章生成完成
字数: 2189

开始发布文章: DeepSeek R1推理优化实..
添加到草稿箱...
   标题: 'DeepSeek R1推理优化实..' (长度: 12)
   作者: 'CC' (长度: 2)
   摘要: '最近很多读者问我...' (长度: 20)
   内容长度: 8974 字符
发布成功！
   - Draft Media ID: 9fHlMGS-UMMgSi6s2ovRS...
```

### 示例2：仅生成Word文档

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
    "filename": "2026-03-05-Kubernetes服务网格深度分析.docx",
    "path": "./articles/2026-03-05-Kubernetes服务网格深度分析.docx",
    "word_count": 3125,
    "topic": "Kubernetes服务网格",
    "sources": ["知乎", "掘金", "GitHub"]
  }
}
```

---

## Project Structure

```
content-factory/
├── SKILL.md                    # 技能定义文件（本文档）
├── README.md                   # 项目说明
├── requirements.txt            # Python依赖
├── config/
│   ├── default.yaml           # 默认配置
│   └── wechat.yaml            # 微信公众号配置
├── scripts/
│   ├── main.py                # 主入口
│   ├── searcher.py            # 搜索模块（含爆款选题引擎）
│   ├── writer.py              # 写作模块（自然语言版）
│   ├── wechat_publisher.py    # 微信发布模块
│   └── utils.py               # 工具函数
├── templates/
│   ├── tech_architecture.md   # 技术架构模板
│   └── news_brief.md          # 资讯简报模板
├── docs/
│   └── WECHAT_BEST_PRACTICES.md  # 微信发布最佳实践
├── articles/                  # 生成文章存放目录
└── tests/
    └── test_main.py          # 测试用例
```

---

## Development

### 本地测试
```bash
# 进入目录
cd content-factory

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

# 测试微信发布（不实际发送）
python scripts/test_wechat.py
```

---

## Changelog

### v1.1.0 (2026-03-05)
- ✨ **爆款选题引擎**：自动追踪热点，分析爆款潜力
- ✨ **微信公众号发布**：一键发布到草稿箱
- ✨ **自然语言写作**：移除 Markdown 标记，降低 AI 感
- ✨ **丰富内容结构**：案例、踩坑、数据、对比、建议
- ✨ **图片占位提示**：自动提示插入配图位置
- 🔧 **修复编码问题**：解决中文乱码
- 🔧 **修复标题/摘要长度限制**：适配微信规则

### v1.0.0 (2026-03-04)
- ✨ 初始版本发布
- 🔍 支持多平台热点搜索
- ✍️ 技术架构深度分析文章生成
- 📄 Word文档自动排版输出
- 🎨 支持多种文章风格模板

---

## Roadmap

- [x] 爆款选题引擎
- [x] 微信公众号发布
- [x] 自然语言写作
- [ ] AI图片自动生成（封面、配图）
- [ ] 定时任务（Cron）
- [ ] 数据分析与报表功能
- [ ] 接入飞书/钉钉通知
- [ ] 支持更多文章风格模板

---

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

---

## Troubleshooting

### 问题1：中文乱码

```
解决：确保文件编码为 UTF-8，PowerShell 执行 chcp 65001
```

### 问题2：微信发布失败 45003

```
错误：title size out of limit
原因：标题超过 12 字符
解决：已自动截断，建议控制在 10 字符以内
```

### 问题3：微信发布失败 45004

```
错误：description size out of limit
原因：摘要超过 20 字符
解决：已自动截断到 20 字符
```

### 问题4：IP不在白名单 40164

```
解决：
1. 登录微信公众平台
2. 设置与开发 > 基本配置
3. IP白名单 > 添加服务器IP
```

---

**Happy Writing! 🚀**
