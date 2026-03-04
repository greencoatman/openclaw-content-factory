#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Factory 测试用例
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

class TestConfigLoader(unittest.TestCase):
    """测试配置加载器"""
    
    def test_load_default_config(self):
        """测试加载默认配置"""
        from utils import ConfigLoader
        config = ConfigLoader.load()
        self.assertIsInstance(config, dict)
        self.assertIn('search', config)
        self.assertIn('generation', config)
        self.assertIn('output', config)
    
    def test_default_config_values(self):
        """测试默认配置值"""
        from utils import ConfigLoader
        config = ConfigLoader.load()
        self.assertEqual(config['output']['format'], 'docx')
        self.assertEqual(config['generation']['default_word_count'], 3000)


class TestHotSearcher(unittest.TestCase):
    """测试热点搜索器"""
    
    def setUp(self):
        from utils import ConfigLoader
        self.config = ConfigLoader.load()
    
    def test_search_returns_list(self):
        """测试搜索返回列表"""
        from searcher import HotSearcher
        searcher = HotSearcher(self.config)
        results = searcher.search("Kubernetes")
        self.assertIsInstance(results, list)
    
    def test_search_result_structure(self):
        """测试搜索结果结构"""
        from searcher import HotSearcher
        searcher = HotSearcher(self.config)
        results = searcher.search("微服务架构")
        if results:
            result = results[0]
            self.assertIn('source', result)
            self.assertIn('title', result)
            self.assertIn('url', result)
            self.assertIn('summary', result)
    
    def test_search_limit(self):
        """测试搜索数量限制"""
        from searcher import HotSearcher
        searcher = HotSearcher(self.config)
        results = searcher.search("AI架构", limit=3)
        self.assertLessEqual(len(results), 3)
    
    def test_get_hot_topics(self):
        """测试获取热门话题"""
        from searcher import HotSearcher
        searcher = HotSearcher(self.config)
        topics = searcher.get_hot_topics("技术架构")
        self.assertIsInstance(topics, list)
        self.assertGreater(len(topics), 0)


class TestArticleWriter(unittest.TestCase):
    """测试文章写作器"""
    
    def setUp(self):
        from utils import ConfigLoader
        self.config = ConfigLoader.load()
    
    def test_generate_article(self):
        """测试文章生成"""
        from writer import ArticleWriter
        writer = ArticleWriter(self.config)
        article = writer.generate(
            topic="Kubernetes",
            style="tech_architecture",
            word_count=3000,
            sources=[]
        )
        self.assertIsInstance(article, dict)
        self.assertIn('title', article)
        self.assertIn('sections', article)
        self.assertIn('word_count', article)
    
    def test_article_has_sections(self):
        """测试文章包含章节"""
        from writer import ArticleWriter
        writer = ArticleWriter(self.config)
        article = writer.generate(
            topic="微服务架构",
            style="tech_architecture",
            word_count=3000,
            sources=[]
        )
        self.assertGreater(len(article['sections']), 0)
    
    def test_save_to_docx(self):
        """测试保存为Word文档"""
        from writer import ArticleWriter
        writer = ArticleWriter(self.config)
        
        # 生成文章
        article = writer.generate(
            topic="测试主题",
            style="tech_architecture",
            word_count=1000,
            sources=[]
        )
        
        # 保存文档
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = writer.save_to_docx(article, tmpdir)
            self.assertTrue(os.path.exists(filepath))
            self.assertTrue(filepath.endswith('.docx'))


class TestTextFormatter(unittest.TestCase):
    """测试文本格式化工具"""
    
    def test_count_words_chinese(self):
        """测试中文字数统计"""
        from utils import TextFormatter
        text = "这是一段中文文字"
        count = TextFormatter.count_words(text)
        self.assertGreater(count, 0)
    
    def test_truncate_text(self):
        """测试文本截断"""
        from utils import TextFormatter
        text = "这是一段很长的文字" * 20
        truncated = TextFormatter.truncate_text(text, max_length=20)
        self.assertLessEqual(len(truncated), 23)  # 20 + "..."


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_full_pipeline(self):
        """测试完整流程"""
        from utils import ConfigLoader
        from searcher import HotSearcher
        from writer import ArticleWriter
        import tempfile
        
        # 加载配置
        config = ConfigLoader.load()
        
        # 搜索
        searcher = HotSearcher(config)
        sources = searcher.search("AI架构", limit=3)
        
        # 生成文章
        writer = ArticleWriter(config)
        article = writer.generate(
            topic="AI架构",
            style="tech_architecture",
            word_count=2000,
            sources=sources
        )
        
        # 保存文档
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = writer.save_to_docx(article, tmpdir)
            self.assertTrue(os.path.exists(filepath))
        
        print(f"\n✅ 集成测试通过！文章《{article['title']}》生成成功，共{article['word_count']}字")


if __name__ == '__main__':
    # 运行所有测试
    unittest.main(verbosity=2)
