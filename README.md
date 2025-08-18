# DocuGenius | 文档精灵

Automatically convert Word, Excel, PowerPoint, and PDF files to Markdown in VS Code.

自动在VS Code中将Word、Excel、PowerPoint和PDF文件转换为Markdown格式。

## 📥 Download | 下载

[![Download Latest Release](https://img.shields.io/badge/Download-Latest%20Release-blue?style=for-the-badge&logo=github)](https://github.com/brucevanfdm/DocuGenius/releases/latest)

**🚀 Get DocuGenius**: [GitHub Releases](https://github.com/brucevanfdm/DocuGenius/releases/latest)

**获取DocuGenius**: [GitHub发布页面](https://github.com/brucevanfdm/DocuGenius/releases/latest)

## ✨ What It Does | 功能

- **📄 Converts Documents**: Word (.docx), Excel (.xlsx), PowerPoint (.pptx), PDF (.pdf) → Markdown
- **📁 Organizes Everything**: Creates a `DocuGenius/` folder with all converted files for easy searching
- **🔄 Stays Updated**: Automatically re-converts when you modify source files
- **🖼️ Advanced Image Extraction**: Automatically extracts images from PDF, DOCX, and PPTX files with smart organization
- **文档转换**：Word (.docx)、Excel (.xlsx)、PowerPoint (.pptx)、PDF (.pdf) → Markdown
- **统一管理**：创建 `DocuGenius/` 文件夹，便于搜索所有转换文件
- **自动更新**：源文件修改时自动重新转换
- **智能图片提取**：自动从 PDF、DOCX、PPTX 文件中提取图片并智能组织

## 🚀 Quick Start | 快速开始

### 1. Install | 安装

1. **Download**: Go to [GitHub Releases](https://github.com/brucevanfdm/DocuGenius/releases/latest) and download `docugenius-2.3.0.vsix`
2. **Install**: Open VS Code → Extensions (`Ctrl+Shift+X`) → "..." menu → "Install from VSIX..."
3. **Select**: Choose the downloaded `.vsix` file

1. **下载**：访问 [GitHub发布页面](https://github.com/brucevanfdm/DocuGenius/releases/latest) 下载 `docugenius-2.3.0.vsix`
2. **安装**：打开VS Code → 扩展(`Ctrl+Shift+X`) → "..."菜单 → "从VSIX安装..."
3. **选择**：选择下载的 `.vsix` 文件

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

### Image Extraction Settings | 图片提取设置
- **Image Min Size | 最小图片尺寸**: Minimum image size to extract (default: 50px)
- **Image Formats | 图片格式**: Supported formats (PNG, JPG, GIF, BMP)
- **Naming Convention | 命名规则**: How to name extracted images (page_based, sequential, descriptive)
- **Output Folder | 输出文件夹**: Folder name for images (default: "images")

## 🖼️ Image Extraction Features | 图片提取功能

DocuGenius automatically extracts images from your documents and organizes them intelligently:

DocuGenius 自动从文档中提取图片并智能组织：

### Supported Document Types | 支持的文档类型
- **PDF Files**: Uses PyMuPDF for high-quality extraction with fallback to pdfplumber
- **Word Documents (.docx)**: Extracts embedded images from document relationships
- **PowerPoint (.pptx)**: Extracts images from slides and shapes

**PDF 文件**：使用 PyMuPDF 进行高质量提取，回退到 pdfplumber
**Word 文档 (.docx)**：从文档关系中提取嵌入图片
**PowerPoint (.pptx)**：从幻灯片和形状中提取图片

### Smart Organization | 智能组织
```
DocuGenius/
├── document.md
└── images/
    └── document/                   # Organized by document name
        ├── page_1_img_1.png       # Page-based naming
        ├── page_1_img_2.jpg
        ├── page_2_img_1.png
        └── slide_3_img_1.gif
```

### Image Quality & Formats | 图片质量与格式
- **High Quality**: Maintains original image quality during extraction
- **Multiple Formats**: Supports PNG, JPEG, GIF, BMP formats
- **Smart Filtering**: Skips decorative images smaller than configured threshold
- **Collision-Free**: Automatic filename collision detection and resolution

**高质量**：提取过程中保持原始图片质量
**多种格式**：支持 PNG、JPEG、GIF、BMP 格式
**智能过滤**：跳过小于配置阈值的装饰性图片
**无冲突**：自动检测和解决文件名冲突

### Markdown Integration | Markdown 集成
Extracted images are automatically referenced in the generated Markdown:

提取的图片自动在生成的 Markdown 中引用：

```markdown
# Document Title

## Extracted Images

![Image from pdf (Page 1)](images/document/page_1_img_1.png)

![Image from pptx (Slide 2)](images/document/slide_2_img_1.jpg)

<!-- Images extracted: 5 images saved to DocuGenius/images/document -->
```
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

## 📦 Installation Requirements | 安装要求

### For Basic Document Conversion | 基本文档转换
- **Windows**: Python 3.6+ with basic libraries (auto-installed)
- **macOS/Linux**: Built-in binary (no additional requirements)

**Windows**：Python 3.6+ 及基础库（自动安装）
**macOS/Linux**：内置二进制文件（无额外要求）

### For Enhanced Image Extraction | 增强图片提取
For optimal image extraction quality, install these Python packages:

为获得最佳图片提取质量，请安装这些 Python 包：

```bash
# Recommended for best PDF image extraction
pip install PyMuPDF

# Alternative PDF libraries (fallback)
pip install pdfplumber PyPDF2

# Document libraries (auto-installed by CLI)
pip install python-docx python-pptx openpyxl
```

**Note**: The extension works without these packages but with limited image extraction capabilities.

**注意**：扩展在没有这些包的情况下也能工作，但图片提取功能有限。

## 🔧 Troubleshooting | 故障排除

**Conversion not working?** | **转换不工作？**

1. Check Output panel: `View → Output → DocuGenius`
2. Make sure Python is installed (Windows only)
3. Try manual conversion: Right-click file → "Convert to Markdown"
4. 检查输出面板：`查看 → 输出 → DocuGenius`
5. 确保已安装Python（仅Windows）
6. 尝试手动转换：右键文件 → "Convert to Markdown"

**Image extraction not working?** | **图片提取不工作？**

1. Install PyMuPDF for better PDF image extraction: `pip install PyMuPDF`
2. Check that image extraction is enabled in settings
3. Verify document contains extractable images (not just text)
4. 安装 PyMuPDF 以获得更好的 PDF 图片提取：`pip install PyMuPDF`
5. 检查设置中是否启用了图片提取
6. 验证文档包含可提取的图片（不仅仅是文本）
