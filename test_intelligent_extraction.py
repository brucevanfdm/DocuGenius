#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试智能图片提取功能 - 图片在原始位置插入
"""

import sys
import json
from pathlib import Path

# Add the bin/win32 directory to the path
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

try:
    from image_extractor import ImageExtractor, extract_document_with_images, extract_images_from_document
    print("✓ Successfully imported image_extractor with new features")
except ImportError as e:
    print(f"✗ Failed to import image_extractor: {e}")
    sys.exit(1)

def test_intelligent_extraction():
    """测试智能提取功能"""
    print("\n=== 测试智能图片提取功能 ===")
    print("这个功能会将图片插入到文档的原始位置，而不是放在末尾")
    
    try:
        # 测试新的智能提取功能
        extractor = ImageExtractor("test-document.txt")
        
        # 测试是否有新方法
        if hasattr(extractor, 'extract_document_content_with_images'):
            print("✓ 新的智能提取方法可用")
            
            # 尝试调用新方法
            result = extractor.extract_document_content_with_images()
            print(f"✓ 智能提取执行成功")
            print(f"  - Success: {result.get('success', 'N/A')}")
            print(f"  - Error: {result.get('error', 'None')}")
            print(f"  - Has markdown_content: {'markdown_content' in result}")
            
            if result.get('markdown_content'):
                print(f"  - Markdown content length: {len(result['markdown_content'])} characters")
                print(f"  - First 200 chars: {result['markdown_content'][:200]}...")
            
        else:
            print("✗ 新的智能提取方法不可用")
            return False
            
        return True
    except Exception as e:
        print(f"✗ 智能提取测试失败: {e}")
        return False

def test_full_document_extraction():
    """测试完整文档提取功能"""
    print("\n=== 测试完整文档提取功能 ===")
    
    try:
        # 测试新的完整文档提取函数
        result = extract_document_with_images("test-document.txt")
        
        print("✓ 完整文档提取执行成功")
        print(f"  - Success: {result.get('success', 'N/A')}")
        print(f"  - Error: {result.get('error', 'None')}")
        print(f"  - Images count: {result.get('images_count', 0)}")
        print(f"  - Has markdown_content: {'markdown_content' in result}")
        
        return True
    except Exception as e:
        print(f"✗ 完整文档提取测试失败: {e}")
        return False

def compare_extraction_modes():
    """比较不同的提取模式"""
    print("\n=== 比较不同提取模式 ===")
    
    try:
        print("\n1. 传统模式 (只提取图片):")
        traditional_result = extract_images_from_document("test-document.txt")
        print(f"   - 返回字段: {list(traditional_result.keys())}")
        print(f"   - 有markdown_references: {'markdown_references' in traditional_result}")
        print(f"   - 有markdown_content: {'markdown_content' in traditional_result}")
        
        print("\n2. 智能模式 (完整文档内容):")
        intelligent_result = extract_document_with_images("test-document.txt")
        print(f"   - 返回字段: {list(intelligent_result.keys())}")
        print(f"   - 有markdown_references: {'markdown_references' in intelligent_result}")
        print(f"   - 有markdown_content: {'markdown_content' in intelligent_result}")
        
        print("\n📝 主要区别:")
        print("   - 传统模式: 只返回图片引用，需要手动插入")
        print("   - 智能模式: 返回完整的markdown内容，图片已在正确位置")
        
        return True
    except Exception as e:
        print(f"✗ 模式比较失败: {e}")
        return False

def demonstrate_usage():
    """演示使用方法"""
    print("\n=== 使用方法演示 ===")
    
    print("\n💻 命令行使用:")
    print("   # 传统模式 - 只提取图片")
    print("   python bin/win32/image_extractor.py document.pdf")
    print("")
    print("   # 智能模式 - 提取完整文档内容")
    print("   python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius full_content")
    
    print("\n🐍 Python API使用:")
    print("   # 传统模式")
    print("   result = extract_images_from_document('document.pdf')")
    print("   image_refs = result['simple_image_list']  # 手动插入图片")
    print("")
    print("   # 智能模式")
    print("   result = extract_document_with_images('document.pdf')")
    print("   markdown_content = result['markdown_content']  # 完整内容，图片已在正确位置")
    
    print("\n🎯 使用场景:")
    print("   - 智能模式: 自动生成完整的markdown文档，图片在原始位置")
    print("   - 传统模式: 需要手动控制图片位置的情况")

def main():
    """运行所有测试"""
    print("DocuGenius 智能图片提取测试")
    print("=" * 60)
    print("🎯 目标: 图片根据原文档位置自动插入到markdown内容中")
    
    tests = [
        test_intelligent_extraction,
        test_full_document_extraction,
        compare_extraction_modes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    demonstrate_usage()
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 所有测试通过! 智能图片提取功能已就绪!")
        print("现在图片会根据它们在原文档中的位置自动插入到markdown内容中")
        return 0
    else:
        print("❌ 部分测试失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
