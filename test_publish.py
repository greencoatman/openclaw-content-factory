import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

html = """
<style>
body { font-family: Microsoft YaHei; font-size: 16px; }
</style>
<h1>AI大模型推理优化</h1>
<p>这是一篇测试文章。</p>
"""

try:
    result = publisher.publish_article(
        title="AI大模型推理优化",
        content_html=html
    )
    print(f'成功!')
    print(f'  Media ID: {result["data"]["media_id"]}')
except Exception as e:
    print(f'失败: {e}')
