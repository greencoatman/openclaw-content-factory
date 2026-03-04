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
        """初始化"""
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'wechat.yaml'
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.app_id = self.config['wechat']['app_id']
        self.app_secret = self.config['wechat']['app_secret']
        self.api_base = self.config['wechat']['api_base_url']
        self.token_cache_file = self.config['wechat']['token']['cache_file']
        
        self.access_token = None
        self.token_expires_at = None
    
    def get_access_token(self) -> str:
        """
        获取 Access Token（带缓存）
        """
        # 检查缓存
        if self._load_token_from_cache():
            return self.access_token
        
        # 请求新的 token
        url = f"{self.api_base}/cgi-bin/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if 'access_token' in result:
            self.access_token = result['access_token']
            expires_in = result.get('expires_in', 7200)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            # 保存到缓存
            self._save_token_to_cache()
            
            print(f"✅ Access Token 获取成功，有效期至: {self.token_expires_at}")
            return self.access_token
        else:
            error_msg = f"获取 Access Token 失败: {result}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def _load_token_from_cache(self) -> bool:
        """从缓存加载 token"""
        if not os.path.exists(self.token_cache_file):
            return False
        
        try:
            with open(self.token_cache_file, 'r') as f:
                cache = json.load(f)
            
            expires_at = datetime.fromisoformat(cache['expires_at'])
            refresh_before = self.config['wechat']['token']['refresh_before']
            
            # 检查是否即将过期（提前刷新）
            if datetime.now() < expires_at - timedelta(seconds=refresh_before):
                self.access_token = cache['access_token']
                self.token_expires_at = expires_at
                print(f"✅ 使用缓存的 Access Token，有效期至: {self.token_expires_at}")
                return True
        except Exception as e:
            print(f"⚠️ 缓存加载失败: {e}")
        
        return False
    
    def _save_token_to_cache(self):
        """保存 token 到缓存"""
        cache = {
            'access_token': self.access_token,
            'expires_at': self.token_expires_at.isoformat()
        }
        with open(self.token_cache_file, 'w') as f:
            json.dump(cache, f)
    
    def upload_image(self, image_path: str) -> str:
        """
        上传图片到微信素材库
        
        Args:
            image_path: 图片本地路径
            
        Returns:
            图片在微信服务器的 URL
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
        
        if 'url' in result:
            print(f"✅ 图片上传成功: {result['url']}")
            return result['url']
        else:
            error_msg = f"图片上传失败: {result}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def upload_news(self, articles: List[Dict]) -> str:
        """
        上传图文素材
        
        Args:
            articles: 图文列表，每个元素包含:
                - title: 标题
                - author: 作者
                - digest: 摘要
                - content: 正文HTML
                - content_source_url: 原文链接
                - thumb_media_id: 封面图media_id
                
        Returns:
            media_id
        """
        token = self.get_access_token()
        url = f"{self.api_base}/cgi-bin/material/add_news"
        params = {"access_token": token}
        
        data = {"articles": articles}
        
        response = requests.post(url, params=params, json=data)
        result = response.json()
        
        if 'media_id' in result:
            print(f"✅ 图文素材上传成功: {result['media_id']}")
            return result['media_id']
        else:
            error_msg = f"图文素材上传失败: {result}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def add_draft(self, articles: List[Dict]) -> str:
        """
        添加草稿（订阅号专用，直接添加文章内容）
        
        Args:
            articles: 图文列表
            
        Returns:
            media_id
        """
        token = self.get_access_token()
        url = f"{self.api_base}/cgi-bin/draft/add"
        params = {"access_token": token}
        
        data = {"articles": articles}
        
        response = requests.post(url, params=params, json=data)
        result = response.json()
        
        if 'media_id' in result:
            print(f"✅ 草稿添加成功，media_id: {result['media_id']}")
            return result['media_id']
        else:
            error_msg = f"添加草稿失败: {result}"
            print(f"❌ {error_msg}")
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
        print(f"\n📝 开始发布文章: {title}")
        
        # 使用默认配置
        defaults = self.config['publish']['defaults']
        author = author or defaults['author']
        
        # 如果没有摘要，自动生成（取前100字符）
        if not digest:
            # 简单提取文本（去除HTML标签）
            import re
            text = re.sub('<[^<]+?>', '', content_html)
            digest = text[:100] + "..." if len(text) > 100 else text
        
        # 上传封面图（可选）
        thumb_media_id = ""
        if thumb_image_path and os.path.exists(thumb_image_path):
            print(f"📷 上传封面图: {thumb_image_path}")
            thumb_media_id = self._upload_permanent_image(thumb_image_path)
        else:
            # 使用默认封面图
            default_cover = Path(__file__).parent.parent / 'default_cover.jpg'
            if default_cover.exists():
                print(f"📷 使用默认封面图")
                thumb_media_id = self._upload_permanent_image(str(default_cover))
            else:
                print(f"⚠️ 未提供封面图，将创建无封面草稿（可在草稿箱中补充）")
        
        # 构建图文素材
        article = {
            "title": title,
            "author": author,
            "digest": digest,
            "content": content_html,
            "content_source_url": "",  # 原文链接，可选
            "need_open_comment": defaults['need_open_comment'],
            "only_fans_can_comment": defaults['only_fans_can_comment']
        }
        
        # 添加封面图（如果有）
        if thumb_media_id:
            article["thumb_media_id"] = thumb_media_id
        
        # 订阅号直接添加到草稿箱（不支持永久素材接口）
        print("📋 添加到草稿箱...")
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
        
        print(f"✅ 发布成功！")
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
        将 Word 文档转换为 HTML
        
        Args:
            docx_path: Word 文档路径
            
        Returns:
            HTML 内容
        """
        from docx import Document
        
        doc = Document(docx_path)
        
        html_parts = []
        style_config = self.config['content']['style']
        
        # 添加样式
        html_parts.append(f"""
        <style>
            body {{
                font-family: {style_config['font_family']};
                font-size: {style_config['font_size']};
                line-height: {style_config['line_height']};
                color: #333;
            }}
            p {{
                margin: {style_config['paragraph_margin']} 0;
            }}
            h1 {{
                font-size: {style_config['heading']['h1']['font_size']};
                color: {style_config['heading']['h1']['color']};
                margin: {style_config['heading']['h1']['margin']};
            }}
            h2 {{
                font-size: {style_config['heading']['h2']['font_size']};
                color: {style_config['heading']['h2']['color']};
                margin: {style_config['heading']['h2']['margin']};
            }}
            h3 {{
                font-size: {style_config['heading']['h3']['font_size']};
                color: {style_config['heading']['h3']['color']};
                margin: {style_config['heading']['h3']['margin']};
            }}
            pre {{
                background: {style_config['code_block']['background']};
                border: {style_config['code_block']['border']};
                padding: {style_config['code_block']['padding']};
                border-radius: {style_config['code_block']['border_radius']};
                overflow-x: auto;
            }}
        </style>
        """)
        
        # 转换段落
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            
            # 根据样式判断标题级别
            style_name = para.style.name if para.style else None
            if style_name and style_name.startswith('Heading'):
                level = style_name[-1]
                html_parts.append(f"<h{level}>{text}</h{level}>")
            else:
                html_parts.append(f"<p>{text}</p>")
        
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
    print(f"📄 转换 Word 文档: {docx_path}")
    html_content = publisher.convert_docx_to_html(docx_path)
    
    # 发布到草稿箱
    result = publisher.publish_article(
        title=title,
        content_html=html_content
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
