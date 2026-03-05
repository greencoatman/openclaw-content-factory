import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 测试不同长度的标题
test_titles = [
    "AI优化",           # 4字符
    "AI大模型优化",      # 6字符
    "AI大模型推理优化",   # 8字符
    "AI大模型推理优化深度", # 10字符
]

for title in test_titles:
    try:
        result = publisher.publish_article(
            title=title,
            content_html="<p>测试</p>"
        )
        print(f'✅ "{title}" ({len(title)}字符) - 成功')
    except Exception as e:
        print(f'❌ "{title}" ({len(title)}字符) - 失败: {str(e)[:50]}')
