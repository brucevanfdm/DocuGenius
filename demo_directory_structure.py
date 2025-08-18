#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示新的目录结构和相对路径计算
"""

import sys
from pathlib import Path

# Add the bin/win32 directory to the path
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

from image_extractor import ImageExtractor

def demonstrate_directory_structure():
    """演示新的目录结构"""
    print("DocuGenius 图片提取器 - 新目录结构演示")
    print("=" * 60)
    
    print("\n📁 新的目录结构:")
    print("项目根目录/")
    print("├── DocuGenius/                    # markdown文件存放目录")
    print("│   ├── document1.md")
    print("│   ├── document2.md")
    print("│   └── images/                    # 图片存放目录")
    print("│       ├── document1/")
    print("│       │   ├── image1.png")
    print("│       │   └── image2.jpg")
    print("│       └── document2/")
    print("│           ├── image1.png")
    print("│           └── image2.jpg")
    print("├── test-document.txt              # 原始文档")
    print("└── other-files...")
    
    print("\n🔗 相对路径示例:")
    
    # 演示默认情况
    print("\n1. 默认情况 (markdown在DocuGenius目录，图片在DocuGenius/images目录):")
    extractor1 = ImageExtractor("test-document.txt")
    print(f"   - 文档路径: {extractor1.document_path}")
    print(f"   - 图片输出目录: {extractor1.output_dir}")
    print(f"   - Markdown目录: {extractor1.markdown_dir}")
    
    # 模拟图片路径
    sample_image_path = extractor1.output_dir / "image1.png"
    relative_path = extractor1._calculate_relative_path(sample_image_path)
    print(f"   - 图片绝对路径: {sample_image_path}")
    print(f"   - Markdown中的相对路径: {relative_path}")
    print(f"   - Markdown引用: ![Image](images/test-document/image1.png)")
    
    print("\n2. 自定义markdown目录的情况:")
    extractor2 = ImageExtractor("test-document.txt", markdown_dir="custom_docs")
    sample_image_path2 = extractor2.output_dir / "image1.png"
    relative_path2 = extractor2._calculate_relative_path(sample_image_path2)
    print(f"   - Markdown目录: {extractor2.markdown_dir}")
    print(f"   - 图片输出目录: {extractor2.output_dir}")
    print(f"   - Markdown中的相对路径: {relative_path2}")
    
    print("\n✅ 优势:")
    print("   • Markdown文件和图片都在DocuGenius目录下，便于管理")
    print("   • 相对路径简洁: images/document_name/image.png")
    print("   • 支持自定义markdown目录位置")
    print("   • 跨平台兼容的路径分隔符")

def demonstrate_markdown_generation():
    """演示markdown生成"""
    print("\n📝 Markdown生成示例:")
    print("-" * 40)
    
    # 模拟提取的图片信息
    mock_images = [
        {
            'filename': 'page_1_img_1.png',
            'relative_path': 'images/test-document/page_1_img_1.png',
            'page': 1,
            'source': 'PDF'
        },
        {
            'filename': 'page_2_img_1.jpg',
            'relative_path': 'images/test-document/page_2_img_1.jpg',
            'page': 2,
            'source': 'PDF'
        }
    ]
    
    extractor = ImageExtractor("test-document.txt")
    markdown_content = extractor.generate_markdown_references(mock_images)
    
    print("生成的Markdown内容:")
    print(markdown_content)

if __name__ == "__main__":
    demonstrate_directory_structure()
    demonstrate_markdown_generation()
