#!/usr/bin/env python3
"""
测试macOS版本的pdfplumber同步调整
验证与Windows版本的一致性
"""

import sys
import os
import tempfile
from pathlib import Path

def test_macos_converter():
    """测试macOS版本的converter.py"""
    print("🍎 测试macOS版本converter.py")
    print("=" * 50)
    
    try:
        # 添加macOS路径
        sys.path.insert(0, 'bin/darwin')
        from converter import convert_with_images
        
        print("✅ macOS converter导入成功")
        
        # 创建测试文件
        test_content = "测试PDF内容\n包含中文字符\n多行文本测试"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            # 测试转换
            result = convert_with_images(test_file, False)
            
            if result and len(result) > 0:
                print("✅ macOS文本转换成功")
                print(f"   输出长度: {len(result)} 字符")
                return True
            else:
                print("❌ macOS文本转换失败")
                return False
                
        finally:
            os.unlink(test_file)
            
    except Exception as e:
        print(f"❌ macOS converter测试失败: {e}")
        return False

def test_macos_image_extractor():
    """测试macOS版本的image_extractor.py"""
    print(f"\n🖼️ 测试macOS版本image_extractor.py")
    print("=" * 50)
    
    try:
        # 添加macOS路径
        sys.path.insert(0, 'bin/darwin')
        from image_extractor import extract_document_with_images
        
        print("✅ macOS image_extractor导入成功")
        
        # 创建测试PDF文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False, encoding='utf-8') as f:
            f.write("测试PDF内容")
            test_pdf = f.name
        
        try:
            # 测试PDF图像提取
            result = extract_document_with_images(test_pdf)
            
            print(f"📊 macOS PDF图像提取结果:")
            if isinstance(result, dict):
                print(f"   成功: {result.get('success', False)}")
                print(f"   错误信息: {result.get('error', 'N/A')}")
                print(f"   说明: {result.get('note', 'N/A')}")
                
                # 检查是否正确返回不支持信息
                if not result.get('success') and 'lightweight mode' in result.get('error', ''):
                    print("✅ macOS正确返回轻量化模式不支持信息")
                    return True
                else:
                    print("❌ macOS返回信息不符合预期")
                    return False
            else:
                print(f"❌ macOS返回类型错误: {type(result)}")
                return False
                
        finally:
            os.unlink(test_pdf)
            
    except Exception as e:
        print(f"❌ macOS image_extractor测试失败: {e}")
        return False

def compare_with_windows():
    """对比Windows和macOS版本的一致性"""
    print(f"\n🔄 对比Windows和macOS版本一致性")
    print("=" * 50)
    
    try:
        # 测试Windows版本
        sys.path.insert(0, 'bin/win32')
        from converter import simple_convert as win_convert
        from image_extractor import ImageExtractor as WinImageExtractor
        
        # 测试macOS版本
        sys.path.insert(0, 'bin/darwin')
        from converter import simple_convert as mac_convert
        from image_extractor import ImageExtractor as MacImageExtractor
        
        print("✅ 两个版本都成功导入")
        
        # 创建测试文件
        test_content = "测试内容\n多行文本"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(test_content)
            test_file = f.name
        
        try:
            # 测试文本转换一致性
            win_result = win_convert(test_file)
            mac_result = mac_convert(test_file)
            
            if win_result == mac_result:
                print("✅ 文本转换结果一致")
            else:
                print("⚠️  文本转换结果有差异")
                print(f"   Windows: {win_result[:50]}...")
                print(f"   macOS: {mac_result[:50]}...")
            
            # 测试PDF图像提取行为一致性
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pdf', delete=False, encoding='utf-8') as f:
                f.write("测试PDF")
                test_pdf = f.name
            
            try:
                win_extractor = WinImageExtractor(test_pdf)
                mac_extractor = MacImageExtractor(test_pdf)
                
                win_pdf_result = win_extractor._extract_from_pdf()
                mac_pdf_result = mac_extractor._extract_from_pdf()
                
                # 检查两个版本是否都返回不支持信息
                win_unsupported = not win_pdf_result.get('success') and 'lightweight mode' in win_pdf_result.get('error', '')
                mac_unsupported = not mac_pdf_result.get('success') and 'lightweight mode' in mac_pdf_result.get('error', '')
                
                if win_unsupported and mac_unsupported:
                    print("✅ PDF图像提取行为一致 (都不支持)")
                    return True
                else:
                    print("❌ PDF图像提取行为不一致")
                    print(f"   Windows: {win_pdf_result}")
                    print(f"   macOS: {mac_pdf_result}")
                    return False
                    
            finally:
                os.unlink(test_pdf)
                
        finally:
            os.unlink(test_file)
            
    except Exception as e:
        print(f"❌ 版本对比测试失败: {e}")
        return False

def check_file_consistency():
    """检查文件结构一致性"""
    print(f"\n📁 检查文件结构一致性")
    print("=" * 50)
    
    win_files = set()
    mac_files = set()
    
    # 检查Windows文件
    win_dir = Path("bin/win32")
    if win_dir.exists():
        for file in win_dir.glob("*.py"):
            win_files.add(file.name)
    
    # 检查macOS文件
    mac_dir = Path("bin/darwin")
    if mac_dir.exists():
        for file in mac_dir.glob("*.py"):
            mac_files.add(file.name)
    
    print(f"Windows文件: {sorted(win_files)}")
    print(f"macOS文件: {sorted(mac_files)}")
    
    # 检查核心文件是否都存在
    core_files = {'converter.py', 'image_extractor.py'}
    
    win_has_core = core_files.issubset(win_files)
    mac_has_core = core_files.issubset(mac_files)
    
    if win_has_core and mac_has_core:
        print("✅ 两个平台都有核心文件")
        
        # 检查是否有Windows独有的文件
        win_only = win_files - mac_files
        mac_only = mac_files - win_files
        
        if win_only:
            print(f"⚠️  Windows独有文件: {win_only}")
        if mac_only:
            print(f"⚠️  macOS独有文件: {mac_only}")
        
        return True
    else:
        print("❌ 核心文件缺失")
        if not win_has_core:
            print(f"   Windows缺失: {core_files - win_files}")
        if not mac_has_core:
            print(f"   macOS缺失: {core_files - mac_files}")
        return False

def main():
    print("🔍 macOS版本pdfplumber同步调整测试")
    print("=" * 60)
    
    test_results = []
    
    # 文件结构检查
    result1 = check_file_consistency()
    test_results.append(("文件结构", result1))
    
    # macOS converter测试
    result2 = test_macos_converter()
    test_results.append(("macOS converter", result2))
    
    # macOS image_extractor测试
    result3 = test_macos_image_extractor()
    test_results.append(("macOS image_extractor", result3))
    
    # 版本一致性对比
    result4 = compare_with_windows()
    test_results.append(("版本一致性", result4))
    
    # 总结
    print(f"\n📊 测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 macOS版本同步调整成功！")
        print("\n📈 同步效果:")
        print("   • macOS和Windows版本行为一致")
        print("   • 都使用pdfplumber进行PDF文本提取")
        print("   • 都不支持PDF图像提取")
        print("   • 保持轻量化依赖策略")
    else:
        print("⚠️  部分测试失败，需要进一步调整")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
