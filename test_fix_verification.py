#!/usr/bin/env python3
"""
验证图像位置插入修复的测试脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def test_converter_behavior():
    """测试converter.py的行为"""
    print("🧪 测试converter.py的图像处理行为")
    print("=" * 50)
    
    # 创建一个简单的测试文件
    test_file = "test_simple.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("这是一个简单的测试文档。\n\n包含一些文本内容。\n")
    
    try:
        # 测试converter.py
        result = subprocess.run(
            ["python", "bin/darwin/converter.py", test_file],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            content = result.stdout
            print(f"✅ converter.py 执行成功")
            print(f"📊 输出长度: {len(content)} 字符")
            
            # 检查是否包含问题标题
            has_bad_title = "## Extracted Images" in content
            print(f"{'❌' if has_bad_title else '✅'} 标题检查: {'发现问题标题' if has_bad_title else '无问题标题'}")
            
            # 显示输出内容
            print(f"📄 输出内容:")
            print("-" * 30)
            print(content)
            print("-" * 30)
            
        else:
            print(f"❌ converter.py 执行失败")
            print(f"错误: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_image_extractor_modes():
    """测试image_extractor.py的不同模式"""
    print("\n🧪 测试image_extractor.py的不同模式")
    print("=" * 50)
    
    # 创建测试文件
    test_file = "test_for_extractor.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("测试文档内容\n图像提取测试\n")
    
    try:
        # 测试智能模式
        print("\n📋 测试智能模式 (full_content):")
        result = subprocess.run([
            "python", "bin/darwin/image_extractor.py", 
            test_file, "test_output", "test_output", "full_content"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ 智能模式执行成功")
            try:
                import json
                data = json.loads(result.stdout)
                print(f"📊 成功状态: {data.get('success', False)}")
                print(f"📝 包含内容: {bool(data.get('markdown_content'))}")
                if data.get('markdown_content'):
                    has_bad_title = "## Extracted Images" in data['markdown_content']
                    print(f"{'❌' if has_bad_title else '✅'} 内容标题检查: {'发现问题标题' if has_bad_title else '无问题标题'}")
            except json.JSONDecodeError:
                print("⚠️  输出不是有效的JSON")
                print(f"原始输出: {result.stdout}")
        else:
            print(f"❌ 智能模式执行失败: {result.stderr}")
        
        # 测试传统模式
        print("\n📋 测试传统模式 (images_only):")
        result = subprocess.run([
            "python", "bin/darwin/image_extractor.py", 
            test_file, "test_output", "test_output", "images_only"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ 传统模式执行成功")
            try:
                import json
                data = json.loads(result.stdout)
                print(f"📊 成功状态: {data.get('success', False)}")
                print(f"📝 图像数量: {data.get('images_count', 0)}")
                
                # 检查markdown引用
                markdown_refs = data.get('markdown_references', '')
                if markdown_refs:
                    has_bad_title = "## Extracted Images" in markdown_refs
                    print(f"{'❌' if has_bad_title else '✅'} 引用标题检查: {'发现问题标题' if has_bad_title else '无问题标题'}")
                
            except json.JSONDecodeError:
                print("⚠️  输出不是有效的JSON")
                print(f"原始输出: {result.stdout}")
        else:
            print(f"❌ 传统模式执行失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)
        # 清理输出目录
        import shutil
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")

def test_typescript_logic_simulation():
    """模拟TypeScript逻辑的测试"""
    print("\n🧪 模拟TypeScript调用逻辑")
    print("=" * 50)
    
    # 模拟TypeScript的新逻辑：当启用图像提取时，直接使用converter.py
    test_file = "test_typescript_sim.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("模拟TypeScript调用的测试文档\n包含一些内容用于测试\n")
    
    try:
        print("📋 模拟启用图像提取时的调用:")
        
        # 这模拟了新的TypeScript逻辑：直接调用converter.py
        result = subprocess.run([
            "python", "bin/darwin/converter.py", test_file
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            content = result.stdout
            print("✅ 模拟调用成功")
            print(f"📊 输出长度: {len(content)} 字符")
            
            # 关键检查：是否包含问题标题
            has_bad_title = "## Extracted Images" in content
            print(f"{'❌' if has_bad_title else '✅'} 最终结果检查: {'发现问题标题' if has_bad_title else '无问题标题'}")
            
            if has_bad_title:
                print("🚨 警告：仍然存在'## Extracted Images'标题！")
            else:
                print("🎉 成功：没有发现问题标题！")
                
            print(f"📄 输出预览:")
            print("-" * 30)
            print(content[:200] + "..." if len(content) > 200 else content)
            print("-" * 30)
            
        else:
            print(f"❌ 模拟调用失败: {result.stderr}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    finally:
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    print("🔍 DocuGenius 图像位置插入修复验证")
    print("=" * 60)
    
    # 检查必要文件是否存在
    required_files = [
        "bin/darwin/converter.py",
        "bin/darwin/image_extractor.py"
    ]
    
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"❌ 缺少必要文件: {missing_files}")
        return
    
    # 运行测试
    test_converter_behavior()
    test_image_extractor_modes()
    test_typescript_logic_simulation()
    
    print(f"\n📊 测试总结")
    print("=" * 30)
    print("✅ 如果所有测试都显示'无问题标题'，则修复成功")
    print("❌ 如果任何测试显示'发现问题标题'，则需要进一步修复")
    print("\n💡 下一步：")
    print("1. 如果测试通过，可以构建新的扩展包")
    print("2. 如果测试失败，需要进一步调试代码")

if __name__ == "__main__":
    main()
