import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 测试转换
docx_path = './articles/2026-03-05-Kubernetes-2026新特性最佳实践.docx'
print(f'转换文档: {docx_path}')

try:
    html = publisher.convert_docx_to_html(docx_path)
    print(f'HTML长度: {len(html)}')
    print(f'\n前800字符:')
    print(html[:800])
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()
