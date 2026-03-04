#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Content Factory - 智能内容生成助手
主入口文件
"""

import json
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from searcher import HotSearcher
from writer import ArticleWriter
from utils import ConfigLoader, Logger

def main():
    """主入口函数"""
    # 初始化日志
    logger = Logger()
    logger.info("Content Factory 启动")
    
    try:
        # 解析输入参数
        args = parse_input()
        logger.info(f"输入参数: {args}")
        
        # 加载配置
        config = ConfigLoader.load()
        logger.info("配置加载成功")
        
        # 确定文章主题
        if args.get('mode') == 'auto':
            # 自动搜索热点
            logger.info("开始自动搜索热点...")
            searcher = HotSearcher(config)
            hot_topics = searcher.search(args.get('domain', '技术架构'))
            topic = hot_topics[0] if hot_topics else '技术架构最新趋势'
            logger.info(f"自动选择热点: {topic}")
        else:
            topic = args.get('topic', '技术架构')
            logger.info(f"使用指定主题: {topic}")
        
        # 确定文章风格
        style = args.get('style', config['generation']['default_style'])
        logger.info(f"文章风格: {style}")
        
        # 确定字数
        word_count = args.get('word_count', config['generation']['default_word_count'])
        logger.info(f"目标字数: {word_count}")
        
        # 搜索相关资料
        logger.info("开始搜索相关资料...")
        searcher = HotSearcher(config)
        search_results = searcher.search(topic, limit=5)
        logger.info(f"搜索到 {len(search_results)} 条相关资料")
        
        # 生成文章
        logger.info("开始生成文章...")
        writer = ArticleWriter(config)
        article_data = writer.generate(
            topic=topic,
            style=style,
            word_count=word_count,
            sources=search_results
        )
        logger.info("文章生成完成")
        
        # 保存为Word文档
        output_path = args.get('output_dir', config['output']['default_dir'])
        filename = writer.save_to_docx(article_data, output_path)
        logger.info(f"文档已保存: {filename}")
        
        # 返回结果
        result = {
            "status": "success",
            "message": "文章生成成功",
            "data": {
                "filename": os.path.basename(filename),
                "path": filename,
                "topic": topic,
                "style": style,
                "word_count": article_data.get('word_count', 0),
                "sources": [s['source'] for s in search_results[:3]],
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        
        print(json.dumps(result, ensure_ascii=False))
        logger.info("Content Factory 执行完成")
        
    except Exception as e:
        logger.error(f"执行失败: {str(e)}")
        error_result = {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(json.dumps(error_result, ensure_ascii=False))
        sys.exit(1)

def parse_input():
    """解析输入参数"""
    # 尝试从命令行参数读取
    parser = argparse.ArgumentParser(description='Content Factory - 智能内容生成')
    parser.add_argument('--topic', '-t', help='文章主题')
    parser.add_argument('--style', '-s', help='文章风格')
    parser.add_argument('--word-count', '-w', type=int, help='目标字数')
    parser.add_argument('--output-dir', '-o', help='输出目录')
    parser.add_argument('--mode', '-m', choices=['auto', 'manual'], default='manual', help='生成模式')
    parser.add_argument('--domain', '-d', help='自动搜索时的领域')
    
    args, unknown = parser.parse_known_args()
    
    # 尝试从stdin读取JSON输入
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read()
            if stdin_data.strip():
                json_input = json.loads(stdin_data)
                # 合并stdin数据和命令行参数（命令行优先）
                result = json_input.copy()
                for key, value in vars(args).items():
                    if value is not None:
                        result[key] = value
                return result
        except json.JSONDecodeError:
            pass
    
    # 返回命令行参数
    return {k: v for k, v in vars(args).items() if v is not None}

if __name__ == "__main__":
    main()
