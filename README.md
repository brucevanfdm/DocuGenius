# DocuGenius | 文档精灵

A VS Code extension that automatically converts Word, Excel, PowerPoint, and PDF files to Markdown with built-in conversion engine.

一个VS Code扩展，内置转换引擎，自动将Word、Excel、PowerPoint和PDF文件转换为Markdown格式。

## Features | 功能特性

- **🚀 Built-in Conversion Engine | 内置转换引擎**: Uses professional Python libraries for accurate document conversion | 使用专业Python库进行精确文档转换
- **📄 Full Document Support | 完整文档支持**:
  - **Word**: Complete text extraction with heading styles and tables (python-docx) | 完整文本提取，支持标题样式和表格
  - **Excel**: Multi-sheet support with proper table formatting (openpyxl) | 多工作表支持，正确的表格格式
  - **PowerPoint**: Slide-by-slide text extraction (python-pptx) | 逐幻灯片文本提取
  - **PDF**: Page-by-page text extraction (PyPDF2) | 逐页文本提取
- **📁 Unified Knowledge Base | 统一知识库**: All files organized in `kb/` directory for unified search | 所有文件统一组织在`kb/`目录中便于搜索
- **🔄 Manual Conversion | 手动转换**: Right-click any supported file to manually convert it | 右键点击任何支持的文件进行手动转换
- **🔄 Complete Lifecycle Management | 完整生命周期管理**: Automatically cleans up when source files are deleted | 源文件删除时自动清理
- **📊 Smart Processing | 智能处理**: Converts documents and copies text files | 转换文档文件并复制文本文件
- **🔄 Automatic Updates | 自动更新**: Monitors source files and updates processed versions when changed | 监控源文件变化并自动更新
- **🖼️ Image Handling | 图片处理**: Extracts and organizes images in dedicated asset folders | 提取并整理图片到专用资源文件夹
- **⚙️ Highly Configurable | 高度可配置**: Customize file types, output organization, and conversion behavior | 自定义文件类型、输出组织和转换行为
- **📱 User-Friendly | 用户友好**: Progress indicators, status bar updates, and detailed logging | 进度指示器、状态栏更新和详细日志

## Requirements | 系统要求

### Built-in Binaries | 内置二进制文件

The extension includes pre-built conversion binaries for:
- **macOS**: Native binary with all required libraries bundled | 包含所有必需库的原生二进制文件
- **Windows**: Batch script that uses system Python | 使用系统Python的批处理脚本

### For Windows Users | Windows用户

For full document conversion functionality on Windows, you may need to install Python libraries:

```bash
pip install python-docx python-pptx openpyxl PyPDF2
```

The extension will work with basic file types (text, JSON, CSV, XML) without additional dependencies.

扩展在没有额外依赖的情况下可以处理基本文件类型（文本、JSON、CSV、XML）。

## Installation | 安装

1. Install the extension from the VS Code marketplace | 从VS Code市场安装扩展
2. The extension will activate automatically when VS Code starts | 扩展将在VS Code启动时自动激活

## Usage | 使用方法

### 🎯 Project-Level Activation | 项目级别激活

**智能启用机制**: DocuGenius 采用项目级别的智能激活，避免对不需要文档转换的项目造成干扰。

**Smart Activation**: DocuGenius uses project-level intelligent activation to avoid interfering with projects that don't need document conversion.

#### 首次使用 | First Time Usage

1. **打开包含文档的文件夹** | **Open a folder containing documents**
   - 当您在 Trae 中打开包含 `.docx`、`.pptx`、`.xlsx`、`.pdf` 等文档的文件夹时
   - When you open a folder containing `.docx`, `.pptx`, `.xlsx`, `.pdf` documents in Trae

2. **智能检测与提示** | **Smart Detection & Prompt**
   - 扩展会检测到文档文件，并询问是否为此项目启用 DocuGenius
   - The extension detects document files and asks if you want to enable DocuGenius for this project
   - 选择"启用"后，将创建 `.docugenius.json` 配置文件并开始自动转换
   - After selecting "Enable", a `.docugenius.json` config file is created and auto-conversion begins

3. **自动识别已使用项目** | **Auto-Recognition of Used Projects**
   - 如果项目中已存在 `kb` 文件夹，说明之前使用过，会自动启用
   - If a `kb` folder already exists, indicating previous usage, it will be automatically enabled

#### 项目管理命令 | Project Management Commands

通过命令面板 (`Cmd/Ctrl + Shift + P`) 访问：| Access via Command Palette (`Cmd/Ctrl + Shift + P`):

- **`DocuGenius: Enable for Current Project`** - 为当前项目启用 | Enable for current project
- **`DocuGenius: Disable for Current Project`** - 为当前项目禁用 | Disable for current project  
- **`DocuGenius: Show Project Status`** - 查看项目状态 | View project status

#### 项目配置文件 | Project Configuration File

每个启用的项目会包含 `.docugenius.json` 配置文件：| Each enabled project contains a `.docugenius.json` config file:

```json
{
  "enabled": true,
  "autoConvert": true,
  "markdownSubdirectoryName": "kb",
  "supportedExtensions": [".docx", ".xlsx", ".pptx", ".pdf"],
  "lastActivated": "2024-01-01T00:00:00.000Z"
}
```

### Automatic Conversion | 自动转换

启用后，扩展会自动监控工作区中的文档文件变化。当您添加支持的文件（通过复制、移动或创建）时，它将自动转换为Markdown。

Once enabled, the extension automatically monitors document file changes in your workspace. When you add a supported file (by copying, moving, or creating), it will be automatically converted to Markdown.

### Manual Conversion | 手动转换

You can also manually convert files | 您也可以手动转换文件：

1. Right-click on a supported file in the Explorer | 在资源管理器中右键点击支持的文件
2. Select "Convert to Markdown" from the context menu | 从上下文菜单中选择"Convert to Markdown"
   - This will force conversion even if the file was already converted | 即使文件已经转换过也会强制转换
   - Useful when you've modified the original file and want to update the markdown version | 当您修改了原文件并想更新markdown版本时很有用

Or convert entire folders | 或转换整个文件夹：

1. Right-click on a folder in the Explorer | 在资源管理器中右键点击文件夹
2. Select "Process All Files in Folder" from the context menu | 从上下文菜单中选择"Process All Files in Folder"

### Output Format | 输出格式

**📁 Unified Knowledge Base | 统一知识库**: All files are processed into a `kb/` subdirectory for unified search and management | 所有文件都被处理到`kb/`子目录中以便统一搜索和管理：

```
your-project/
├── document.docx                    # Source file (for editing) | 源文件（用于编辑）
├── presentation.pptx               # Source file (for editing) | 源文件（用于编辑）
├── notes.txt                       # Source file (for editing) | 源文件（用于编辑）
├── config.json                     # Source file (for editing) | 源文件（用于编辑）
└── kb/                             # Knowledge base (for VS Code search) | 知识库（用于VS Code搜索）
    ├── document.md                 # Converted from docx | 从docx转换而来
    ├── presentation.md             # Converted from pptx | 从pptx转换而来
    ├── notes.txt                   # Copied from source | 从源文件复制
    ├── config.json                 # Copied from source | 从源文件复制
    ├── document_assets/            # Images from document.docx | 来自document.docx的图片
    └── presentation_assets/        # Images from presentation.pptx | 来自presentation.pptx的图片
```

**🔄 Complete Lifecycle Management | 完整生命周期管理**:
- ✅ **File Added | 文件添加**: Automatically converts/copies to `kb/` directory | 自动转换/复制到`kb/`目录
- ✅ **File Updated | 文件更新**: Automatically updates the processed version | 自动更新处理后的版本
- ✅ **File Deleted | 文件删除**: Automatically cleans up processed files and assets | 自动清理处理后的文件和资源

**📊 Smart Processing | 智能处理**:

**Document Conversion | 文档转换** (→ `.md` files):
- **📄 Word Documents**: `.docx` - Full text extraction with heading styles, paragraphs, and tables | 完整文本提取，支持标题样式、段落和表格
- **📊 Excel Spreadsheets**: `.xlsx`, `.xls` - Multi-sheet conversion to markdown tables | 多工作表转换为markdown表格
- **📽️ PowerPoint Presentations**: `.pptx` - Slide-by-slide text extraction | 逐幻灯片文本提取
- **📑 PDF Documents**: `.pdf` - Page-by-page text extraction | 逐页文本提取

**File Copying | 文件复制** (→ same format):
- **📝 Text Files**: `.txt`, `.md`, `.markdown` - Direct copy | 直接复制
- **🔧 Data Files**: `.json`, `.csv`, `.xml`, `.html`, `.yaml`, `.sql` - Formatted display | 格式化显示
- **⚙️ Config Files**: `.toml`, `.ini`, `.cfg`, `.conf` - Direct copy | 直接复制

## Configuration | 配置选项

The extension provides several configuration options | 扩展提供多个配置选项：

### `markitdown.autoConvert` | 自动转换
- **Type | 类型**: `boolean`
- **Default | 默认值**: `true`
- **Description | 描述**: Enable automatic conversion of supported files | 启用支持文件的自动转换

### `markitdown.overwriteExisting` | 覆盖现有文件
- **Type | 类型**: `boolean`
- **Default | 默认值**: `true`
- **Description | 描述**: Overwrite existing .md files if source file is newer | 如果源文件更新则覆盖现有的.md文件

### `markitdown.extractImages` | 提取图片
- **Type | 类型**: `boolean`
- **Default | 默认值**: `true`
- **Description | 描述**: Extract images from documents to separate assets folder | 将文档中的图片提取到单独的资源文件夹

### `markitdown.supportedExtensions` | 支持的扩展名
- **Type | 类型**: `array`
- **Default | 默认值**: `[".docx", ".xlsx", ".pptx", ".pdf"]`
- **Description | 描述**: File extensions to monitor for automatic conversion | 监控自动转换的文件扩展名

### `markitdown.organizeInSubdirectory` | 在子目录中组织
- **Type | 类型**: `boolean`
- **Default | 默认值**: `true`
- **Description | 描述**: Organize converted Markdown files in a subdirectory to separate them from source files | 将转换的Markdown文件组织在子目录中以与源文件分离

### `markitdown.markdownSubdirectoryName` | Markdown子目录名称
- **Type | 类型**: `string`
- **Default | 默认值**: `"kb"`
- **Description | 描述**: Name of the subdirectory where converted Markdown files will be stored | 存储转换的Markdown文件的子目录名称

## Status Bar | 状态栏

The extension shows its status in the VS Code status bar | 扩展在VS Code状态栏中显示其状态：
- **Ready | 就绪**: Extension is active and monitoring | 扩展处于活动状态并正在监控
- **Converting | 转换中**: Currently converting a file | 当前正在转换文件
- **✓ Converted | ✓ 已转换**: Recently completed a conversion | 最近完成了转换
- **✗ Failed | ✗ 失败**: Recent conversion failed | 最近的转换失败

Click the status bar item to view detailed logs in the Output panel | 点击状态栏项目在输出面板中查看详细日志。

## Troubleshooting | 故障排除

### Conversion Fails | 转换失败

Check the Output panel (View → Output → Markitdown Auto Converter) for detailed error messages.

检查输出面板（查看 → 输出 → Markitdown Auto Converter）以获取详细的错误消息。

## Known Limitations | 已知限制

- Large files may take some time to convert | 大文件可能需要一些时间来转换
- Complex document formatting may not be perfectly preserved in Markdown | 复杂的文档格式可能无法在Markdown中完美保留