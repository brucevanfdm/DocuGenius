# DocuGenius | 文档精灵

Automatically convert Word, Excel, PowerPoint, and PDF files to Markdown in VS Code.

自动在VS Code中将Word、Excel、PowerPoint和PDF文件转换为Markdown格式。

## 📥 Download | 下载

**🚀 Latest Release | 最新版本**: [DocuGenius v2.3.0](https://github.com/brucevanfdm/project-plugin/releases/latest)

[![Download VSIX](https://img.shields.io/badge/Download-VSIX%20Package-blue?style=for-the-badge&logo=visual-studio-code)](https://github.com/brucevanfdm/project-plugin/releases/download/v2.3.0/docugenius-2.3.0.vsix)

**直接下载**: [docugenius-2.3.0.vsix](https://github.com/brucevanfdm/project-plugin/releases/download/v2.3.0/docugenius-2.3.0.vsix)

## ✨ What It Does | 功能

- **📄 Converts Documents**: Word (.docx), Excel (.xlsx), PowerPoint (.pptx), PDF (.pdf) → Markdown
- **📁 Organizes Everything**: Creates a `DocuGenius/` folder with all converted files for easy searching
- **🔄 Stays Updated**: Automatically re-converts when you modify source files
- **🖼️ Handles Images**: Extracts images from documents into organized asset folders
- **文档转换**：Word (.docx)、Excel (.xlsx)、PowerPoint (.pptx)、PDF (.pdf) → Markdown
- **统一管理**：创建 `DocuGenius/` 文件夹，便于搜索所有转换文件
- **自动更新**：源文件修改时自动重新转换
- **图片处理**：提取文档中的图片到整理好的资源文件夹

## 🚀 Quick Start | 快速开始

### 1. Install | 安装

**Option 1: Download from GitHub | 从GitHub下载**
1. Download `docugenius-2.3.0.vsix` from this repository
2. Open VS Code → Extensions (`Ctrl+Shift+X`) → "..." menu → "Install from VSIX..."
3. Select the downloaded file

1. 从此仓库下载 `docugenius-2.3.0.vsix` 文件
2. 打开VS Code → 扩展(`Ctrl+Shift+X`) → "..."菜单 → "从VSIX安装..."
3. 选择下载的文件

**Option 2: VS Code Marketplace | VS Code市场**
- Search for "DocuGenius" in VS Code Extensions
- 在VS Code扩展中搜索"DocuGenius"

### 2. Setup | 设置

**macOS**: Ready to use! | 开箱即用！

**Windows**: Python libraries are **automatically installed** when needed. Just make sure you have Python installed.

**Windows**: Python库会在需要时**自动安装**。只需确保已安装Python。

If you don't have Python: Download from [python.org](https://python.org)

如果没有Python：从 [python.org](https://python.org) 下载

### 3. Start Using | 开始使用

**First Time**: Open a folder with documents (.docx, .xlsx, .pptx, .pdf) → Extension asks to enable → Click "Enable"

**首次使用**：打开包含文档的文件夹 → 扩展询问是否启用 → 点击"启用"

**Already Used**: If you see a `DocuGenius/` folder, it's already enabled!

**已使用过**：如果看到 `DocuGenius/` 文件夹，说明已经启用！

## 📖 How to Use | 使用方法

### Manual Conversion | 手动转换 (Recommended | 推荐)

- **Single file**: Right-click file → "Convert to Markdown"
- **Whole folder**: Right-click folder → "Process All Files in Folder"
- **单个文件**：右键文件 → "Convert to Markdown"
- **整个文件夹**：右键文件夹 → "Process All Files in Folder"

### Automatic Conversion | 自动转换 (Optional | 可选)

To enable automatic conversion: Go to Settings → Search "DocuGenius" → Turn on "Auto Convert"

要启用自动转换：进入设置 → 搜索"DocuGenius" → 开启"Auto Convert"

When enabled, new document files are automatically converted to the `DocuGenius/` folder

启用后，新文档文件会自动转换到 `DocuGenius/` 文件夹

## 📁 What You Get | 输出结果

Your project stays organized with a dedicated knowledge base:

项目保持整洁，拥有专门的知识库：

```
your-project/
├── document.docx                    # Your original files | 原始文件
├── presentation.pptx
├── notes.txt
└── DocuGenius/                     # Searchable knowledge base | 可搜索的知识库
    ├── document.md                 # Converted documents | 转换后的文档
    ├── presentation.md
    ├── notes.txt                   # Text files copied | 文本文件复制
    ├── document_assets/            # Extracted images | 提取的图片
    └── presentation_assets/
```

**Supported Files | 支持的文件**:

- **Documents**: `.docx`, `.xlsx`, `.pptx`, `.pdf` → Converted to Markdown
- **Text Files**: `.txt`, `.md`, `.json`, `.csv`, `.xml` → Copied for unified search

**文档**：`.docx`、`.xlsx`、`.pptx`、`.pdf` → 转换为Markdown
**文本文件**：`.txt`、`.md`、`.json`、`.csv`、`.xml` → 复制以便统一搜索

## ⚙️ Settings | 设置

Access via `Ctrl+,` (Windows) or `Cmd+,` (Mac), then search "DocuGenius":

通过 `Ctrl+,` (Windows) 或 `Cmd+,` (Mac) 访问，然后搜索"DocuGenius"：

### Core Settings | 核心设置
- **Auto Convert | 自动转换**: Enable automatic conversion of new files (default: off)
- **Overwrite Existing | 覆盖现有**: Update converted files when source changes (default: on)
- **Extract Images | 提取图片**: Save images from documents (default: on)
- **Folder Name | 文件夹名**: Change output folder name (default: "DocuGenius")

### Advanced Settings | 高级设置
- **Supported Extensions | 支持扩展**: File types to monitor (default: .docx, .xlsx, .pptx, .pdf)
- **Copy Text Files | 复制文本**: Include text files in knowledge base (default: off)
- **Show Notifications | 显示通知**: Popup when conversion completes (default: on)
- **Project Config | 项目配置**: Create .docugenius.json files (default: off)
- **Batch Behavior | 批量行为**: How to handle multiple files (default: ask once)

## 📊 Status Bar | 状态栏

Watch the bottom status bar for conversion progress:

观察底部状态栏的转换进度：

- **Ready** | **就绪**: Monitoring for new files | 监控新文件
- **Converting** | **转换中**: Processing a file | 正在处理文件
- **Done** | **完成**: Conversion successful | 转换成功
- **Error** | **错误**: Something went wrong | 出现错误

Click the status to see detailed logs | 点击状态查看详细日志

## 🔧 Troubleshooting | 故障排除

**Conversion not working?** | **转换不工作？**

1. Check Output panel: `View → Output → DocuGenius`
2. Make sure Python is installed (Windows only)
3. Try manual conversion: Right-click file → "Convert to Markdown"
4. 检查输出面板：`查看 → 输出 → DocuGenius`
5. 确保已安装Python（仅Windows）
6. 尝试手动转换：右键文件 → "Convert to Markdown"
