#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试微信公众号发布功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wechat_publisher import WeChatPublisher

def test_get_access_token():
    """测试获取 Access Token"""
    print("=" * 60)
    print("测试1: 获取 Access Token")
    print("=" * 60)
    
    publisher = WeChatPublisher()
    token = publisher.get_access_token()
    
    print(f"\n✅ Access Token: {token[:20]}...")
    print(f"✅ 过期时间: {publisher.token_expires_at}")
    
    return publisher

def test_convert_docx():
    """测试 Word 转 HTML"""
    print("\n" + "=" * 60)
    print("测试2: Word 转 HTML")
    print("=" * 60)
    
    # 查找最近生成的 Word 文档
    articles_dir = "../articles"
    if not os.path.exists(articles_dir):
        print("⚠️ 未找到 articles 目录，跳过此测试")
        return None
    
    docx_files = [f for f in os.listdir(articles_dir) if f.endswith('.docx') and not f.startswith('~$')]
    if not docx_files:
        print("⚠️ 未找到 Word 文档，跳过此测试")
        return None
    
    # 使用最新的文档
    latest_file = sorted(docx_files)[-1]
    docx_path = os.path.join(articles_dir, latest_file)
    
    print(f"\n📄 转换文档: {latest_file}")
    
    publisher = WeChatPublisher()
    html_content = publisher.convert_docx_to_html(docx_path)
    
    print(f"✅ HTML 长度: {len(html_content)} 字符")
    print(f"✅ 预览前500字符:\n{html_content[:500]}...")
    
    return docx_path, html_content

def test_publish_article():
    """测试发布文章到草稿箱"""
    print("\n" + "=" * 60)
    print("测试3: 发布文章到草稿箱")
    print("=" * 60)
    
    # 先转换文档
    result = test_convert_docx()
    if not result:
        print("⚠️ 无法进行发布测试")
        return
    
    docx_path, html_content = result
    
    publisher = WeChatPublisher()
    
    # 提取标题（从文件名）
    filename = os.path.basename(docx_path)
    title = filename.replace('.docx', '').split('-', 1)[-1] if '-' in filename else filename.replace('.docx', '')
    
    print(f"\n📝 发布文章: {title}")
    
    try:
        publish_result = publisher.publish_article(
            title=title,
            content_html=html_content
        )
        
        print(f"\n✅ 发布成功!")
        print(f"   Media ID: {publish_result['data']['media_id']}")
        print(f"   Draft ID: {publish_result['data']['draft_id']}")
        print(f"\n🎉 请前往微信公众号后台查看草稿箱！")
        
    except Exception as e:
        print(f"\n❌ 发布失败: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """运行所有测试"""
    print("\n🚀 开始测试微信公众号发布功能\n")
    
    try:
        # 测试1: 获取 Access Token
        test_get_access_token()
        
        # 测试2: Word 转 HTML
        test_convert_docx()
        
        # 测试3: 发布文章
        choice = input("\n是否继续测试发布到草稿箱？(y/n): ")
        if choice.lower() == 'y':
            test_publish_article()
        else:
            print("\n⏭️ 跳过发布测试")
        
        print("\n✅ 测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
