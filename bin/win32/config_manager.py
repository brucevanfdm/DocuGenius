# -*- coding: utf-8 -*-
"""
DocuGenius Windows 配置管理器
提供用户友好的配置界面和缓存管理功能
"""

import sys
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any

# Windows UTF-8 支持
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except:
            pass

class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.config_file = self.script_dir / "docugenius_config.json"
        self.cache_file = self.script_dir / "dependency_cache.json"
        
        self.default_config = {
            "install_mode": "smart",
            "show_progress": True,
            "auto_install": True,
            "prefer_global": True,
            "cache_duration_hours": 24,
            "user_preferences": {
                "pdf_processor": "PyMuPDF",
                "enable_image_extraction": True,
                "min_image_size": 50
            },
            "advanced_options": {
                "pip_timeout": 300,
                "retry_count": 3,
                "use_mirrors": False,
                "mirror_url": "https://pypi.tuna.tsinghua.edu.cn/simple/"
            }
        }
        
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    self.config = {**self.default_config, **loaded_config}
            except Exception as e:
                print(f"⚠️  配置文件加载失败: {e}")
                self.config = self.default_config.copy()
        else:
            self.config = self.default_config.copy()
    
    def save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print("✅ 配置已保存")
            return True
        except Exception as e:
            print(f"❌ 配置保存失败: {e}")
            return False
    
    def show_current_config(self):
        """显示当前配置"""
        print("📋 当前配置:")
        print("=" * 40)
        
        print(f"🔧 安装模式: {self.config['install_mode']}")
        print(f"📊 显示进度: {'是' if self.config['show_progress'] else '否'}")
        print(f"🚀 自动安装: {'是' if self.config['auto_install'] else '否'}")
        print(f"🌐 优先全局: {'是' if self.config['prefer_global'] else '否'}")
        print(f"⏰ 缓存时长: {self.config['cache_duration_hours']}小时")
        
        print(f"\n👤 用户偏好:")
        prefs = self.config['user_preferences']
        print(f"  📋 PDF处理器: {prefs['pdf_processor']}")
        print(f"  🖼️  图像提取: {'启用' if prefs['enable_image_extraction'] else '禁用'}")
        print(f"  📏 最小图像: {prefs['min_image_size']}像素")
        
        print(f"\n⚙️  高级选项:")
        advanced = self.config['advanced_options']
        print(f"  ⏱️  超时时间: {advanced['pip_timeout']}秒")
        print(f"  🔄 重试次数: {advanced['retry_count']}")
        print(f"  🌏 使用镜像: {'是' if advanced['use_mirrors'] else '否'}")
        if advanced['use_mirrors']:
            print(f"  🔗 镜像地址: {advanced['mirror_url']}")
    
    def interactive_config(self):
        """交互式配置"""
        print("🔧 DocuGenius 配置向导")
        print("=" * 40)
        
        # 安装模式配置
        print("\n1. 安装模式选择:")
        print("   smart  - 智能模式 (推荐)")
        print("   minimal - 最小安装")
        print("   full   - 完整安装")
        
        while True:
            mode = input(f"请选择安装模式 [{self.config['install_mode']}]: ").strip().lower()
            if not mode:
                mode = self.config['install_mode']
            if mode in ['smart', 'minimal', 'full']:
                self.config['install_mode'] = mode
                break
            print("❌ 无效选择，请重新输入")
        
        # 进度显示配置
        print("\n2. 进度显示:")
        show_progress = input(f"显示安装进度? (y/N) [{('y' if self.config['show_progress'] else 'n')}]: ").strip().lower()
        if show_progress in ['y', 'yes']:
            self.config['show_progress'] = True
        elif show_progress in ['n', 'no']:
            self.config['show_progress'] = False
        
        # 自动安装配置
        print("\n3. 自动安装:")
        auto_install = input(f"自动安装缺失的依赖? (Y/n) [{('y' if self.config['auto_install'] else 'n')}]: ").strip().lower()
        if auto_install in ['n', 'no']:
            self.config['auto_install'] = False
        elif auto_install in ['y', 'yes', '']:
            self.config['auto_install'] = True
        
        # PDF处理器选择
        print("\n4. PDF处理器:")
        print("   PyMuPDF    - 功能最全 (推荐)")
        print("   pdfplumber - 文本提取优秀")
        print("   PyPDF2     - 轻量级")
        
        pdf_processor = input(f"选择PDF处理器 [{self.config['user_preferences']['pdf_processor']}]: ").strip()
        if pdf_processor in ['PyMuPDF', 'pdfplumber', 'PyPDF2']:
            self.config['user_preferences']['pdf_processor'] = pdf_processor
        
        # 镜像配置
        print("\n5. 下载镜像:")
        use_mirrors = input(f"使用国内镜像加速下载? (y/N) [{('y' if self.config['advanced_options']['use_mirrors'] else 'n')}]: ").strip().lower()
        if use_mirrors in ['y', 'yes']:
            self.config['advanced_options']['use_mirrors'] = True
        elif use_mirrors in ['n', 'no']:
            self.config['advanced_options']['use_mirrors'] = False
        
        print("\n✅ 配置完成!")
        return self.save_config()
    
    def reset_config(self):
        """重置配置为默认值"""
        print("🔄 重置配置...")
        self.config = self.default_config.copy()
        return self.save_config()
    
    def clear_cache(self):
        """清理缓存"""
        print("🧹 清理缓存...")
        
        files_to_remove = [
            self.cache_file,
            self.script_dir / "dependency_cache.json.bak"
        ]
        
        removed_count = 0
        for file_path in files_to_remove:
            if file_path.exists():
                try:
                    file_path.unlink()
                    removed_count += 1
                    print(f"  ✅ 删除: {file_path.name}")
                except Exception as e:
                    print(f"  ❌ 删除失败: {file_path.name} - {e}")
        
        print(f"🎉 清理完成，删除了 {removed_count} 个缓存文件")
    
    def show_system_info(self):
        """显示系统信息"""
        print("💻 系统信息:")
        print("=" * 40)
        
        # Python信息
        print(f"🐍 Python版本: {sys.version}")
        print(f"📁 Python路径: {sys.executable}")
        
        # 脚本信息
        print(f"📂 脚本目录: {self.script_dir}")
        print(f"📄 配置文件: {self.config_file}")
        print(f"💾 缓存文件: {self.cache_file}")
        
        # 文件状态
        print(f"\n📋 文件状态:")
        files_to_check = [
            ("配置文件", self.config_file),
            ("缓存文件", self.cache_file),
            ("依赖管理器", self.script_dir / "dependency_manager.py"),
            ("转换器", self.script_dir / "converter.py")
        ]
        
        for name, file_path in files_to_check:
            status = "✅ 存在" if file_path.exists() else "❌ 缺失"
            size = ""
            if file_path.exists():
                try:
                    size_bytes = file_path.stat().st_size
                    size = f" ({size_bytes} bytes)"
                except:
                    pass
            print(f"  {name}: {status}{size}")

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DocuGenius 配置管理器')
    parser.add_argument('--show', action='store_true', help='显示当前配置')
    parser.add_argument('--config', action='store_true', help='交互式配置')
    parser.add_argument('--reset', action='store_true', help='重置配置')
    parser.add_argument('--clear-cache', action='store_true', help='清理缓存')
    parser.add_argument('--info', action='store_true', help='显示系统信息')
    
    args = parser.parse_args()
    
    manager = ConfigManager()
    
    if args.show:
        manager.show_current_config()
    elif args.config:
        manager.interactive_config()
    elif args.reset:
        manager.reset_config()
    elif args.clear_cache:
        manager.clear_cache()
    elif args.info:
        manager.show_system_info()
    else:
        # 默认显示配置
        manager.show_current_config()
        print("\n💡 使用 --help 查看更多选项")

if __name__ == '__main__':
    main()
