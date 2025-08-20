# DocuGenius v2.3.4 发布说明

## 📁 重要修复：统一图像目录结构

这是一个关键的修复版本，解决了用户反馈的重要问题：**提取的图片文件夹与引用的目录不对，同时生成assets和images文件夹，引用方式不正确**。

## 📦 下载信息

- **文件名**: `docugenius-2.3.4-unified-images.vsix`
- **文件大小**: 35.7MB
- **支持平台**: Windows 10+, macOS 10.14+
- **VS Code版本要求**: 1.74.0+

## 🚨 解决的核心问题

### 1. 目录结构不统一 ❌ → ✅

**修复前的问题**:
```
DocuGenius/
├── 生成式人工智能服务安全基本要求（GB_T 45654-2025）.md
├── 生成式人工智能服务安全基本要求（GB_T 45654-2025）_assets/  # 错误的assets目录
│   ├── page_1_img_1.png
│   └── page_2_img_1.png
└── images/                                                      # 同时存在的images目录
    └── 生成式人工智能服务安全基本要求（GB_T 45654-2025）/
        ├── page_1_img_1.png
        └── page_2_img_1.png
```

**修复后的结构**:
```
DocuGenius/
├── 生成式人工智能服务安全基本要求（GB_T 45654-2025）.md
└── images/                                                      # 统一的images目录
    └── 生成式人工智能服务安全基本要求（GB_T 45654-2025）/
        ├── page_1_img_1.png
        └── page_2_img_1.png
```

### 2. 引用路径错误 ❌ → ✅

**修复前的错误引用**:
```markdown
![Image from page 9](生成式人工智能服务安全基本要求（GB_T 45654-2025）_assets/page_9_img_1.png)
```

**修复后的正确引用**:
```markdown
![Image from page 9](images/生成式人工智能服务安全基本要求（GB_T 45654-2025）/page_9_img_1.png)
```

### 3. 前后端不一致 ❌ → ✅

**问题**: TypeScript前端代码使用`_assets`目录，Python后端使用`images`目录
**解决**: 统一使用`images`目录结构，确保前后端完全一致

## 🔧 技术修复详情

### TypeScript代码修复
```typescript
// 修复前
assetsDir = path.join(markdownDir, `${originalBaseName}_assets`);

// 修复后
imagesDir = path.join(markdownDir, 'images', originalBaseName);
```

### 图像引用处理修复
```typescript
// 修复前
if (!imagePath.startsWith(`${originalBaseName}_assets/`)) {
    const newImagePath = `${originalBaseName}_assets/${imageName}`;
}

// 修复后
if (!imagePath.startsWith(`images/${originalBaseName}/`)) {
    const newImagePath = `images/${originalBaseName}/${imageName}`;
}
```

### 清理功能增强
- 自动清理遗留的`_assets`文件夹
- 支持新旧版本的平滑迁移
- 删除文档时同时清理对应的图像目录

## 📊 修复验证

### 测试场景
1. **中文文档名**: `生成式人工智能服务安全基本要求（GB_T 45654-2025）.pdf`
2. **多页图像**: 第1页和第2页各包含一个图像
3. **路径一致性**: 验证存储路径和引用路径完全匹配

### 测试结果
```
✅ Extraction successful
   Images extracted: 2
   Output directory: DocuGenius/images/生成式人工智能服务安全基本要求（GB_T 45654-2025）

✅ Correct directory structure verified
   Image files found: 2
   - page_1_img_1.png
   - page_2_img_1.png

✅ Image references in markdown: 2
   📝 ![Image from page 1 (200x100)](images/生成式人工智能服务安全基本要求（GB_T 45654-2025）/page_1_img_1.png)
   📝 ![Image from page 2 (150x150)](images/生成式人工智能服务安全基本要求（GB_T 45654-2025）/page_2_img_1.png)

✅ No legacy assets directories found
✅ All relative paths correct and files exist
```

## 🎯 用户体验改进

### 1. 一致的目录结构
- 所有图像统一保存到`images`目录
- 不再产生混乱的多个目录
- 便于用户管理和查找图像文件

### 2. 正确的图像显示
- 图像引用路径完全正确
- 在VS Code markdown预览中正常显示
- 支持各种文档名（包括中文、特殊字符）

### 3. 自动清理功能
- 删除文档时自动清理对应图像
- 清理遗留的旧版本`_assets`文件夹
- 保持工作目录整洁

## 🔄 升级指南

### 从v2.3.3升级
1. 安装新版本
2. 重新转换之前有问题的文档
3. 旧的`_assets`文件夹会自动清理

### 验证修复效果
1. 转换一个包含图像的PDF文档
2. 检查生成的目录结构：
   ```
   DocuGenius/
   ├── 文档名.md
   └── images/
       └── 文档名/
           └── *.png
   ```
3. 在VS Code中预览markdown，确认图像正确显示

## 🛠️ 技术细节

### 目录结构标准化
- **存储路径**: `DocuGenius/images/文档名/`
- **引用路径**: `images/文档名/图像文件名`
- **相对路径**: 从markdown文件到图像的正确相对路径

### 跨平台一致性
- Mac和Windows版本使用相同的目录结构
- 二进制文件和脚本版本行为一致
- 支持各种文件名编码（UTF-8、中文等）

### 向后兼容性
- 自动检测和清理旧版本的`_assets`目录
- 支持从旧版本平滑升级
- 不影响已有的正确格式文档

## 📈 性能影响

- **存储效率**: 避免重复存储图像文件
- **查找速度**: 统一目录结构便于快速定位
- **清理效率**: 自动清理减少手动维护工作

## 🐛 已修复的具体问题

- ✅ 同时生成`images`和`assets`文件夹
- ✅ 图像引用使用错误的`_assets`路径
- ✅ TypeScript和Python代码不一致
- ✅ 中文文档名的路径处理问题
- ✅ 删除文档时图像目录未清理
- ✅ 图像在markdown预览中无法显示

## 🎯 推荐设置

```json
{
  "documentConverter.extractImages": true,
  "documentConverter.imageMinSize": 50,
  "documentConverter.organizeInSubdirectory": true,
  "documentConverter.markdownSubdirectoryName": "DocuGenius"
}
```

## 📞 支持

如果仍然遇到图像目录问题：
1. 检查`DocuGenius/images/`目录结构
2. 验证markdown中的图像引用路径
3. 重新转换文档以应用新的目录结构

## 🙏 致谢

感谢用户详细的问题反馈，特别是指出了目录结构不统一和引用路径错误的具体问题。这帮助我们实现了完全统一的图像管理系统。

---

**DocuGenius团队**  
2025年8月21日

**重要提醒**: 这是一个重要的修复版本，解决了图像目录和引用的核心问题，强烈建议所有用户升级。
