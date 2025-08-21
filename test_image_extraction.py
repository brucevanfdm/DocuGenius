#!/usr/bin/env python3
"""
测试脚本：验证DocuGenius的图像提取功能
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def test_cli_extraction(document_path, mode="full_content"):
    """测试CLI图像提取功能"""
    print(f"\n🔍 测试CLI提取: {document_path} (模式: {mode})")
    
    # 构建命令
    extractor_path = "bin/darwin/image_extractor.py"
    output_dir = "test_output/images"
    markdown_dir = "test_output"
    
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    Path(markdown_dir).mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "python", extractor_path, 
        document_path, 
        output_dir, 
        markdown_dir, 
        mode, 
        "50"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                print(f"✅ 成功: {data.get('success', False)}")
                print(f"📊 图像数量: {data.get('images_count', 0)}")
                
                if mode == "full_content":
                    has_content = bool(data.get('markdown_content'))
                    print(f"📝 包含完整内容: {has_content}")
                    if has_content:
                        content_preview = data['markdown_content'][:200] + "..." if len(data['markdown_content']) > 200 else data['markdown_content']
                        print(f"📄 内容预览: {content_preview}")
                        
                        # 检查是否包含图像引用
                        image_refs = data['markdown_content'].count('![')
                        print(f"🖼️  图像引用数量: {image_refs}")
                        
                        # 检查是否有"## Extracted Images"标题
                        has_extracted_section = "## Extracted Images" in data['markdown_content']
                        print(f"❌ 包含'## Extracted Images'标题: {has_extracted_section}")
                
                return data
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析错误: {e}")
                print(f"原始输出: {result.stdout}")
                return None
        else:
            print(f"❌ 命令执行失败 (返回码: {result.returncode})")
            print(f"错误输出: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ 命令执行超时")
        return None
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return None

def test_converter_py(document_path):
    """测试converter.py的集成功能"""
    print(f"\n🔍 测试converter.py集成: {document_path}")
    
    converter_path = "bin/darwin/converter.py"
    
    try:
        result = subprocess.run(
            ["python", converter_path, document_path], 
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            content = result.stdout
            print(f"✅ 转换成功")
            print(f"📊 内容长度: {len(content)} 字符")
            
            # 检查图像引用
            image_refs = content.count('![')
            print(f"🖼️  图像引用数量: {image_refs}")
            
            # 检查是否有"## Extracted Images"标题
            has_extracted_section = "## Extracted Images" in content
            print(f"❌ 包含'## Extracted Images'标题: {has_extracted_section}")
            
            # 保存结果用于检查
            output_file = f"test_output/converter_result_{Path(document_path).stem}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 结果已保存到: {output_file}")
            
            return content
        else:
            print(f"❌ 转换失败 (返回码: {result.returncode})")
            print(f"错误输出: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ 转换超时")
        return None
    except Exception as e:
        print(f"❌ 转换错误: {e}")
        return None

def main():
    print("🧪 DocuGenius 图像提取功能测试")
    print("=" * 50)
    
    # 检查测试文档
    test_docs = []
    
    # 查找测试文档
    for ext in ['.pdf', '.docx']:
        for test_file in Path('.').glob(f'*{ext}'):
            test_docs.append(str(test_file))
    
    if not test_docs:
        print("❌ 未找到测试文档 (.pdf 或 .docx 文件)")
        print("请在当前目录放置一些包含图像的PDF或DOCX文件进行测试")
        return
    
    print(f"📁 找到测试文档: {test_docs}")
    
    for doc_path in test_docs:
        print(f"\n{'='*60}")
        print(f"📄 测试文档: {doc_path}")
        print(f"{'='*60}")
        
        # 测试1: CLI智能提取
        cli_result = test_cli_extraction(doc_path, "full_content")
        
        # 测试2: CLI传统提取
        cli_traditional = test_cli_extraction(doc_path, "images_only")
        
        # 测试3: converter.py集成
        converter_result = test_converter_py(doc_path)
        
        # 分析结果
        print(f"\n📊 {doc_path} 测试总结:")
        if cli_result and cli_result.get('success'):
            print(f"  ✅ CLI智能提取: 成功 ({cli_result.get('images_count', 0)} 图像)")
            if cli_result.get('markdown_content'):
                has_bad_title = "## Extracted Images" in cli_result['markdown_content']
                print(f"  {'❌' if has_bad_title else '✅'} 智能提取标题检查: {'发现问题标题' if has_bad_title else '正常'}")
        else:
            print("  ❌ CLI智能提取: 失败")
            
        if converter_result:
            has_bad_title = "## Extracted Images" in converter_result
            print(f"  {'❌' if has_bad_title else '✅'} converter.py标题检查: {'发现问题标题' if has_bad_title else '正常'}")
        else:
            print("  ❌ converter.py集成: 失败")

if __name__ == "__main__":
    main()
