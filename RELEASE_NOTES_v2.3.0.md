# DocuGenius v2.3.0 Release Notes | 发布说明

## 🎯 Major Feature: Project-Level Activation | 主要功能：项目级别激活

### 🚀 What's New | 新功能

#### Smart Project Activation | 智能项目激活

DocuGenius 现在采用**项目级别的智能激活机制**，完美平衡了便利性和非侵入性：

DocuGenius now uses **project-level intelligent activation** that perfectly balances convenience and non-intrusiveness:

- **🔍 智能检测** | **Smart Detection**: 自动检测项目中的文档文件，仅在需要时提示启用
- **📁 项目隔离** | **Project Isolation**: 每个项目独立配置，不影响其他项目
- **🎛️ 用户控制** | **User Control**: 用户完全控制哪些项目启用文档转换功能

#### Key Benefits | 主要优势

1. **避免干扰** | **Avoid Interference**
   - 不再对所有项目自动启用，避免不必要的文件监听和转换
   - No longer auto-enables for all projects, avoiding unnecessary file watching and conversion

2. **智能提示** | **Smart Prompts**
   - 仅在检测到文档文件时才询问是否启用
   - Only prompts when document files are detected

3. **自动识别** | **Auto Recognition**
   - 已使用过的项目（存在 `kb` 文件夹）自动启用
   - Previously used projects (with existing `kb` folder) are automatically enabled

### 🛠️ New Features | 新功能

#### Project Configuration File | 项目配置文件

每个启用的项目现在包含 `.docugenius.json` 配置文件：

Each enabled project now contains a `.docugenius.json` configuration file:

```json
{
  "enabled": true,
  "autoConvert": true,
  "markdownSubdirectoryName": "kb",
  "supportedExtensions": [".docx", ".xlsx", ".pptx", ".pdf"],
  "lastActivated": "2024-01-01T00:00:00.000Z"
}
```

#### New Commands | 新命令

通过命令面板访问的新命令：| New commands accessible via Command Palette:

- **`DocuGenius: Enable for Current Project`** - 为当前项目启用
- **`DocuGenius: Disable for Current Project`** - 为当前项目禁用
- **`DocuGenius: Show Project Status`** - 查看项目状态和配置

#### Enhanced Configuration Management | 增强的配置管理

- **项目级配置优先级** | **Project-level config priority**: 项目配置覆盖全局设置
- **智能配置合并** | **Smart config merging**: 自动合并默认配置和项目配置

### 🔄 Migration Guide | 迁移指南

#### For Existing Users | 现有用户

如果您之前使用过 DocuGenius：

If you've used DocuGenius before:

1. **自动迁移** | **Automatic Migration**: 
   - 存在 `kb` 文件夹的项目会自动启用
   - Projects with existing `kb` folders will be automatically enabled

2. **手动启用** | **Manual Enabling**:
   - 对于新项目，使用命令 `DocuGenius: Enable for Current Project`
   - For new projects, use the command `DocuGenius: Enable for Current Project`

#### For New Users | 新用户

1. 打开包含文档的文件夹 | Open a folder containing documents
2. 扩展会自动检测并询问是否启用 | Extension will auto-detect and ask if you want to enable
3. 选择"启用"开始使用 | Select "Enable" to start using

### 🐛 Bug Fixes | 错误修复

- 修复了文件监听器可能导致的无限循环问题 | Fixed potential infinite loop issues with file watchers
- 改进了配置变更时的监听器重新初始化逻辑 | Improved watcher reinitialization logic on configuration changes
- 优化了启动时的性能，避免不必要的资源消耗 | Optimized startup performance, avoiding unnecessary resource consumption

### 🔧 Technical Improvements | 技术改进

- **新增 ProjectManager 类** | **New ProjectManager class**: 专门管理项目级别的配置和状态
- **重构配置管理** | **Refactored configuration management**: 支持项目级配置优先级
- **改进的文件监听逻辑** | **Improved file watching logic**: 仅在项目启用时创建监听器

### 📝 Breaking Changes | 破坏性变更

**无破坏性变更** | **No Breaking Changes**: 此版本完全向后兼容，现有用户的工作流程不会受到影响。

This version is fully backward compatible, and existing users' workflows will not be affected.

### 🎉 What's Next | 下一步计划

- 支持工作区级别的批量项目管理 | Support for workspace-level batch project management
- 更丰富的项目配置选项 | More rich project configuration options
- 项目模板和预设配置 | Project templates and preset configurations

---

## Installation | 安装

更新到最新版本：| Update to the latest version:

1. 在 VS Code 中打开扩展面板 | Open Extensions panel in VS Code
2. 搜索 "DocuGenius" | Search for "DocuGenius"
3. 点击"更新"按钮 | Click the "Update" button

或通过命令行：| Or via command line:

```bash
code --install-extension brucevan.docugenius
```

## Feedback | 反馈

如有问题或建议，请访问：| For issues or suggestions, please visit:

- GitHub Issues: https://github.com/brucevan/docugenius/issues
- Email: brucevanfdm@gmail.com

感谢您使用 DocuGenius！| Thank you for using DocuGenius!