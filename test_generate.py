import sys
sys.path.insert(0, 'scripts')
import json
from writer import ArticleWriter
from utils import ConfigLoader

# 加载配置
config = ConfigLoader.load('config/default.yaml')

# 创建 writer
writer = ArticleWriter(config)

# 生成文章
article = writer.generate(
    topic='AI大模型推理优化',
    style='tech_architecture',
    word_count=500,
    sources=[{'title': '测试', 'source': '知乎'}]
)

# 打印生成的内容
print('=== 生成的文章内容 ===')
print(f"标题: {article['title']}")
print(f"\n主题: {article['topic']}")
print(f"\n字数: {article['word_count']}")

print('\n=== 各章节内容 ===')
for section in article['sections']:
    print(f"\n--- {section['title']} ---")
    print(f"内容前100字: {section['content'][:100]}")
