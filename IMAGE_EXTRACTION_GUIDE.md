# DocuGenius 图片提取器使用指南

## 🎯 解决的问题

之前的版本将所有图片都放在markdown文件末尾的"Extracted Images"部分，现在提供了更灵活的选项，让您可以：

1. **手动控制图片位置** - 获取图片引用列表，自己决定在文档中的什么位置插入图片
2. **按页面组织图片** - 图片按原文档的页面/幻灯片分组显示
3. **传统方式** - 保持原有的"Extracted Images"部分（向后兼容）

## 📁 目录结构

```
项目根目录/
├── DocuGenius/                    # markdown文件存放目录
│   ├── document1.md               # 转换后的markdown文件
│   ├── document2.md
│   └── images/                    # 图片存放目录
│       ├── document1/
│       │   ├── page_1_img_1.png
│       │   └── page_2_img_1.jpg
│       └── document2/
│           ├── slide_1_img_1.png
│           └── slide_3_img_1.jpg
├── original_document.pdf          # 原始文档
└── other_files...
```

## 🚀 使用方法

### 命令行使用

```bash
# 基本用法 (使用simple模式)
python bin/win32/image_extractor.py document.pdf

# 指定输出目录和markdown目录
python bin/win32/image_extractor.py document.pdf custom_images DocuGenius

# 指定markdown生成模式
python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius simple
python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius grouped
python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius inline
```

### 编程接口使用

```python
from image_extractor import extract_images_from_document

# 提取图片并获取不同格式的输出
result = extract_images_from_document(
    'document.pdf',
    markdown_mode='simple'  # 或 'grouped', 'inline'
)

# 获取不同格式的图片引用
simple_refs = result['simple_image_list']           # 简单的图片引用列表
page_refs = result['image_references_by_page']      # 按页面分组的图片引用
traditional = result['markdown_references']         # 传统格式的markdown
```

## 📝 三种Markdown生成模式

### 1. Simple模式 (推荐) 🌟

**用途**: 手动控制图片在文档中的位置

**输出**:
```markdown
![Image from page 1](images/document/page_1_img_1.png)

![Image from page 1](images/document/page_1_img_2.jpg)

![Image from page 3](images/document/page_3_img_1.png)
```

**使用场景**: 
- 您想要将图片插入到文档的特定位置
- 需要在图片前后添加说明文字
- 希望完全控制文档的结构

### 2. Grouped模式

**用途**: 按页面/幻灯片组织图片

**输出**:
```markdown
### Page 1 Images

![Image from PDF](images/document/page_1_img_1.png)

![Image from PDF](images/document/page_1_img_2.jpg)

### Page 3 Images

![Image from PDF](images/document/page_3_img_1.png)
```

**使用场景**:
- 需要保持原文档的页面结构
- 图片较多，需要按页面分组管理
- 制作文档的图片索引

### 3. Inline模式 (传统)

**用途**: 所有图片放在文档末尾

**输出**:
```markdown
## Extracted Images

![Image from PDF (Page 1)](images/document/page_1_img_1.png)

![Image from PDF (Page 1)](images/document/page_1_img_2.jpg)

![Image from PDF (Page 3)](images/document/page_3_img_1.png)
```

**使用场景**:
- 图片作为附录或参考资料
- 向后兼容旧版本的行为
- 不需要手动调整图片位置

## 🔧 高级功能

### 按页面获取图片引用

```python
# 获取按页面分组的图片引用
page_refs = result['image_references_by_page']

# 使用示例
for page_num, image_refs in page_refs.items():
    print(f"第{page_num}页有{len(image_refs)}张图片:")
    for ref in image_refs:
        print(f"  {ref}")
```

### 获取简单图片列表

```python
# 获取所有图片的简单引用列表
simple_list = result['simple_image_list']

# 手动插入到markdown中
markdown_content = f"""
# 文档标题

这里是第一段内容...

{simple_list[0]}

这里是第二段内容...

{simple_list[1]}

继续其他内容...
"""
```

## 💡 最佳实践

1. **推荐使用Simple模式**: 提供最大的灵活性，可以精确控制图片位置
2. **相对路径**: 所有图片引用使用相对路径，确保跨平台兼容性
3. **目录结构**: 保持DocuGenius目录结构，便于管理和部署
4. **批量处理**: 可以编写脚本批量处理多个文档

## 🔄 从旧版本迁移

如果您之前使用的是旧版本（图片都在文档末尾），现在可以：

1. 继续使用`inline`模式保持原有行为
2. 或者切换到`simple`模式，获得更好的控制能力
3. 使用`grouped`模式按页面组织图片

所有模式都完全向后兼容！
