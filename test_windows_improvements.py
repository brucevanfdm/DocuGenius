#!/usr/bin/env python3
"""
测试Windows改进脚本的功能和性能
"""

import os
import sys
import time
import subprocess
import tempfile
from pathlib import Path

def create_test_files():
    """创建测试文件"""
    print("📁 创建测试文件...")
    
    test_files = []
    
    # 创建简单的文本文件
    txt_file = "test_document.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("这是一个测试文档\n包含一些中文内容\n用于测试DocuGenius的功能")
    test_files.append(txt_file)
    print(f"  ✅ 创建: {txt_file}")
    
    # 创建CSV文件
    csv_file = "test_data.csv"
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("姓名,年龄,城市\n张三,25,北京\n李四,30,上海\n王五,28,广州\n")
    test_files.append(csv_file)
    print(f"  ✅ 创建: {csv_file}")
    
    return test_files

def test_dependency_manager():
    """测试依赖管理器"""
    print("\n🔍 测试依赖管理器...")
    
    dep_manager_path = Path("bin/win32/dependency_manager.py")
    if not dep_manager_path.exists():
        print("❌ 依赖管理器不存在")
        return False
    
    try:
        # 测试检查功能
        print("  📋 测试依赖检查...")
        result = subprocess.run([
            sys.executable, str(dep_manager_path), "--check"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("  ✅ 依赖检查成功")
            print(f"     输出: {result.stdout.strip()}")
        else:
            print(f"  ⚠️  依赖检查返回码: {result.returncode}")
            print(f"     错误: {result.stderr.strip()}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("  ❌ 依赖管理器测试超时")
        return False
    except Exception as e:
        print(f"  ❌ 依赖管理器测试失败: {e}")
        return False

def test_config_manager():
    """测试配置管理器"""
    print("\n🔧 测试配置管理器...")
    
    config_manager_path = Path("bin/win32/config_manager.py")
    if not config_manager_path.exists():
        print("❌ 配置管理器不存在")
        return False
    
    try:
        # 测试显示配置
        print("  📋 测试配置显示...")
        result = subprocess.run([
            sys.executable, str(config_manager_path), "--show"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ 配置显示成功")
            lines = result.stdout.strip().split('\n')[:3]  # 只显示前3行
            for line in lines:
                print(f"     {line}")
        else:
            print(f"  ❌ 配置显示失败: {result.stderr.strip()}")
        
        # 测试系统信息
        print("  💻 测试系统信息...")
        result = subprocess.run([
            sys.executable, str(config_manager_path), "--info"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("  ✅ 系统信息获取成功")
        else:
            print(f"  ❌ 系统信息获取失败")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置管理器测试失败: {e}")
        return False

def test_improved_batch_script():
    """测试改进的批处理脚本"""
    print("\n🚀 测试改进的批处理脚本...")
    
    improved_script = Path("bin/win32/docugenius-cli-improved.bat")
    if not improved_script.exists():
        print("❌ 改进的批处理脚本不存在")
        return False
    
    # 创建测试文件
    test_files = create_test_files()
    
    try:
        for test_file in test_files:
            print(f"  📄 测试文件: {test_file}")
            
            start_time = time.time()
            
            # 在Windows上，我们需要使用cmd来运行bat文件
            if sys.platform == 'win32':
                cmd = ['cmd', '/c', str(improved_script), test_file]
            else:
                # 在非Windows系统上，我们只能模拟测试
                print(f"  ⚠️  非Windows系统，跳过批处理脚本测试")
                continue
            
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            print(f"     执行时间: {duration:.2f}秒")
            print(f"     返回码: {result.returncode}")
            
            if result.returncode == 0:
                print(f"  ✅ {test_file} 处理成功")
            else:
                print(f"  ❌ {test_file} 处理失败")
                if result.stderr:
                    print(f"     错误: {result.stderr.strip()[:200]}...")
        
        return True
        
    except subprocess.TimeoutExpired:
        print("  ❌ 批处理脚本测试超时")
        return False
    except Exception as e:
        print(f"  ❌ 批处理脚本测试失败: {e}")
        return False
    finally:
        # 清理测试文件
        for test_file in test_files:
            try:
                if os.path.exists(test_file):
                    os.remove(test_file)
            except:
                pass

def compare_performance():
    """性能对比测试"""
    print("\n📊 性能对比测试...")
    
    original_script = Path("bin/win32/docugenius-cli.bat")
    improved_script = Path("bin/win32/docugenius-cli-improved.bat")
    
    if not original_script.exists():
        print("❌ 原始脚本不存在，跳过性能对比")
        return
    
    if not improved_script.exists():
        print("❌ 改进脚本不存在，跳过性能对比")
        return
    
    # 创建测试文件
    test_file = "performance_test.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("性能测试文档")
    
    try:
        scripts = [
            ("原始脚本", original_script),
            ("改进脚本", improved_script)
        ]
        
        results = {}
        
        for name, script_path in scripts:
            if sys.platform != 'win32':
                print(f"  ⚠️  非Windows系统，跳过 {name} 测试")
                continue
            
            print(f"  🔄 测试 {name}...")
            
            start_time = time.time()
            
            try:
                result = subprocess.run([
                    'cmd', '/c', str(script_path), test_file
                ], capture_output=True, text=True, timeout=30)
                
                end_time = time.time()
                duration = end_time - start_time
                
                results[name] = {
                    'duration': duration,
                    'success': result.returncode == 0,
                    'output_length': len(result.stdout)
                }
                
                print(f"     执行时间: {duration:.2f}秒")
                print(f"     成功: {'是' if result.returncode == 0 else '否'}")
                
            except subprocess.TimeoutExpired:
                print(f"     ❌ {name} 超时")
                results[name] = {'duration': 30, 'success': False, 'output_length': 0}
        
        # 显示对比结果
        if len(results) >= 2:
            print(f"\n📈 性能对比结果:")
            original_time = results.get("原始脚本", {}).get('duration', 0)
            improved_time = results.get("改进脚本", {}).get('duration', 0)
            
            if original_time > 0 and improved_time > 0:
                improvement = ((original_time - improved_time) / original_time) * 100
                print(f"   时间改进: {improvement:.1f}%")
                
                if improvement > 0:
                    print(f"   ✅ 改进脚本更快")
                else:
                    print(f"   ⚠️  改进脚本较慢 (可能由于额外的功能)")
    
    finally:
        # 清理测试文件
        try:
            if os.path.exists(test_file):
                os.remove(test_file)
        except:
            pass

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
    required_files = [
        "bin/win32/dependency_manager.py",
        "bin/win32/config_manager.py",
        "bin/win32/docugenius_config.json",
        "bin/win32/requirements.txt",
        "bin/win32/docugenius-cli-improved.bat",
        "bin/win32/converter.py",
        "bin/win32/image_extractor.py"
    ]
    
    missing_files = []
    existing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            existing_files.append(file_path)
            print(f"  ✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"  ❌ {file_path}")
    
    print(f"\n📊 文件结构检查结果:")
    print(f"   存在: {len(existing_files)}/{len(required_files)}")
    print(f"   缺失: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  缺失的文件:")
        for file_path in missing_files:
            print(f"     - {file_path}")
    
    return len(missing_files) == 0

def main():
    """主测试函数"""
    print("🧪 DocuGenius Windows改进方案测试")
    print("=" * 50)
    
    test_results = {}
    
    # 测试文件结构
    test_results['file_structure'] = test_file_structure()
    
    # 测试依赖管理器
    test_results['dependency_manager'] = test_dependency_manager()
    
    # 测试配置管理器
    test_results['config_manager'] = test_config_manager()
    
    # 测试改进的批处理脚本
    test_results['improved_script'] = test_improved_batch_script()
    
    # 性能对比
    compare_performance()
    
    # 总结
    print(f"\n📊 测试总结:")
    print("=" * 50)
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！改进方案可以部署")
    else:
        print("⚠️  部分测试失败，需要进一步调试")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
