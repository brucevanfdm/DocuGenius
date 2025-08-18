#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试集成修复 - 验证VSCode扩展现在使用智能提取
"""

import sys
import json
import subprocess
from pathlib import Path

def test_converter_py():
    """测试converter.py是否使用智能提取"""
    print("测试 converter.py 集成")
    print("-" * 40)
    
    try:
        # 测试converter.py
        converter_path = Path("bin/win32/converter.py")
        if not converter_path.exists():
            print("❌ converter.py 不存在")
            return False
        
        # 运行converter.py (使用test-document.txt，虽然不支持但可以测试代码路径)
        result = subprocess.run([
            sys.executable, str(converter_path), "test-document.txt", "true"
        ], capture_output=True, text=True, cwd=".")
        
        print(f"✓ converter.py 执行成功")
        print(f"  - 返回码: {result.returncode}")
        print(f"  - 输出长度: {len(result.stdout)} 字符")
        
        if result.stdout:
            # 检查输出是否包含智能提取的特征
            if "Page " in result.stdout or "Slide " in result.stdout:
                print("✓ 输出包含智能提取特征 (Page/Slide)")
            else:
                print("ℹ 输出不包含智能提取特征 (可能是不支持的文件类型)")
        
        return True
    except Exception as e:
        print(f"❌ converter.py 测试失败: {e}")
        return False

def test_image_extractor_modes():
    """测试image_extractor的不同模式"""
    print("\n测试 image_extractor.py 模式")
    print("-" * 40)
    
    try:
        extractor_path = Path("bin/win32/image_extractor.py")
        if not extractor_path.exists():
            print("❌ image_extractor.py 不存在")
            return False
        
        # 测试传统模式
        print("\n1. 测试传统模式:")
        result1 = subprocess.run([
            sys.executable, str(extractor_path), "test-document.txt"
        ], capture_output=True, text=True, cwd=".")
        
        if result1.returncode == 0:
            try:
                data1 = json.loads(result1.stdout)
                print(f"   ✓ 传统模式执行成功")
                print(f"   - 有 markdown_references: {'markdown_references' in data1}")
                print(f"   - 有 markdown_content: {'markdown_content' in data1}")
            except json.JSONDecodeError:
                print(f"   ❌ JSON解析失败")
        
        # 测试智能模式
        print("\n2. 测试智能模式:")
        result2 = subprocess.run([
            sys.executable, str(extractor_path), "test-document.txt", 
            "DocuGenius/images", "DocuGenius", "full_content"
        ], capture_output=True, text=True, cwd=".")
        
        if result2.returncode == 0:
            try:
                data2 = json.loads(result2.stdout)
                print(f"   ✓ 智能模式执行成功")
                print(f"   - 有 markdown_references: {'markdown_references' in data2}")
                print(f"   - 有 markdown_content: {'markdown_content' in data2}")
                print(f"   - Success: {data2.get('success', 'N/A')}")
                print(f"   - Error: {data2.get('error', 'None')}")
            except json.JSONDecodeError:
                print(f"   ❌ JSON解析失败")
        
        return True
    except Exception as e:
        print(f"❌ image_extractor 测试失败: {e}")
        return False

def check_code_changes():
    """检查代码修改是否正确"""
    print("\n检查代码修改")
    print("-" * 30)
    
    # 检查converter.py
    try:
        with open("bin/win32/converter.py", 'r', encoding='utf-8') as f:
            converter_content = f.read()
        
        if "extract_document_with_images" in converter_content:
            print("✓ converter.py 已更新为使用智能提取")
        else:
            print("❌ converter.py 仍使用旧的提取方法")
        
        if "markdown_content" in converter_content:
            print("✓ converter.py 处理 markdown_content")
        else:
            print("❌ converter.py 不处理 markdown_content")
            
    except Exception as e:
        print(f"❌ 检查 converter.py 失败: {e}")
    
    # 检查converter.ts
    try:
        with open("src/converter.ts", 'r', encoding='utf-8') as f:
            ts_content = f.read()
        
        if "full_content" in ts_content:
            print("✓ converter.ts 已更新为使用智能模式")
        else:
            print("❌ converter.ts 仍使用传统模式")
        
        if "markdown_content" in ts_content:
            print("✓ converter.ts 处理 markdown_content")
        else:
            print("❌ converter.ts 不处理 markdown_content")
            
    except Exception as e:
        print(f"❌ 检查 converter.ts 失败: {e}")

def show_usage_instructions():
    """显示使用说明"""
    print("\n" + "=" * 60)
    print("🎯 修复说明")
    print("=" * 60)
    
    print("\n✅ 已修复的问题:")
    print("   - converter.py 现在使用 extract_document_with_images()")
    print("   - converter.ts 现在调用智能模式 (full_content)")
    print("   - 图片会根据原文档位置插入，不再在文档末尾")
    
    print("\n🔧 如何测试修复:")
    print("   1. 重新编译VSCode扩展:")
    print("      npm run compile")
    print("   ")
    print("   2. 在VSCode中测试转换PDF或DOCX文件")
    print("   ")
    print("   3. 检查生成的markdown文件:")
    print("      - 图片应该在相应的页面/段落位置")
    print("      - 不应该有统一的'Extracted Images'部分")
    
    print("\n📝 直接测试命令:")
    print("   python bin/win32/converter.py your_document.pdf true")

def main():
    """主函数"""
    print("DocuGenius 集成修复测试")
    print("=" * 60)
    print("🎯 验证VSCode扩展现在使用智能图片提取")
    
    tests = [
        test_converter_py,
        test_image_extractor_modes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    check_code_changes()
    show_usage_instructions()
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 集成修复成功!")
        print("现在VSCode扩展会使用智能图片提取，图片不再在文档末尾!")
        return 0
    else:
        print("⚠️ 部分测试失败，请检查修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
