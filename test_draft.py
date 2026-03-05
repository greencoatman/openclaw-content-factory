import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 测试极简内容
test_article = {
    "title": "测试文章",
    "author": "测试",
    "digest": "测试摘要",
    "content": "<p>测试内容</p>",
    "content_source_url": "",
    "need_open_comment": 0,
    "only_fans_can_comment": 0
}

print('发送测试文章:')
print(f'  标题: {test_article["title"]} (长度: {len(test_article["title"])})')
print(f'  作者: {test_article["author"]} (长度: {len(test_article["author"])})')
print(f'  摘要: {test_article["digest"]} (长度: {len(test_article["digest"])})')

try:
    result = publisher.add_draft([test_article])
    print(f'成功! Media ID: {result}')
except Exception as e:
    print(f'失败: {e}')
