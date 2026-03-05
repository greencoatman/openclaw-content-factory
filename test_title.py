import sys
sys.path.insert(0, 'scripts')
from writer import ArticleWriter
from utils import ConfigLoader

config = ConfigLoader.load()
writer = ArticleWriter(config)

article = writer.generate(
    topic='AI大模型推理优化',
    style='tech_architecture',
    word_count=1000,
    sources=[]
)

print('标题:', article['title'])
print('标题长度:', len(article['title']), '字符')
