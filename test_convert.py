import sys
sys.path.insert(0, 'scripts')
from wechat_publisher import WeChatPublisher

publisher = WeChatPublisher()

# 测试转换
docx_path = './articles/2026-03-05-AI大模型推理优化深度分析.docx'
print(f'📄 转换文档: {docx_path}')

try:
    html_content = publisher.convert_docx_to_html(docx_path)
    print(f'✅ HTML 内容长度: {len(html_content)}')
    print(f'\n📝 前500字符:')
    print(html_content[:500])
    print(f'\n📝 包含中文段落示例:')
    # 找出包含中文的行
    for line in html_content.split('\n'):
        if '<p>' in line and 'AI' in line:
            print(line)
            break
except Exception as e:
    print(f'❌ 错误: {e}')
