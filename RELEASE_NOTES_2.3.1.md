# DocuGenius v2.3.1 发布说明

## 🎉 重大更新：Mac版本功能对等

我们很高兴地宣布DocuGenius v2.3.1的发布！这个版本主要专注于为Mac用户提供与Windows用户相同的完整功能体验。

## 📦 下载信息

- **文件名**: `docugenius-2.3.1-final.vsix`
- **文件大小**: 137KB（相比2.3.0版本的20MB大幅减少）
- **支持平台**: Windows 10+, macOS 10.14+
- **VS Code版本要求**: 1.74.0+

## 🚀 主要新功能

### 1. 完整的Mac版本图像提取功能
- **智能图像提取**: 支持PDF、DOCX、PPTX、XLSX格式
- **文档结构保持**: 图像在转换后的markdown中保持原始位置
- **高质量输出**: 支持多种图像格式和质量设置
- **最小尺寸过滤**: 自动过滤装饰性小图像

### 2. 新增Mac版本静态转换器
- **完整的converter.py**: 247行代码，与Windows版本功能对等
- **多格式支持**: TXT, DOCX, XLSX, PPTX, PDF
- **智能编码处理**: 自动处理各种文本编码
- **图像集成**: 转换时自动提取和引用图像

### 3. 增强的CLI工具
- **Shell脚本替代**: 使用维护性更好的shell脚本替代二进制文件
- **自动依赖管理**: 智能检测和安装所需的Python包
- **向后兼容**: 保持与现有工作流程的兼容性
- **详细错误提示**: 提供清晰的错误信息和解决建议

## 🔧 技术改进

### 文件大小优化
- **大幅减少**: 从20MB减少到137KB（减少99.3%）
- **移除冗余**: 排除了大型二进制备份文件
- **保持功能**: 所有核心功能完全保留

### 跨平台兼容性
- **统一体验**: Mac和Windows用户现在享有相同的功能
- **平台适配**: 移除了平台特定的代码限制
- **智能检测**: 自动适应不同的系统环境

### 依赖管理
- **自动安装**: CLI工具会自动安装缺失的Python包
- **智能回退**: 支持多种PDF处理库的自动回退
- **版本检测**: 智能检测Python版本和可用工具

## 📊 功能对比表

| 功能特性 | Windows 2.3.0 | Mac 2.3.0 | Mac 2.3.1 |
|----------|---------------|-----------|-----------|
| 图像提取 | ✅ 完整 | ❌ 有限 | ✅ 完整 |
| 文档转换 | ✅ 完整 | ❌ 缺失 | ✅ 完整 |
| CLI工具 | ✅ 批处理 | ❌ 旧版 | ✅ Shell脚本 |
| 依赖管理 | ✅ 自动 | ❌ 手动 | ✅ 自动 |
| 多格式支持 | ✅ 全部 | ❌ 部分 | ✅ 全部 |
| 图像集成 | ✅ 智能 | ❌ 无 | ✅ 智能 |

## 🛠️ 安装和升级

### 新用户安装
1. 下载 `docugenius-2.3.1-final.vsix` 文件
2. 在VS Code中按 `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac)
3. 输入 "Extensions: Install from VSIX"
4. 选择下载的vsix文件

### 现有用户升级
- 如果通过VS Code扩展市场安装，将自动更新
- 如果手动安装，请下载新版本并重新安装

### 系统要求
- **Python**: 3.6或更高版本
- **推荐包**: `pip install PyMuPDF python-docx python-pptx openpyxl`
- **注意**: CLI工具会自动安装缺失的依赖

## 🎯 使用指南

### 基本文档转换
```bash
# 转换单个文件
右键点击文档 → "Convert to Markdown with DocuGenius"

# 批量转换文件夹
右键点击文件夹 → "Convert Folder to Markdown"
```

### 命令行使用
```bash
# Mac用户
bin/darwin/docugenius-cli document.pdf

# Windows用户
bin/win32/docugenius-cli.bat document.pdf
```

### 图像提取
```bash
# 提取图像并生成markdown引用
python3 bin/darwin/image_extractor.py document.pdf

# 提取完整文档内容（包含图像）
python3 bin/darwin/image_extractor.py document.pdf output_dir markdown_dir full_content
```

## 🐛 已修复的问题

- Mac版本图像提取功能不完整
- Mac版本缺少静态转换器
- CLI工具依赖管理问题
- 跨平台兼容性问题
- 文件大小过大的问题

## 🔮 未来计划

- 进一步优化图像提取算法
- 添加更多文档格式支持
- 改进批量处理性能
- 增强用户界面体验

## 📞 支持和反馈

如果您遇到任何问题或有建议，请：
- 在GitHub上提交Issue: https://github.com/brucevan/docugenius/issues
- 发送邮件至: brucevanfdm@gmail.com

## 🙏 致谢

感谢所有用户的反馈和建议，特别是Mac用户对功能对等的需求，这推动了这次重大更新的实现。

---

**DocuGenius团队**  
2025年8月20日
