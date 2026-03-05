import sys
sys.path.insert(0, 'scripts')
from writer import ArticleWriter
from wechat_publisher import WeChatPublisher
from utils import ConfigLoader

# 加载配置
config = ConfigLoader.load('config/default.yaml')

# 1. 生成文章
print('=== 1. 生成文章 ===')
writer = ArticleWriter(config)
article = writer.generate(
    topic='AI大模型推理优化',
    style='tech_architecture',
    word_count=500,
    sources=[{'title': '测试', 'source': '知乎'}]
)
print(f"标题: {article['title']}")
print(f"引言前50字: {article['sections'][0]['content'][:50]}")

# 2. 保存为 Word
print('\n=== 2. 保存 Word ===')
filename = writer.save_to_docx(article, './articles')
print(f"保存路径: {filename}")

# 3. 转换为 HTML
print('\n=== 3. 转换 HTML ===')
publisher = WeChatPublisher()
html_content = publisher.convert_docx_to_html(filename)
print(f"HTML 长度: {len(html_content)}")
print(f"HTML 内容片段:")
# 找到第一个包含中文的段落
for line in html_content.split('\n'):
    if '<p>' in line and 'AI' in line and '大' in line:
        print(f"  {line}")
        break

print('\n=== 4. 准备发送到微信的数据 ===')
article_data = {
    "title": article['title'][:12],  # 截断标题
    "author": "CC",
    "digest": "测试摘要",
    "content": html_content,
}
print(f"标题: {article_data['title']}")
print(f"内容前200字符: {article_data['content'][:200]}")
