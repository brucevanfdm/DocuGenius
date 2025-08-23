#!/usr/bin/env python3
"""
验证macOS二进制文件的跨架构兼容性脚本
支持Intel Mac和Apple Silicon Mac
"""

import os
import subprocess
import platform

def main():
    print("🔍 验证macOS二进制文件跨架构兼容性")
    print("=" * 50)
    
    # 检查系统架构
    arch = platform.machine()
    print(f"📱 当前系统架构: {arch}")
    if arch == "arm64":
        print("   (Apple Silicon - ARM64)")
    elif arch == "x86_64":
        print("   (Intel - x86_64)")
    else:
        print(f"   (未知架构: {arch})")
    
    # 检查二进制文件是否存在
    binary_path = "bin/darwin/docugenius-cli"
    if not os.path.exists(binary_path):
        print(f"❌ 二进制文件不存在: {binary_path}")
        return False
    
    print(f"✅ 二进制文件存在: {binary_path}")
    
    # 检查文件架构详情
    try:
        # 使用file命令检查基本信息
        result = subprocess.run(["file", binary_path], capture_output=True, text=True)
        print(f"📋 文件信息: {result.stdout.strip()}")
        
        # 使用lipo命令检查架构详情
        lipo_result = subprocess.run(["lipo", "-info", binary_path], capture_output=True, text=True)
        print(f"🏗️  架构详情: {lipo_result.stdout.strip()}")
        
        # 判断兼容性
        if "Architectures in the fat file" in lipo_result.stdout:
            print("🎉 这是一个通用二进制文件 (Universal Binary)")
            if "x86_64" in lipo_result.stdout and "arm64" in lipo_result.stdout:
                print("✅ 原生支持Intel Mac和Apple Silicon Mac")
            else:
                print("⚠️  部分架构支持")
        elif "x86_64" in lipo_result.stdout:
            print("✅ 支持Intel Mac (x86_64)")
            if arch == "arm64":
                print("✅ 在Apple Silicon Mac上通过Rosetta 2运行")
            else:
                print("✅ 在Intel Mac上原生运行")
        elif "arm64" in lipo_result.stdout:
            print("✅ 支持Apple Silicon Mac (ARM64)")
            if arch == "x86_64":
                print("❌ 在Intel Mac上无法运行")
            else:
                print("✅ 在Apple Silicon Mac上原生运行")
        else:
            print("⚠️  未知架构支持")
            
    except Exception as e:
        print(f"❌ 检查文件架构失败: {e}")
        return False
    
    # 测试二进制文件执行
    try:
        result = subprocess.run([f"./{binary_path}"], capture_output=True, text=True)
        if "DocuGenius CLI" in result.stderr:
            print("✅ 二进制文件可以正常执行")
        else:
            print("❌ 二进制文件执行异常")
            print(f"输出: {result.stdout}")
            print(f"错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 执行二进制文件失败: {e}")
        return False
    
    # 文件大小信息
    size_mb = os.path.getsize(binary_path) / (1024 * 1024)
    print(f"📊 文件大小: {size_mb:.1f} MB")
    
    print("\n🎉 Intel Mac二进制文件验证成功！")
    print("\n📝 使用方法:")
    print(f"   ./{binary_path} <文档文件>")
    print("\n支持的文件格式:")
    print("   - 文本文件: .txt, .md, .markdown")
    print("   - 数据文件: .json, .csv, .xml, .html")
    print("   - 文档文件: .docx, .xlsx, .pptx, .pdf")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)