#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试图片提取功能
"""

import sys
import json
from pathlib import Path

# Add the bin/win32 directory to the path
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

from image_extractor import extract_document_with_images, extract_images_from_document

def debug_extraction_functions():
    """调试提取函数"""
    print("调试图片提取功能")
    print("=" * 50)
    
    # 测试文档路径
    test_doc = "test-document.txt"
    
    print(f"\n测试文档: {test_doc}")
    
    print("\n1. 测试传统模式 (extract_images_from_document):")
    try:
        result1 = extract_images_from_document(test_doc)
        print(f"   - Success: {result1.get('success')}")
        print(f"   - Error: {result1.get('error')}")
        print(f"   - 返回字段: {list(result1.keys())}")
        print(f"   - 有markdown_content: {'markdown_content' in result1}")
        
        if 'markdown_references' in result1:
            md_ref = result1['markdown_references']
            if md_ref and len(md_ref) > 100:
                print(f"   - markdown_references前100字符: {md_ref[:100]}...")
            else:
                print(f"   - markdown_references: {md_ref}")
    except Exception as e:
        print(f"   - 异常: {e}")
    
    print("\n2. 测试智能模式 (extract_document_with_images):")
    try:
        result2 = extract_document_with_images(test_doc)
        print(f"   - Success: {result2.get('success')}")
        print(f"   - Error: {result2.get('error')}")
        print(f"   - 返回字段: {list(result2.keys())}")
        print(f"   - 有markdown_content: {'markdown_content' in result2}")
        
        if 'markdown_content' in result2:
            md_content = result2['markdown_content']
            if md_content and len(md_content) > 100:
                print(f"   - markdown_content前100字符: {md_content[:100]}...")
            else:
                print(f"   - markdown_content: {md_content}")
    except Exception as e:
        print(f"   - 异常: {e}")

def check_function_availability():
    """检查函数可用性"""
    print("\n检查函数可用性:")
    print("-" * 30)
    
    try:
        from image_extractor import ImageExtractor
        extractor = ImageExtractor("test.txt")
        
        # 检查是否有新方法
        if hasattr(extractor, 'extract_document_content_with_images'):
            print("✓ extract_document_content_with_images 方法存在")
        else:
            print("✗ extract_document_content_with_images 方法不存在")
            
        if hasattr(extractor, '_extract_pdf_content_with_images'):
            print("✓ _extract_pdf_content_with_images 方法存在")
        else:
            print("✗ _extract_pdf_content_with_images 方法不存在")
            
        if hasattr(extractor, '_extract_docx_content_with_images'):
            print("✓ _extract_docx_content_with_images 方法存在")
        else:
            print("✗ _extract_docx_content_with_images 方法不存在")
            
    except Exception as e:
        print(f"检查失败: {e}")

def show_usage_reminder():
    """显示使用提醒"""
    print("\n" + "=" * 50)
    print("🔍 使用提醒:")
    print("=" * 50)
    
    print("\n❌ 如果您使用的是传统调用:")
    print("   result = extract_images_from_document('doc.pdf')")
    print("   # 这会返回图片在末尾的传统格式")
    
    print("\n✅ 请使用新的智能调用:")
    print("   result = extract_document_with_images('doc.pdf')")
    print("   # 这会返回图片在原始位置的智能格式")
    
    print("\n📝 命令行使用:")
    print("   # 传统模式")
    print("   python bin/win32/image_extractor.py doc.pdf")
    print("   ")
    print("   # 智能模式")
    print("   python bin/win32/image_extractor.py doc.pdf DocuGenius/images DocuGenius full_content")

if __name__ == "__main__":
    debug_extraction_functions()
    check_function_availability()
    show_usage_reminder()
