import sys
sys.path.insert(0, 'scripts')
from writer import ArticleWriter
from utils import ConfigLoader
import json

config = ConfigLoader.load()
writer = ArticleWriter(config)

article = writer.generate(
    topic='AI大模型推理优化',
    style='tech_architecture',
    word_count=1000,
    sources=[]
)

print('文章数据:')
print(json.dumps({
    'title': article['title'],
    'title_len': len(article['title']),
    'topic': article['topic'],
    'style': article['style']
}, ensure_ascii=False, indent=2))
