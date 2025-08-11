# DocuGenius Binary Build Guide | 二进制文件构建指南

This guide explains how to rebuild the DocuGenius CLI binaries for different platforms.

本指南说明如何为不同平台重新构建DocuGenius CLI二进制文件。

## Prerequisites | 前提条件

- Python 3.6+ installed | 安装Python 3.6+
- pip package manager | pip包管理器
- For macOS builds: macOS system | macOS构建：macOS系统

## Build Script | 构建脚本

The `build_binaries.py` script can create binaries for both macOS and Windows platforms.

`build_binaries.py`脚本可以为macOS和Windows平台创建二进制文件。

### Usage | 使用方法

```bash
# Build for all platforms | 为所有平台构建
python3 build_binaries.py

# Build only for macOS | 仅为macOS构建
python3 build_binaries.py darwin

# Build only for Windows | 仅为Windows构建
python3 build_binaries.py windows
```

### Output Files | 输出文件

The script generates the following files | 脚本生成以下文件：

- **macOS**: `bin/darwin/docugenius-cli` (3.4 MB executable)
- **Windows**: `bin/win32/docugenius-cli.bat` (4.8 KB batch script)

## Build Process | 构建过程

### macOS Binary | macOS二进制文件

1. Creates a temporary Python virtual environment | 创建临时Python虚拟环境
2. Installs PyInstaller | 安装PyInstaller
3. Compiles the CLI source code into a standalone executable | 将CLI源代码编译为独立可执行文件
4. Copies the binary to `bin/darwin/` | 将二进制文件复制到`bin/darwin/`
5. Cleans up temporary files | 清理临时文件

### Windows Batch File | Windows批处理文件

1. Creates a batch script that calls Python | 创建调用Python的批处理脚本
2. Includes basic document conversion logic | 包含基本文档转换逻辑
3. Saves to `bin/win32/docugenius-cli.bat` | 保存到`bin/win32/docugenius-cli.bat`

## Testing | 测试

After building, test the binaries | 构建后，测试二进制文件：

```bash
# Test macOS binary | 测试macOS二进制文件
./bin/darwin/docugenius-cli test.txt

# Test Windows batch (on Windows) | 测试Windows批处理（在Windows上）
bin\win32\docugenius-cli.bat test.txt
```

## Supported File Formats | 支持的文件格式

The CLI supports the following formats | CLI支持以下格式：

- **Text files | 文本文件**: .txt, .md, .markdown
- **Data files | 数据文件**: .json, .csv, .xml, .html
- **Documents | 文档**: .docx, .xlsx, .pptx, .pdf

## Troubleshooting | 故障排除

### PyInstaller Installation Issues | PyInstaller安装问题

If PyInstaller fails to install | 如果PyInstaller安装失败：

```bash
# Update pip first | 首先更新pip
python3 -m pip install --upgrade pip

# Install PyInstaller manually | 手动安装PyInstaller
pip3 install pyinstaller
```

### Binary Size Optimization | 二进制文件大小优化

The current binary is optimized for size. If you need further optimization | 当前二进制文件已针对大小进行优化。如果需要进一步优化：

1. Use `--strip` flag in PyInstaller | 在PyInstaller中使用`--strip`标志
2. Use UPX compression (already enabled) | 使用UPX压缩（已启用）
3. Exclude unnecessary modules | 排除不必要的模块

### Cross-Platform Building | 跨平台构建

- macOS binaries should be built on macOS for best compatibility | macOS二进制文件应在macOS上构建以获得最佳兼容性
- Windows batch files can be created on any platform | Windows批处理文件可以在任何平台上创建
- Linux support can be added by modifying the build script | 可以通过修改构建脚本添加Linux支持

## Development | 开发

To modify the CLI functionality | 要修改CLI功能：

1. Edit the `create_cli_source()` function in `build_binaries.py` | 编辑`build_binaries.py`中的`create_cli_source()`函数
2. Rebuild the binaries | 重新构建二进制文件
3. Test the changes | 测试更改
4. Update the VS Code extension if needed | 如果需要，更新VS Code扩展

## Integration with VS Code Extension | 与VS Code扩展集成

After rebuilding binaries | 重新构建二进制文件后：

1. Recompile the TypeScript code | 重新编译TypeScript代码：
   ```bash
   npm run compile
   ```

2. Repackage the extension | 重新打包扩展：
   ```bash
   npm run package
   ```

3. The new binaries will be included in the VSIX file | 新的二进制文件将包含在VSIX文件中

## File Structure | 文件结构

```
project-plugin/
├── build_binaries.py          # Build script | 构建脚本
├── bin/
│   ├── darwin/
│   │   └── docugenius-cli      # macOS binary | macOS二进制文件
│   └── win32/
│       └── docugenius-cli.bat  # Windows batch | Windows批处理
└── src/
    └── converter.ts            # Extension code that calls binaries | 调用二进制文件的扩展代码
```
