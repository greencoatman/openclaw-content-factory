#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号发布模块
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class WeChatPublisher:
    """微信公众号发布器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化发布器
        
        Args:
            config_path: 配置文件路径，默认使用 config/wechat.yaml
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'wechat.yaml'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        wechat_config = self.config.get('wechat', {})
        self.api_base = wechat_config.get('api_base_url', 'https://api.weixin.qq.com')
        self.app_id = wechat_config.get('app_id', '')
        self.app_secret = wechat_config.get('app_secret', '')
        
        # Token缓存
        self._token_cache = None
        self._token_expires = None
    
    def get_access_token(self) -> str:
        """
        获取Access Token（带缓存）
        
        Returns:
            access_token
        """
        # 检查缓存是否有效
        if self._token_cache and self._token_expires and datetime.now() < self._token_expires:
            return self._token_cache
        
        # 获取新Token
        url = f"{self.api_base}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        response = requests.get(url, params=params, timeout=30)
        result = response.json()
        
        if 'access_token' in result:
            self._token_cache = result['access_token']
            # 提前5分钟过期
            expires_in = result.get('expires_in', 7200) - 300
            self._token_expires = datetime.now() + timedelta(seconds=expires_in)
            return self._token_cache
        else:
            raise Exception(f"获取Access Token失败: {result}")
    
    def add_draft(self, articles: List[Dict]) -> str:
        """
        添加草稿（订阅号专用）
        
        Args:
            articles: 图文列表
            
        Returns:
            media_id
        """
        token = self.get_access_token()
        url = f"{self.api_base}/cgi-bin/draft/add"
        params = {"access_token": token}
        
        data = {"articles": articles}
        
        # 手动编码 JSON，确保中文正确传输
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        response = requests.post(url, params=params, data=json_data, headers=headers)
        result = response.json()
        
        if 'media_id' in result:
            return result['media_id']
        else:
            error_msg = f"添加草稿失败: {result}"
            print(error_msg)
            raise Exception(error_msg)
    
    def publish_article(self, title: str, content_html: str, 
                       author: str = None, digest: str = None,
                       thumb_image_path: str = None) -> Dict:
        """
        发布文章到草稿箱
        
        Args:
            title: 文章标题
            content_html: 文章HTML内容
            author: 作者
            digest: 摘要
            thumb_image_path: 封面图路径
            
        Returns:
            发布结果
        """
        print(f"\n开始发布文章: {title}")
        
        # 截断标题（微信订阅号限制12字符）
        if len(title) > 12:
            title = title[:10] + ".."
            print(f"标题过长，已截断为: {title}")
        
        # 使用默认配置
        defaults = self.config['publish']['defaults']
        author = author or defaults['author']
        
        # 截断作者（微信限制8字符）
        if len(author) > 8:
            author = author[:8]
            print(f"作者名称过长，已截断为: {author}")
        
        # 如果没有摘要，自动生成（微信限制很严格）
        if not digest:
            import re
            # 先移除 style 标签及其内容
            text = re.sub(r'<style[^>]*>.*?</style>', '', content_html, flags=re.DOTALL | re.IGNORECASE)
            # 移除其他HTML标签
            text = re.sub(r'<[^>]+>', '', text)
            # 移除多余空白
            text = re.sub(r'\s+', ' ', text).strip()
            # 极短摘要：取前20字符
            digest = text[:20] + "..." if len(text) > 20 else text
        
        # 上传封面图（可选）
        thumb_media_id = ""
        if thumb_image_path and os.path.exists(thumb_image_path):
            print(f"上传封面图: {thumb_image_path}")
            thumb_media_id = self._upload_permanent_image(thumb_image_path)
        else:
            # 使用默认封面图
            default_cover = Path(__file__).parent.parent / 'default_cover.jpg'
            if default_cover.exists():
                print(f"使用默认封面图")
                thumb_media_id = self._upload_permanent_image(str(default_cover))
            else:
                print(f"未提供封面图，将创建无封面草稿")
        
        # 构建图文素材
        article = {
            "title": title,
            "author": author,
            "digest": digest,
            "content": content_html,
            "content_source_url": "",
            "need_open_comment": defaults['need_open_comment'],
            "only_fans_can_comment": defaults['only_fans_can_comment']
        }
        
        # 添加封面图（如果有）
        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id
        
        # 订阅号直接添加到草稿箱
        print("添加到草稿箱...")
        print(f"   标题: '{title}' (长度: {len(title)})")
        print(f"   作者: '{author}' (长度: {len(author)})")
        print(f"   摘要: '{digest[:20]}...' (长度: {len(digest)})")
        print(f"   内容长度: {len(content_html)} 字符")
        
        draft_id = self.add_draft([article])
        
        result = {
            "status": "success",
            "message": "文章已发布到草稿箱",
            "data": {
                "title": title,
                "media_id": draft_id,
                "draft_id": draft_id,
                "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        print(f"发布成功！")
        print(f"   - Draft Media ID: {draft_id}")
        
        return result
    
    def _upload_permanent_image(self, image_path: str) -> str:
        """
        上传永久图片素材（用于封面）
        
        Returns:
            media_id
        """
        token = self.get_access_token()
        url = f"{self.api_base}/cgi-bin/material/add_material"
        params = {
            "access_token": token,
            "type": "image"
        }
        
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, params=params, files=files)
        
        result = response.json()
        
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"上传永久图片失败: {result}")
    
    def convert_docx_to_html(self, docx_path: str) -> str:
        """
        将 Word 文档转换为 HTML - 自然语言版
        """
        from docx import Document
        
        doc = Document(docx_path)
        
        html_parts = []
        style_config = self.config['content']['style']
        
        # 微信支持的样式（内联）
        body_style = f"font-family: {style_config['font_family']}; font-size: {style_config['font_size']}; line-height: {style_config['line_height']}; color: #333;"
        p_style = f"margin: 1em 0; font-size: {style_config['font_size']}; line-height: 1.8; text-align: justify;"
        h1_style = f"font-size: 22px; color: #1a1a1a; margin: 1.5em 0 0.8em; font-weight: bold;"
        h2_style = f"font-size: 18px; color: #2c3e50; margin: 1.2em 0 0.6em; font-weight: bold;"
        
        # 图片占位样式
        img_placeholder_style = "margin: 15px 0; padding: 30px 20px; background: #f8f9fa; border: 1px dashed #ccc; border-radius: 4px; text-align: center; color: #999; font-size: 14px;"
        
        # 开始 body
        html_parts.append(f'<section style="{body_style}">')
        
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            style_name = para.style.name if para.style else None
            
            # 一级标题（文章主标题）
            if style_name and style_name.startswith('Title'):
                html_parts.append(f'<h1 style="{h1_style} text-align: center;">{text}</h1>')
            
            # 二级标题（章节标题）
            elif style_name and style_name.startswith('Heading 1'):
                html_parts.append(f'<h2 style="{h1_style}">{text}</h2>')
            
            # 三级标题（小节标题）
            elif style_name and style_name.startswith('Heading 2'):
                html_parts.append(f'<h3 style="{h2_style}">{text}</h3>')
            
            # 图片占位符 [配图：描述]
            elif text.startswith('[配图：') and text.endswith(']'):
                description = text[4:-1]  # 提取描述
                html_parts.append(f'<div style="{img_placeholder_style}">{description}</div>')
            
            # 分隔线
            elif text.startswith('_' * 10) or text.startswith('—' * 5):
                html_parts.append('<hr style="border: none; border-top: 1px solid #e8e8e8; margin: 20px 0;"/>')
            
            # 元信息（居中、灰色）
            elif ' | ' in text and ('技术架构' in text or any(c.isdigit() for c in text)):
                html_parts.append(f'<p style="{p_style} text-align: center; color: #999; font-size: 13px;">{text}</p>')
            
            # 钩子（蓝色、居中）
            elif text.startswith(('最近', '在架构', '去年', '如果你')) and len(text) < 100:
                html_parts.append(f'<p style="{p_style} text-align: center; color: #1890ff; font-size: 15px;">{text}</p>')
            
            # 普通段落
            else:
                # 检查是否包含需要强调的内容
                if any(keyword in text for keyword in ['第一', '第二', '第三', '第四', '第五', '总结', '建议']):
                    # 开头加粗
                    html_parts.append(f'<p style="{p_style}"><strong>{text[:4]}</strong>{text[4:]}</p>')
                else:
                    html_parts.append(f'<p style="{p_style}">{text}</p>')
        
        # 结束 body
        html_parts.append('</section>')
        
        return '\n'.join(html_parts)


def main():
    """测试入口"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python wechat_publisher.py <docx_path> <title>")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    title = sys.argv[2]
    
    publisher = WeChatPublisher()
    
    # 转换 Word 为 HTML
    print(f"转换 Word 文档: {docx_path}")
    html_content = publisher.convert_docx_to_html(docx_path)
    
    # 发布到草稿箱
    result = publisher.publish_article(
        title=title,
        content_html=html_content
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
