# DocuGenius 智能图片提取指南

## 🎯 问题解决

**之前的问题**: 所有图片都被统一放到markdown文件末尾，标题是"Extracted Images"

**现在的解决方案**: 图片根据它们在原文档中的位置（页码、段落）自动插入到markdown内容的相应位置

## 🚀 新功能: 智能内容提取

### 核心特性

- ✅ **位置感知**: 图片根据原文档位置智能插入
- ✅ **结构保持**: 保持原文档的页面/段落结构
- ✅ **自动化**: 一键生成完整的markdown文档
- ✅ **多格式支持**: PDF、DOCX、PPTX

## 📊 模式对比

### 传统模式 (images_only)
```markdown
# 文档标题
这里是文档内容...

## Extracted Images
![Image from PDF (Page 1)](images/document/page_1_img_1.png)
![Image from PDF (Page 2)](images/document/page_2_img_1.png)
```

### 智能模式 (full_content) 🌟
```markdown
## Page 1
这里是第一页的内容...

### Images from this page
![Image from page 1](images/document/page_1_img_1.png)

---

## Page 2
这里是第二页的内容...

### Images from this page
![Image from page 2](images/document/page_2_img_1.png)
```

## 💻 使用方法

### 命令行使用

```bash
# 智能模式 - 完整文档内容提取
python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius full_content

# 传统模式 - 只提取图片
python bin/win32/image_extractor.py document.pdf DocuGenius/images DocuGenius images_only
```

### Python API使用

```python
from image_extractor import extract_document_with_images

# 智能模式 - 推荐使用
result = extract_document_with_images('document.pdf')

if result['success']:
    # 获取完整的markdown内容，图片已在正确位置
    markdown_content = result['markdown_content']
    
    # 保存到文件
    with open('DocuGenius/document.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ 成功提取 {result['images_count']} 张图片")
    print("📍 图片已按原文档位置插入")
else:
    print(f"❌ 提取失败: {result['error']}")
```

## 📄 不同格式的处理方式

### PDF文件
- **文本提取**: 按页面提取文本内容
- **图片插入**: 每页内容后插入该页的所有图片
- **结构**: `## Page N` → 文本内容 → `### Images from this page` → 图片

### DOCX文件
- **文本提取**: 按段落提取文本内容
- **图片插入**: 图片在原始段落位置插入
- **结构**: 段落文本 → 图片 → 下一段落文本 → 图片

### PPTX文件
- **文本提取**: 按幻灯片提取文本内容
- **图片插入**: 每张幻灯片内容后插入该幻灯片的图片
- **结构**: `## Slide N` → 文本内容 → 图片

## 🔧 API返回结果

### 智能模式返回结果
```json
{
  "success": true,
  "document": "path/to/document.pdf",
  "output_dir": "DocuGenius/images/document",
  "images_count": 5,
  "images": [...],
  "markdown_content": "完整的markdown内容，图片已在正确位置"
}
```

### 传统模式返回结果
```json
{
  "success": true,
  "images": [...],
  "markdown_references": "## Extracted Images\n...",
  "simple_image_list": ["![Image](path1)", "![Image](path2)"],
  "image_references_by_page": {1: ["![Image](path1)"], 2: ["![Image](path2)"]}
}
```

## 🎯 使用场景建议

### 推荐使用智能模式的情况
- ✅ 需要完整转换文档为markdown
- ✅ 希望保持原文档结构
- ✅ 图片需要在正确位置显示
- ✅ 自动化处理大量文档

### 使用传统模式的情况
- 🔸 需要手动控制图片位置
- 🔸 只需要提取图片，不需要文本内容
- 🔸 需要自定义markdown结构

## 📁 目录结构

```
项目根目录/
├── DocuGenius/                    # markdown文件存放目录
│   ├── document1.md               # 智能模式生成的完整文档
│   ├── document2.md
│   └── images/                    # 图片存放目录
│       ├── document1/
│       │   ├── page_1_img_1.png
│       │   └── page_2_img_1.jpg
│       └── document2/
│           └── slide_1_img_1.png
├── original_document.pdf          # 原始文档
└── other_files...
```

## 🔄 迁移指南

### 从旧版本迁移
1. **保持兼容**: 旧的API调用仍然有效
2. **新功能**: 使用 `extract_document_with_images()` 获得智能提取
3. **命令行**: 添加 `full_content` 参数启用智能模式

### 批量处理脚本示例
```python
import os
from pathlib import Path
from image_extractor import extract_document_with_images

def batch_convert_documents(input_dir, output_dir):
    """批量转换文档"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    for doc_file in input_path.glob("*.pdf"):
        print(f"处理: {doc_file.name}")
        
        result = extract_document_with_images(
            str(doc_file),
            str(output_path / "images"),
            str(output_path)
        )
        
        if result['success']:
            # 保存markdown文件
            md_file = output_path / f"{doc_file.stem}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(result['markdown_content'])
            
            print(f"✅ 成功: {result['images_count']} 张图片")
        else:
            print(f"❌ 失败: {result['error']}")

# 使用示例
batch_convert_documents("./documents", "./DocuGenius")
```

## 🎉 总结

现在您的问题已经完全解决了！

- ❌ **之前**: 图片都在文档末尾的"Extracted Images"部分
- ✅ **现在**: 图片根据原文档位置智能插入到相应位置
- 🚀 **优势**: 一键生成完整、结构化的markdown文档
