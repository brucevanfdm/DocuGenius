#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示新的图片提取和markdown生成功能
"""

import sys
import json
from pathlib import Path

# Add the bin/win32 directory to the path
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

from image_extractor import ImageExtractor, extract_images_from_document

def demonstrate_new_features():
    """演示新的功能"""
    print("DocuGenius 图片提取器 - 新功能演示")
    print("=" * 60)
    
    # 模拟提取的图片数据
    mock_images = [
        {
            'filename': 'page_1_img_1.png',
            'relative_path': 'images/test-document/page_1_img_1.png',
            'page': 1,
            'source': 'PDF',
            'width': 800,
            'height': 600
        },
        {
            'filename': 'page_1_img_2.jpg',
            'relative_path': 'images/test-document/page_1_img_2.jpg',
            'page': 1,
            'source': 'PDF',
            'width': 640,
            'height': 480
        },
        {
            'filename': 'page_3_img_1.png',
            'relative_path': 'images/test-document/page_3_img_1.png',
            'page': 3,
            'source': 'PDF',
            'width': 1024,
            'height': 768
        }
    ]
    
    extractor = ImageExtractor("test-document.txt")
    
    print("\n📝 不同的Markdown生成模式:")
    print("-" * 50)
    
    # 1. Simple模式
    print("\n1. Simple模式 (推荐用于手动插入):")
    simple_md = extractor.generate_markdown_references(mock_images, "simple")
    print(simple_md)
    
    # 2. Grouped模式
    print("\n2. Grouped模式 (按页面分组):")
    grouped_md = extractor.generate_markdown_references(mock_images, "grouped")
    print(grouped_md)
    
    # 3. Inline模式 (传统模式)
    print("\n3. Inline模式 (传统的'Extracted Images'部分):")
    inline_md = extractor.generate_markdown_references(mock_images, "inline")
    print(inline_md)
    
    print("\n🔧 辅助功能:")
    print("-" * 30)
    
    # 按页面获取图片引用
    print("\n按页面获取图片引用:")
    page_refs = extractor.get_image_references_by_page(mock_images)
    for page, refs in page_refs.items():
        print(f"  第{page}页: {len(refs)}张图片")
        for ref in refs:
            print(f"    {ref}")
    
    # 简单图片列表
    print("\n简单图片列表:")
    simple_list = extractor.get_simple_image_list(mock_images)
    for i, ref in enumerate(simple_list, 1):
        print(f"  {i}. {ref}")

def demonstrate_usage_scenarios():
    """演示使用场景"""
    print("\n\n💡 使用场景建议:")
    print("=" * 60)
    
    print("\n🎯 场景1: 手动控制图片位置")
    print("   使用 'simple' 模式，获取图片引用列表")
    print("   然后手动将图片插入到文档的合适位置")
    print("   示例:")
    print("   ```")
    print("   # 第一章")
    print("   这里是文本内容...")
    print("   ")
    print("   ![Image from page 1](images/document/page_1_img_1.png)")
    print("   ")
    print("   继续文本内容...")
    print("   ```")
    
    print("\n🎯 场景2: 按页面组织图片")
    print("   使用 'grouped' 模式，图片按页面分组显示")
    print("   适合需要保持原文档结构的情况")
    
    print("\n🎯 场景3: 传统方式")
    print("   使用 'inline' 模式，所有图片放在文档末尾")
    print("   适合图片作为附录或参考资料的情况")
    
    print("\n🔧 编程接口使用:")
    print("   ```python")
    print("   result = extract_images_from_document(")
    print("       'document.pdf',")
    print("       markdown_mode='simple'  # 或 'grouped', 'inline'")
    print("   )")
    print("   ")
    print("   # 获取不同格式的输出")
    print("   simple_refs = result['simple_image_list']")
    print("   page_refs = result['image_references_by_page']")
    print("   traditional = result['markdown_references']")
    print("   ```")

if __name__ == "__main__":
    demonstrate_new_features()
    demonstrate_usage_scenarios()
