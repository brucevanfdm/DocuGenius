#!/bin/bash
# DocuGenius v2.3.1 安装验证脚本

echo "🔍 DocuGenius v2.3.1 安装验证"
echo "================================"

# 检查操作系统
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "📱 检测到操作系统: $MACHINE"

# 检查Python
echo ""
echo "🐍 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python3: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✅ Python: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "❌ Python未安装或不在PATH中"
    echo "   请从 https://python.org 安装Python"
    exit 1
fi

# 检查DocuGenius文件
echo ""
echo "📁 检查DocuGenius文件..."

if [ "$MACHINE" = "Mac" ]; then
    CLI_PATH="bin/darwin/docugenius-cli"
    CONVERTER_PATH="bin/darwin/converter.py"
    EXTRACTOR_PATH="bin/darwin/image_extractor.py"
else
    CLI_PATH="bin/win32/docugenius-cli.bat"
    CONVERTER_PATH="bin/win32/converter.py"
    EXTRACTOR_PATH="bin/win32/image_extractor.py"
fi

# 检查CLI工具
if [ -f "$CLI_PATH" ]; then
    echo "✅ CLI工具: $CLI_PATH"
    if [ -x "$CLI_PATH" ]; then
        echo "   ✅ 可执行权限正常"
    else
        echo "   ⚠️  缺少执行权限，尝试修复..."
        chmod +x "$CLI_PATH"
    fi
else
    echo "❌ CLI工具未找到: $CLI_PATH"
fi

# 检查转换器
if [ -f "$CONVERTER_PATH" ]; then
    echo "✅ 转换器: $CONVERTER_PATH"
    # 检查文件大小
    SIZE=$(wc -l < "$CONVERTER_PATH" 2>/dev/null || echo "0")
    if [ "$SIZE" -gt 200 ]; then
        echo "   ✅ 文件完整 ($SIZE 行)"
    else
        echo "   ⚠️  文件可能不完整 ($SIZE 行)"
    fi
else
    echo "❌ 转换器未找到: $CONVERTER_PATH"
fi

# 检查图像提取器
if [ -f "$EXTRACTOR_PATH" ]; then
    echo "✅ 图像提取器: $EXTRACTOR_PATH"
    # 检查文件大小
    SIZE=$(wc -l < "$EXTRACTOR_PATH" 2>/dev/null || echo "0")
    if [ "$SIZE" -gt 800 ]; then
        echo "   ✅ 文件完整 ($SIZE 行)"
    else
        echo "   ⚠️  文件可能不完整 ($SIZE 行)"
    fi
else
    echo "❌ 图像提取器未找到: $EXTRACTOR_PATH"
fi

# 测试基本功能
echo ""
echo "🧪 测试基本功能..."

# 测试CLI工具
if [ -f "$CLI_PATH" ]; then
    echo "测试CLI工具..."
    if [ "$MACHINE" = "Mac" ]; then
        OUTPUT=$("$CLI_PATH" 2>&1 | head -1)
    else
        OUTPUT=$(cmd //c "$CLI_PATH" 2>&1 | head -1)
    fi
    
    if [[ "$OUTPUT" == *"DocuGenius"* ]]; then
        echo "✅ CLI工具运行正常"
    else
        echo "⚠️  CLI工具可能有问题"
        echo "   输出: $OUTPUT"
    fi
fi

# 测试Python模块
echo "测试Python模块..."
if [ -f "$EXTRACTOR_PATH" ]; then
    OUTPUT=$($PYTHON_CMD "$EXTRACTOR_PATH" 2>&1 | head -1)
    if [[ "$OUTPUT" == *"DocuGenius"* ]] || [[ "$OUTPUT" == *"Usage"* ]]; then
        echo "✅ 图像提取器运行正常"
    else
        echo "⚠️  图像提取器可能有问题"
        echo "   输出: $OUTPUT"
    fi
fi

# 检查推荐的Python包
echo ""
echo "📦 检查推荐的Python包..."

PACKAGES=("docx" "openpyxl" "pptx" "fitz" "pdfplumber" "PyPDF2")
PACKAGE_NAMES=("python-docx" "openpyxl" "python-pptx" "PyMuPDF" "pdfplumber" "PyPDF2")

for i in "${!PACKAGES[@]}"; do
    PACKAGE="${PACKAGES[$i]}"
    PACKAGE_NAME="${PACKAGE_NAMES[$i]}"
    
    if $PYTHON_CMD -c "import $PACKAGE" 2>/dev/null; then
        echo "✅ $PACKAGE_NAME"
    else
        echo "⚠️  $PACKAGE_NAME (可选，CLI工具会自动安装)"
    fi
done

# 总结
echo ""
echo "📋 验证总结"
echo "============"

if [ -f "$CLI_PATH" ] && [ -f "$CONVERTER_PATH" ] && [ -f "$EXTRACTOR_PATH" ]; then
    echo "✅ DocuGenius v2.3.1 安装完整"
    echo ""
    echo "🚀 快速开始:"
    echo "1. 在VS Code中右键点击文档文件"
    echo "2. 选择 'Convert to Markdown with DocuGenius'"
    echo "3. 或使用命令行: $CLI_PATH <文件路径>"
    echo ""
    echo "📚 更多信息请查看 README.md"
else
    echo "❌ 安装不完整，请重新安装DocuGenius扩展"
fi

echo ""
echo "🎉 验证完成！"
