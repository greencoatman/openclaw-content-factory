import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 测试13字符标题
title = "AI大模型推理优化深度分析"
print(f'测试标题: "{title}" ({len(title)}字符)')

try:
    result = publisher.publish_article(
        title=title,
        content_html="<p>测试内容</p>"
    )
    print(f'✅ 成功! Media ID: {result["data"]["media_id"]}')
except Exception as e:
    print(f'❌ 失败: {e}')
