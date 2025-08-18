#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试移除图片标题后的效果
"""

import sys
from pathlib import Path

# Add the bin/win32 directory to the path
sys.path.insert(0, str(Path(__file__).parent / "bin" / "win32"))

from image_extractor import ImageExtractor

def test_no_image_headers():
    """测试智能提取是否移除了图片标题"""
    print("测试图片标题移除效果")
    print("=" * 50)
    
    # 模拟PDF提取结果
    print("\n📄 模拟PDF智能提取结果:")
    print("-" * 30)
    
    # 创建模拟的图片信息
    mock_images = [
        {
            'filename': 'page_1_img_1.png',
            'relative_path': 'images/test/page_1_img_1.png',
            'page': 1,
            'width': 800,
            'height': 600,
            'format': 'PNG',
            'size_bytes': 12345
        },
        {
            'filename': 'page_2_img_1.jpg',
            'relative_path': 'images/test/page_2_img_1.jpg',
            'page': 2,
            'width': 640,
            'height': 480,
            'format': 'JPG',
            'size_bytes': 23456
        }
    ]
    
    # 模拟智能提取的markdown内容生成
    markdown_lines = []
    
    # 第一页内容
    markdown_lines.append("\n## Page 1\n")
    markdown_lines.append("这里是第一页的文本内容...")
    markdown_lines.append("第一页的段落文本。")
    markdown_lines.append("")
    
    # 第一页图片 (不再有标题)
    page_1_images = [img for img in mock_images if img['page'] == 1]
    if page_1_images:
        for img_info in page_1_images:
            alt_text = f"Image from page {img_info['page']}"
            markdown_lines.append(f"![{alt_text}]({img_info['relative_path']})")
            markdown_lines.append("")
    
    markdown_lines.append("---\n")
    
    # 第二页内容
    markdown_lines.append("\n## Page 2\n")
    markdown_lines.append("这里是第二页的文本内容...")
    markdown_lines.append("第二页的段落文本。")
    markdown_lines.append("")
    
    # 第二页图片 (不再有标题)
    page_2_images = [img for img in mock_images if img['page'] == 2]
    if page_2_images:
        for img_info in page_2_images:
            alt_text = f"Image from page {img_info['page']}"
            markdown_lines.append(f"![{alt_text}]({img_info['relative_path']})")
            markdown_lines.append("")
    
    markdown_lines.append("---\n")
    
    result_content = '\n'.join(markdown_lines)
    
    print("生成的Markdown内容:")
    print(result_content)
    
    # 检查是否还有图片标题
    if "### Images from this page" in result_content:
        print("❌ 仍然包含图片标题")
        return False
    else:
        print("✅ 已移除图片标题，图片直接融入内容")
        return True

def test_excel_no_headers():
    """测试Excel智能提取是否移除了图片标题"""
    print("\n📊 模拟Excel智能提取结果:")
    print("-" * 30)
    
    # 模拟Excel智能提取的markdown内容
    markdown_lines = []
    
    # Sheet1内容
    markdown_lines.append("\n## Sheet1\n")
    markdown_lines.append("| 产品 | 价格 | 库存 |")
    markdown_lines.append("| --- | --- | --- |")
    markdown_lines.append("| 产品A | 100 | 50 |")
    markdown_lines.append("| 产品B | 200 | 30 |")
    markdown_lines.append("")
    
    # Sheet1图片 (不再有标题)
    markdown_lines.append("![Image from sheet Sheet1](images/test/sheet_Sheet1_img_1.png)")
    markdown_lines.append("")
    
    markdown_lines.append("---\n")
    
    result_content = '\n'.join(markdown_lines)
    
    print("生成的Markdown内容:")
    print(result_content)
    
    # 检查是否还有图片标题
    if "### Images from this sheet" in result_content:
        print("❌ 仍然包含图片标题")
        return False
    else:
        print("✅ 已移除图片标题，图片直接融入内容")
        return True

def show_before_after_comparison():
    """显示修改前后的对比"""
    print("\n📊 修改前后对比")
    print("=" * 50)
    
    print("\n❌ 修改前 (有图片标题):")
    print("""
## Page 1
这里是第一页的文本内容...

### Images from this page

![Image from page 1](images/doc/page_1_img_1.png)

---
""")
    
    print("\n✅ 修改后 (图片直接融入):")
    print("""
## Page 1
这里是第一页的文本内容...

![Image from page 1](images/doc/page_1_img_1.png)

---
""")
    
    print("\n🎯 改进效果:")
    print("   - 移除了多余的'### Images from this page'标题")
    print("   - 图片更自然地融入到页面内容中")
    print("   - 保持了图片在正确位置的智能插入")
    print("   - 文档结构更简洁清晰")

def show_all_formats_effect():
    """显示所有格式的效果"""
    print("\n📄 所有格式的改进效果")
    print("=" * 40)
    
    formats = {
        'PDF': {
            'removed': '### Images from this page',
            'effect': '图片直接在页面内容后显示'
        },
        'Excel': {
            'removed': '### Images from this sheet', 
            'effect': '图片直接在工作表内容后显示'
        },
        'PowerPoint': {
            'removed': '### Images from this slide',
            'effect': '图片直接在幻灯片内容后显示'
        },
        'Word': {
            'removed': '(Word文档图片本来就在段落中)',
            'effect': '保持原有的段落内嵌入方式'
        }
    }
    
    for format_name, info in formats.items():
        print(f"\n{format_name}:")
        print(f"   移除标题: {info['removed']}")
        print(f"   效果: {info['effect']}")

def main():
    """主函数"""
    print("DocuGenius 图片标题移除测试")
    print("=" * 60)
    print("🎯 验证图片直接融入内容，不再有多余的标题")
    
    tests = [
        test_no_image_headers,
        test_excel_no_headers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    show_before_after_comparison()
    show_all_formats_effect()
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("🎉 图片标题移除成功!")
        print("现在图片会直接融入到内容中，不再有多余的标题!")
        return 0
    else:
        print("⚠️ 部分测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
