#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """配置加载器"""
    
    @staticmethod
    def load(config_path: str = None) -> Dict:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径，默认使用config/default.yaml
            
        Returns:
            配置字典
        """
        if config_path is None:
            # 获取脚本所在目录
            script_dir = Path(__file__).parent
            config_path = script_dir.parent / 'config' / 'default.yaml'
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config or {}
        except FileNotFoundError:
            # 返回默认配置
            return ConfigLoader._default_config()
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件解析错误: {e}")
    
    @staticmethod
    def _default_config() -> Dict:
        """返回默认配置"""
        return {
            'search': {
                'max_results': 10,
                'timeout': 30
            },
            'generation': {
                'default_word_count': 3000,
                'min_word_count': 2000,
                'max_word_count': 5000
            },
            'output': {
                'format': 'docx',
                'default_dir': './articles'
            },
            'styles': {
                'tech_architecture': {
                    'name': '技术架构深度分析',
                    'tone': 'professional',
                    'code_examples': True,
                    'tables': True
                }
            }
        }

class Logger:
    """日志记录器"""
    
    def __init__(self, name: str = "ContentFactory", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除已有处理器
        self.logger.handlers = []
        
        # 创建处理器
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def debug(self, message: str):
        self.logger.debug(message)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def error(self, message: str):
        self.logger.error(message)

class TextFormatter:
    """文本格式化工具"""
    
    @staticmethod
    def count_words(text: str) -> int:
        """统计字数"""
        # 中文字符计数
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        # 英文单词计数
        english_words = len(text.split())
        return chinese_chars + english_words
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """截断文本"""
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
    
    @staticmethod
    def format_code_block(code: str, language: str = "python") -> str:
        """格式化代码块"""
        return f"```{language}\n{code}\n```"

class DateTimeUtil:
    """日期时间工具"""
    
    @staticmethod
    def get_current_date() -> str:
        """获取当前日期"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_current_datetime() -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
