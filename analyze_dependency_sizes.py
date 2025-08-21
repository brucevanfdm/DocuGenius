#!/usr/bin/env python3
"""
分析DocuGenius Python依赖包的磁盘占用情况
"""

import subprocess
import sys
import tempfile
import os
import shutil
from pathlib import Path

def get_package_info(package_name):
    """获取包的详细信息"""
    try:
        # 获取包信息
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'show', package_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            return info
        return None
    except Exception as e:
        print(f"获取{package_name}信息失败: {e}")
        return None

def estimate_download_size(package_name):
    """估算包的下载大小"""
    try:
        # 使用pip download --dry-run来估算大小
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'download', '--dry-run', '--no-deps', package_name
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            # 解析输出中的大小信息
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Would download' in line and package_name.lower() in line.lower():
                    # 尝试提取大小信息
                    if '(' in line and ')' in line:
                        size_part = line.split('(')[1].split(')')[0]
                        if 'MB' in size_part:
                            try:
                                size = float(size_part.replace('MB', '').strip())
                                return size
                            except:
                                pass
                        elif 'kB' in size_part:
                            try:
                                size = float(size_part.replace('kB', '').strip()) / 1024
                                return size
                            except:
                                pass
        return None
    except Exception as e:
        print(f"估算{package_name}下载大小失败: {e}")
        return None

def analyze_current_installation():
    """分析当前已安装的包"""
    packages = [
        'python-docx',
        'python-pptx', 
        'openpyxl',
        'PyMuPDF',
        'pdfplumber',
        'PyPDF2'
    ]
    
    print("📦 DocuGenius Python依赖分析报告")
    print("=" * 60)
    
    total_installed_size = 0
    installed_count = 0
    
    print("\n🔍 当前安装状态:")
    print("-" * 40)
    
    for pkg in packages:
        info = get_package_info(pkg)
        if info:
            print(f"✅ {pkg:<15} v{info.get('Version', 'Unknown')}")
            
            # 尝试计算实际安装大小
            location = info.get('Location', '')
            if location:
                try:
                    pkg_path = Path(location) / pkg.replace('-', '_')
                    if pkg_path.exists():
                        size = sum(f.stat().st_size for f in pkg_path.rglob('*') if f.is_file())
                        size_mb = size / (1024 * 1024)
                        total_installed_size += size_mb
                        print(f"   📊 安装大小: ~{size_mb:.1f}MB")
                    else:
                        print(f"   📊 安装大小: 未知")
                except Exception as e:
                    print(f"   📊 安装大小: 计算失败 ({e})")
            
            installed_count += 1
        else:
            print(f"❌ {pkg:<15} 未安装")
    
    print(f"\n📊 安装状态总结:")
    print(f"   已安装包数: {installed_count}/{len(packages)}")
    print(f"   总安装大小: ~{total_installed_size:.1f}MB")
    
    return packages, installed_count, total_installed_size

def estimate_full_installation_size():
    """估算完整安装所需的大小"""
    packages = [
        'python-docx',
        'python-pptx', 
        'openpyxl',
        'PyMuPDF',
        'pdfplumber',
        'PyPDF2'
    ]
    
    print(f"\n🔍 估算完整安装大小:")
    print("-" * 40)
    
    # 已知的大概大小（基于经验和网络资料）
    estimated_sizes = {
        'python-docx': 0.5,    # ~500KB
        'python-pptx': 1.2,    # ~1.2MB
        'openpyxl': 2.8,       # ~2.8MB
        'PyMuPDF': 45.0,       # ~45MB (包含MuPDF库)
        'pdfplumber': 0.8,     # ~800KB
        'PyPDF2': 0.3          # ~300KB
    }
    
    total_estimated = 0
    
    for pkg in packages:
        size = estimated_sizes.get(pkg, 1.0)  # 默认1MB
        total_estimated += size
        print(f"📦 {pkg:<15} ~{size:.1f}MB")
    
    print(f"\n📊 估算总大小: ~{total_estimated:.1f}MB")
    
    # 考虑依赖包
    dependency_overhead = total_estimated * 0.3  # 估算30%的依赖开销
    total_with_deps = total_estimated + dependency_overhead
    
    print(f"📦 包含依赖估算: ~{total_with_deps:.1f}MB")
    
    return total_with_deps

def analyze_windows_batch_behavior():
    """分析Windows批处理脚本的行为"""
    print(f"\n🔍 Windows批处理脚本分析:")
    print("-" * 40)
    
    batch_file = Path("bin/win32/docugenius-cli.bat")
    if batch_file.exists():
        with open(batch_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📋 发现的安装行为:")
        
        # 分析安装逻辑
        install_commands = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'pip install --user' in line:
                pkg = line.split('pip install --user')[1].strip().split()[0]
                install_commands.append(pkg)
                print(f"   🔧 条件安装: {pkg}")
        
        print(f"\n📊 批处理脚本特点:")
        print(f"   ✅ 使用 --user 标志 (用户级安装)")
        print(f"   ✅ 条件安装 (仅在需要时安装)")
        print(f"   ✅ 按文件类型安装对应依赖")
        print(f"   📦 可能安装的包: {len(install_commands)} 个")
        
        return install_commands
    else:
        print("❌ 未找到Windows批处理文件")
        return []

def suggest_alternatives():
    """建议替代方案"""
    print(f"\n💡 替代方案分析:")
    print("=" * 60)
    
    print("🔧 方案1: 虚拟环境隔离")
    print("   优点: 完全隔离，不污染系统环境")
    print("   缺点: 每个项目重复安装，占用更多空间")
    print("   估算空间: 每个项目 ~50-80MB")
    
    print("\n🔧 方案2: 系统依赖检测")
    print("   优点: 复用已安装的包，节省空间")
    print("   缺点: 版本冲突风险，依赖用户环境")
    print("   估算空间: 0MB (如果已安装)")
    
    print("\n🔧 方案3: 轻量级依赖")
    print("   优点: 减少核心依赖，按需加载")
    print("   缺点: 功能可能受限")
    print("   估算空间: ~10-20MB")
    
    print("\n🔧 方案4: 二进制打包 (当前macOS方案)")
    print("   优点: 自包含，无依赖问题")
    print("   缺点: 文件大，更新困难")
    print("   估算空间: ~35-40MB (单个二进制文件)")
    
    print("\n🔧 方案5: 混合方案")
    print("   优点: 结合多种方案的优点")
    print("   缺点: 复杂度增加")
    print("   估算空间: 根据情况而定")

def main():
    print("🔍 DocuGenius Windows依赖占用分析")
    print("=" * 60)
    
    # 分析当前安装
    packages, installed_count, installed_size = analyze_current_installation()
    
    # 估算完整安装大小
    estimated_total = estimate_full_installation_size()
    
    # 分析Windows批处理行为
    batch_packages = analyze_windows_batch_behavior()
    
    # 建议替代方案
    suggest_alternatives()
    
    # 总结报告
    print(f"\n📊 总结报告:")
    print("=" * 60)
    print(f"📦 DocuGenius需要的Python包: {len(packages)} 个")
    print(f"💾 估算完整安装大小: ~{estimated_total:.1f}MB")
    print(f"🔄 重复安装问题: 每个用户/项目都可能重复安装")
    print(f"📈 潜在磁盘占用: 如果10个项目使用 = ~{estimated_total * 10:.0f}MB")
    
    print(f"\n🎯 建议:")
    print("1. 考虑使用系统依赖检测，避免重复安装")
    print("2. 实现轻量级依赖策略，减少核心包数量")
    print("3. 提供用户选择：完整安装 vs 按需安装")
    print("4. 考虑为Windows也提供二进制方案")

if __name__ == "__main__":
    main()
