#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
写作模块 - 文章生成与Word文档输出
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Any
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

class ArticleWriter:
    """文章写作器"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.styles = config.get('styles', {})
        self.output_config = config.get('output', {})
    
    def generate(self, topic: str, style: str, word_count: int, sources: List[Dict]) -> Dict:
        """
        生成文章
        
        Args:
            topic: 文章主题
            style: 文章风格
            word_count: 目标字数
            sources: 参考资料
            
        Returns:
            文章数据字典
        """
        style_config = self.styles.get(style, self.styles.get('tech_architecture', {}))
        structure = style_config.get('structure', [])
        
        article = {
            "title": f"{topic}深度分析",
            "topic": topic,
            "style": style,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sections": []
        }
        
        # 根据结构生成各部分内容
        total_words = 0
        target_per_section = word_count // len(structure)
        
        for section_config in structure:
            section_name = section_config.get('name', '')
            section_title = section_config.get('title', '')
            section_words = section_config.get('word_count', target_per_section)
            
            content = self._generate_section_content(
                section_name=section_name,
                section_title=section_title,
                topic=topic,
                target_words=section_words,
                sources=sources
            )
            
            article['sections'].append({
                "name": section_name,
                "title": section_title,
                "content": content,
                "word_count": len(content)
            })
            
            total_words += len(content)
        
        article['word_count'] = total_words
        article['sources'] = sources
        
        return article
    
    def _generate_section_content(self, section_name: str, section_title: str, 
                                   topic: str, target_words: int, sources: List[Dict]) -> str:
        """生成章节内容"""
        
        if section_name == 'introduction':
            return self._generate_introduction(topic, target_words, sources)
        elif section_name == 'principle':
            return self._generate_principle(topic, target_words)
        elif section_name == 'practice':
            return self._generate_practice(topic, target_words)
        elif section_name == 'comparison':
            return self._generate_comparison(topic, target_words)
        elif section_name == 'conclusion':
            return self._generate_conclusion(topic, target_words)
        else:
            return self._generate_generic_content(section_title, topic, target_words)
    
    def _generate_introduction(self, topic: str, target_words: int, sources: List[Dict]) -> str:
        """生成引言部分"""
        paragraphs = []
        
        # 背景引入
        paragraphs.append(
            f"2026年，{topic}正在成为技术圈最热门的话题之一。" +
            f"随着数字化转型的深入，越来越多的企业开始关注这一领域。" +
            f"本文将深入剖析{topic}的技术原理、实战案例以及未来发展趋势。"
        )
        
        # 问题阐述
        paragraphs.append(
            f"在实际落地过程中，{topic}面临着诸多挑战：" +
            f"架构设计复杂、成本控制困难、团队协作效率低等问题频发。" +
            f"如何在保证技术先进性的同时，实现业务价值的最大化，成为每个架构师需要思考的问题。"
        )
        
        # 文章价值
        paragraphs.append(
            f"本文将从以下几个维度展开深度分析：首先介绍{topic}的核心技术原理；" +
            f"然后分享大厂实战案例；接着对比不同技术方案的优劣；" +
            f"最后给出架构师行动指南。无论你是初入职场的新手，还是经验丰富的资深架构师，都能从本文中获得有价值的洞察。"
        )
        
        return '\n\n'.join(paragraphs)
    
    def _generate_principle(self, topic: str, target_words: int) -> str:
        """生成技术原理部分"""
        paragraphs = []
        
        paragraphs.append(
            f"{topic}的核心技术架构可以概括为三层：基础设施层、服务编排层和应用层。" +
            f"每一层都有其独特的设计哲学和技术挑战。"
        )
        
        paragraphs.append(
            f"在基础设施层，{topic}采用了分布式架构设计，通过多节点部署实现高可用性。" +
            f"关键技术包括容器化部署、服务网格、以及自动化运维体系。" +
            f"这些技术的组合，使得系统能够支撑百万级并发请求。"
        )
        
        paragraphs.append(
            f"服务编排层是{topic}的核心所在。通过引入微服务架构，系统被拆分为多个独立的服务单元。" +
            f"每个服务单元负责特定的业务功能，通过标准化接口进行通信。" +
            f"这种设计不仅提高了开发效率，也为后续的功能扩展打下了基础。"
        )
        
        paragraphs.append(
            f"应用层直接面向终端用户，提供了丰富的功能接口。" +
            f"通过前后端分离架构，应用层能够灵活响应业务需求的变化。" +
            f"同时，通过引入缓存、CDN等优化手段，用户体验得到了显著提升。"
        )
        
        return '\n\n'.join(paragraphs)
    
    def _generate_practice(self, topic: str, target_words: int) -> str:
        """生成实战案例部分"""
        paragraphs = []
        
        paragraphs.append(
            f"某互联网大厂在2025年初开始实践{topic}，经过一年的探索，积累了宝贵的经验。" +
            f"在架构设计阶段，团队面临的最大挑战是如何在有限资源下实现高可用性。"
        )
        
        paragraphs.append(
            f"经过多轮技术评审，团队最终选择了基于Kubernetes的容器化部署方案。" +
            f"通过引入Istio服务网格，实现了服务间的流量管理和安全通信。" +
            f"同时，通过GitOps实践，部署效率提升了300%。"
        )
        
        paragraphs.append(
            f"在实施过程中，团队也踩了不少坑。比如在初期，由于缺乏经验，" +
            f"微服务拆分粒度过细，导致系统复杂度急剧上升。" +
            f"后来通过引入领域驱动设计（DDD）方法论，重新梳理了服务边界，才解决了这个问题。"
        )
        
        paragraphs.append(
            f"经过一年的优化，该系统已经能够稳定支撑日均千万级请求。" +
            f"系统可用性从99.9%提升到99.99%，平均响应时间从200ms降低到50ms。" +
            f"更重要的是，开发效率大幅提升，新功能上线周期从两周缩短到三天。"
        )
        
        return '\n\n'.join(paragraphs)
    
    def _generate_comparison(self, topic: str, target_words: int) -> str:
        """生成对比分析部分"""
        paragraphs = []
        
        paragraphs.append(
            f"在选择{topic}技术方案时，企业通常面临多种选择。" +
            f"下表对比了几种主流方案的优劣："
        )
        
        paragraphs.append(
            f"方案A采用传统的单体架构，开发简单，但在扩展性和维护性方面存在明显短板。" +
            f"适合小型团队或初创公司快速验证产品。"
        )
        
        paragraphs.append(
            f"方案B采用微服务架构，服务独立部署，扩展性好。" +
            f"但运维复杂度高，需要配套完善的DevOps体系。" +
            f"适合中大型团队，有一定技术积累的公司。"
        )
        
        paragraphs.append(
            f"方案C采用Serverless架构，按需付费，运维成本低。" +
            f"但存在冷启动延迟和供应商锁定风险。" +
            f"适合事件驱动型应用，流量波动大的场景。"
        )
        
        paragraphs.append(
            f"综上所述，技术选型需要综合考虑团队规模、业务特点、成本预算等因素。" +
            f"没有最好的方案，只有最适合的方案。"
        )
        
        return '\n\n'.join(paragraphs)
    
    def _generate_conclusion(self, topic: str, target_words: int) -> str:
        """生成总结部分"""
        paragraphs = []
        
        paragraphs.append(
            f"{topic}代表了技术架构演进的重要方向。" +
            f"通过本文的分析，我们可以看到，成功的架构设计需要在技术先进性和工程可行性之间找到平衡。"
        )
        
        paragraphs.append(
            f"展望未来，随着云原生技术的成熟和AI能力的增强，{topic}将迎来新的发展机遇。" +
            f"建议架构师持续关注以下方向：一是深入理解云原生架构设计模式；" +
            f"二是掌握AI辅助开发工具；三是培养系统性思维，从全局视角审视架构设计。"
        )
        
        paragraphs.append(
            f"技术永远在进步，但架构设计的本质始终不变：解决问题，创造价值。" +
            f"希望本文能为你的技术之路提供一些参考。"
        )
        
        return '\n\n'.join(paragraphs)
    
    def _generate_generic_content(self, title: str, topic: str, target_words: int) -> str:
        """生成通用内容"""
        return f"{title}部分的内容。关于{topic}的详细分析..."
    
    def save_to_docx(self, article: Dict, output_dir: str) -> str:
        """
        保存为Word文档
        
        Args:
            article: 文章数据
            output_dir: 输出目录
            
        Returns:
            文件路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_topic = article['topic'].replace(' ', '-').replace('/', '-')
        filename = f"{date_str}-{safe_topic}深度分析.docx"
        filepath = os.path.join(output_dir, filename)
        
        # 创建Word文档
        doc = Document()
        
        # 设置中文字体
        doc.styles['Normal'].font.name = 'Microsoft YaHei'
        doc.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
        
        # 添加标题
        title = doc.add_heading(article['title'], level=0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加元信息
        meta = doc.add_paragraph()
        meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
        meta_run = meta.add_run(f"深度技术架构分析 | {article['generated_at']}")
        meta_run.font.size = Pt(10)
        meta_run.font.color.rgb = RGBColor(128, 128, 128)
        
        # 添加分隔线
        doc.add_paragraph('_' * 50)
        
        # 添加各章节
        for section in article['sections']:
            # 章节标题
            heading = doc.add_heading(section['title'], level=1)
            
            # 章节内容
            paragraphs = section['content'].split('\n\n')
            for para_text in paragraphs:
                if para_text.strip():
                    para = doc.add_paragraph(para_text.strip())
                    para.paragraph_format.line_spacing = 1.5
                    para.paragraph_format.first_line_indent = Inches(0.3)
        
        # 添加参考资料
        if article.get('sources'):
            doc.add_heading('参考资料', level=1)
            for idx, source in enumerate(article['sources'][:5], 1):
                para = doc.add_paragraph()
                para.add_run(f"{idx}. ").bold = True
                para.add_run(f"{source.get('title', '')} - {source.get('source', '')}")
        
        # 添加页脚
        doc.add_paragraph()
        footer = doc.add_paragraph()
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer_run = footer.add_run("—— 技术架构观察 | 每日分享深度技术文章 ——")
        footer_run.font.size = Pt(9)
        footer_run.font.color.rgb = RGBColor(128, 128, 128)
        
        # 保存文档
        doc.save(filepath)
        
        return filepath
