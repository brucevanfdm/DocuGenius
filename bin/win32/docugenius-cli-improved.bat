@echo off
REM DocuGenius CLI - 改进版Windows脚本
REM 版本: 2.3.6
REM 特性: 智能依赖检测、用户友好提示、批量安装、缓存管理

REM 设置UTF-8编码和延迟变量扩展
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

REM 设置环境变量以支持Unicode
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM 获取脚本目录
set SCRIPT_DIR=%~dp0

REM 显示启动信息
echo.
echo 🚀 DocuGenius CLI v2.3.6 - 智能版
echo ========================================

REM 获取输入文件和图片提取参数
set INPUT_FILE=%1
set EXTRACT_IMAGES=%2

REM 如果没有指定图片提取参数，默认为true
if "%EXTRACT_IMAGES%"=="" set EXTRACT_IMAGES=true

REM 检查是否提供了文件参数
if "%INPUT_FILE%"=="" (
    echo ❌ 错误: 请指定输入文件
    echo.
    echo 📋 用法: %0 ^<input_file^>
    echo.
    echo 📁 支持的文件格式:
    echo   📄 .docx - Word文档
    echo   📊 .pptx - PowerPoint演示文稿  
    echo   📈 .xlsx - Excel电子表格
    echo   📋 .pdf  - PDF文档 ^(支持图像提取^)
    echo   📝 .txt  - 文本文件
    echo   🌐 .html - HTML文件
    echo   📊 .csv  - CSV数据文件
    echo.
    echo 💡 示例:
    echo   %0 "我的文档.docx"
    echo   %0 "报告.pdf"
    echo.
    pause
    exit /b 1
)

REM 检查输入文件是否存在
if not exist "%INPUT_FILE%" (
    echo ❌ 错误: 文件 "%INPUT_FILE%" 不存在
    echo 💡 请检查文件路径是否正确
    pause
    exit /b 1
)

REM 显示处理信息
echo 📁 输入文件: %INPUT_FILE%
for %%i in ("%INPUT_FILE%") do set FILE_EXT=%%~xi
echo 📋 文件类型: %FILE_EXT%

REM 步骤1: 检查Python环境
echo.
echo 🔍 步骤1: 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python环境
    echo.
    echo 💡 解决方案:
    echo   1. 安装Python 3.7或更高版本
    echo   2. 下载地址: https://www.python.org/downloads/
    echo   3. 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python版本: %PYTHON_VERSION%

REM 步骤2: 检查依赖管理器
echo.
echo 🔍 步骤2: 准备依赖管理器...
if not exist "%SCRIPT_DIR%dependency_manager.py" (
    echo ❌ 错误: 依赖管理器不存在
    echo 💡 请重新安装DocuGenius扩展
    pause
    exit /b 1
)

REM 步骤3: 智能依赖管理
echo.
echo 🔍 步骤3: 智能依赖检测和安装...
echo 📦 正在检查 %FILE_EXT% 文件所需的依赖包...

python "%SCRIPT_DIR%dependency_manager.py" --file "%INPUT_FILE%"
set DEP_EXIT_CODE=%ERRORLEVEL%

if %DEP_EXIT_CODE% neq 0 (
    echo.
    echo ❌ 依赖安装失败 ^(错误代码: %DEP_EXIT_CODE%^)
    echo.
    echo 💡 故障排除建议:
    echo   1. 检查网络连接是否正常
    echo   2. 尝试使用管理员权限运行
    echo   3. 检查防火墙和杀毒软件设置
    echo   4. 尝试手动安装: pip install --user python-docx python-pptx openpyxl PyMuPDF
    echo   5. 如果在企业网络，可能需要配置代理
    echo.
    echo 🔧 高级选项:
    echo   - 使用国内镜像: pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ^<package^>
    echo   - 离线安装: 下载whl文件后使用 pip install ^<file.whl^>
    echo.
    pause
    exit /b %DEP_EXIT_CODE%
)

REM 步骤4: 检查转换器
echo.
echo 🔍 步骤4: 准备文档转换器...
if not exist "%SCRIPT_DIR%converter.py" (
    echo ❌ 错误: 转换器不存在
    echo 💡 请重新安装DocuGenius扩展
    pause
    exit /b 1
)

REM 步骤5: 执行文档转换
echo.
echo 🔄 步骤5: 转换文档...
echo 📝 正在处理 "%INPUT_FILE%"...

python "%SCRIPT_DIR%converter.py" "%INPUT_FILE%" "%EXTRACT_IMAGES%"
set CONVERTER_EXIT_CODE=%ERRORLEVEL%

REM 显示结果
echo.
if %CONVERTER_EXIT_CODE% equ 0 (
    echo ✅ 转换成功完成！
    echo.
    echo 📄 输出信息:
    echo   - Markdown文件已生成
    echo   - 图像文件已提取 ^(如适用^)
    echo   - 文件保存在相同目录
    echo.
    echo 🎉 您可以在VSCode中查看生成的Markdown文件
) else (
    echo ❌ 转换失败 ^(错误代码: %CONVERTER_EXIT_CODE%^)
    echo.
    echo 💡 可能的解决方案:
    echo   1. 检查文件是否被其他程序占用
    echo   2. 确认文件格式正确且未损坏
    echo   3. 检查磁盘空间是否充足
    echo   4. 尝试使用其他文件进行测试
    echo   5. 查看上方的详细错误信息
    echo.
    echo 🔧 如果问题持续存在:
    echo   - 重启VSCode和Windows资源管理器
    echo   - 检查文件权限设置
    echo   - 联系技术支持并提供错误代码
)

echo.
echo 🏁 处理完成
echo ========================================

REM 在调试模式下暂停，让用户查看结果
if defined DOCUGENIUS_DEBUG (
    echo.
    echo 🐛 调试模式: 按任意键继续...
    pause >nul
)

exit /b %CONVERTER_EXIT_CODE%
