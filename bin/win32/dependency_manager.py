# -*- coding: utf-8 -*-
"""
DocuGenius Windows 智能依赖管理器
负责检测、安装和管理Python依赖包，避免重复安装
"""

import sys
import os
import json
import subprocess
import importlib
import pkg_resources
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Windows UTF-8 支持
if sys.platform == 'win32':
    import codecs
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass

class DependencyManager:
    """智能依赖管理器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config_file = self.script_dir / "docugenius_config.json"
        self.cache_file = self.script_dir / "dependency_cache.json"
        
        # 依赖包配置
        self.dependencies = {
            'python-docx': {
                'import_name': 'docx',
                'version': '>=0.8.11',
                'description': 'DOCX文档处理',
                'size_mb': 0.5,
                'required_for': ['.docx']
            },
            'python-pptx': {
                'import_name': 'pptx',
                'version': '>=0.6.21',
                'description': 'PPTX演示文稿处理',
                'size_mb': 1.2,
                'required_for': ['.pptx']
            },
            'openpyxl': {
                'import_name': 'openpyxl',
                'version': '>=3.0.10',
                'description': 'Excel文档处理',
                'size_mb': 2.8,
                'required_for': ['.xlsx']
            },
            'pdfplumber': {
                'import_name': 'pdfplumber',
                'version': '>=0.7.0',
                'description': 'PDF文本提取（轻量级，不支持图像）',
                'size_mb': 0.8,
                'required_for': ['.pdf'],
                'priority': 1
            }
        }
        
        self.load_config()
        self.load_cache()
    
    def load_config(self):
        """加载配置文件"""
        default_config = {
            'install_mode': 'smart',  # smart, minimal, full
            'show_progress': True,
            'auto_install': True,
            'prefer_global': True,
            'cache_duration_hours': 24
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = {**default_config, **json.load(f)}
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def load_cache(self):
        """加载依赖缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except:
                self.cache = {}
        else:
            self.cache = {}
    
    def save_cache(self):
        """保存依赖缓存"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def check_package_installed(self, package_name: str, import_name: str) -> Tuple[bool, Optional[str]]:
        """检查包是否已安装，返回(是否安装, 版本)"""
        try:
            # 尝试导入包
            importlib.import_module(import_name)
            
            # 获取版本信息
            try:
                version = pkg_resources.get_distribution(package_name).version
                return True, version
            except:
                return True, None
        except ImportError:
            return False, None
    
    def check_all_dependencies(self, file_extensions: List[str] = None) -> Dict:
        """检查所有依赖的安装状态"""
        if self.config['show_progress']:
            print("🔍 检查依赖包安装状态...")
        
        status = {
            'installed': {},
            'missing': {},
            'needs_update': {},
            'total_size_mb': 0
        }
        
        # 如果指定了文件扩展名，只检查相关依赖
        if file_extensions:
            relevant_deps = {}
            for pkg, info in self.dependencies.items():
                if any(ext in info['required_for'] for ext in file_extensions):
                    relevant_deps[pkg] = info
        else:
            relevant_deps = self.dependencies
        
        for package_name, info in relevant_deps.items():
            import_name = info['import_name']
            is_installed, version = self.check_package_installed(package_name, import_name)
            
            if is_installed:
                status['installed'][package_name] = {
                    'version': version,
                    'description': info['description']
                }
                if self.config['show_progress']:
                    print(f"  ✅ {package_name} v{version or 'unknown'}")
            else:
                status['missing'][package_name] = info
                status['total_size_mb'] += info['size_mb']
                if self.config['show_progress']:
                    print(f"  ❌ {package_name} - {info['description']}")
        
        return status
    
    def install_package(self, package_name: str, version_spec: str = None) -> bool:
        """安装单个包"""
        try:
            install_spec = package_name
            if version_spec:
                install_spec = f"{package_name}{version_spec}"
            
            cmd = [sys.executable, '-m', 'pip', 'install', '--user', install_spec]
            
            if self.config['show_progress']:
                print(f"📦 安装 {package_name}...")
                result = subprocess.run(cmd, capture_output=False, text=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
            
            return result.returncode == 0
        except Exception as e:
            if self.config['show_progress']:
                print(f"❌ 安装 {package_name} 失败: {e}")
            return False
    
    def install_missing_dependencies(self, missing_deps: Dict) -> bool:
        """批量安装缺失的依赖"""
        if not missing_deps:
            return True
        
        if self.config['show_progress']:
            total_size = sum(info['size_mb'] for info in missing_deps.values())
            print(f"\n📥 需要安装 {len(missing_deps)} 个包 (约 {total_size:.1f}MB)")
            
            if not self.config['auto_install']:
                response = input("是否继续安装? (y/N): ").lower().strip()
                if response not in ['y', 'yes']:
                    return False
        
        success_count = 0
        for package_name, info in missing_deps.items():
            if self.install_package(package_name, info['version']):
                success_count += 1
            else:
                if self.config['show_progress']:
                    print(f"⚠️  {package_name} 安装失败，将尝试备选方案")
        
        if self.config['show_progress']:
            print(f"\n✅ 成功安装 {success_count}/{len(missing_deps)} 个包")
        
        return success_count > 0
    
    def ensure_dependencies(self, file_path: str = None) -> bool:
        """确保所需依赖已安装"""
        # 根据文件类型确定需要的依赖
        file_extensions = []
        if file_path:
            ext = Path(file_path).suffix.lower()
            if ext:
                file_extensions = [ext]
        
        # 检查依赖状态
        status = self.check_all_dependencies(file_extensions)
        
        # 如果有缺失的依赖，尝试安装
        if status['missing']:
            return self.install_missing_dependencies(status['missing'])
        
        if self.config['show_progress'] and status['installed']:
            print("✅ 所有依赖已满足")
        
        return True
    
    def get_dependency_info(self) -> Dict:
        """获取依赖信息摘要"""
        status = self.check_all_dependencies()
        return {
            'installed_count': len(status['installed']),
            'missing_count': len(status['missing']),
            'total_packages': len(self.dependencies),
            'estimated_size_mb': status['total_size_mb']
        }

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DocuGenius 依赖管理器')
    parser.add_argument('--check', action='store_true', help='检查依赖状态')
    parser.add_argument('--install', action='store_true', help='安装缺失的依赖')
    parser.add_argument('--file', help='指定文件路径以检查特定依赖')
    parser.add_argument('--quiet', action='store_true', help='静默模式')
    
    args = parser.parse_args()
    
    manager = DependencyManager()
    
    if args.quiet:
        manager.config['show_progress'] = False
    
    if args.check:
        info = manager.get_dependency_info()
        print(f"依赖状态: {info['installed_count']}/{info['total_packages']} 已安装")
        if info['missing_count'] > 0:
            print(f"缺失 {info['missing_count']} 个包 (约 {info['estimated_size_mb']:.1f}MB)")
    elif args.install:
        success = manager.ensure_dependencies(args.file)
        sys.exit(0 if success else 1)
    else:
        # 默认行为：确保依赖
        success = manager.ensure_dependencies(args.file)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
