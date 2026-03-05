import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 极简测试
html = "<p>测试内容</p>"

try:
    result = publisher.publish_article(
        title="AI优化",
        content_html=html
    )
    print(f'成功! Media ID: {result["data"]["media_id"]}')
except Exception as e:
    print(f'失败: {e}')
