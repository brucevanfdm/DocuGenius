# DocuGenius 国际化指南 / Internationalization Guide

## 概述 / Overview

DocuGenius 扩展现在支持国际化（i18n），可以根据 VSCode 的语言设置自动显示相应的语言文本。

The DocuGenius extension now supports internationalization (i18n) and can automatically display text in the appropriate language based on VSCode's language settings.

## 支持的语言 / Supported Languages

- **English (en)** - 默认语言 / Default language
- **简体中文 (zh-cn)** - 中文支持 / Chinese support

## 功能特性 / Features

### 1. 静态文本国际化 / Static Text Internationalization

以下内容会根据 VSCode 语言设置自动显示：
The following content will be automatically displayed based on VSCode language settings:

- 扩展名称和描述 / Extension name and description
- 命令标题 / Command titles
- 配置项描述 / Configuration descriptions
- 枚举选项描述 / Enum option descriptions

### 2. 动态文本国际化 / Dynamic Text Internationalization

运行时的文本也支持国际化：
Runtime text also supports internationalization:

- 通知消息 / Notification messages
- 状态栏文本 / Status bar text
- 日志消息 / Log messages
- 工具提示 / Tooltips

## 如何测试 / How to Test

### 方法 1: 更改 VSCode 语言 / Method 1: Change VSCode Language

1. 打开命令面板：`Ctrl+Shift+P` (Windows/Linux) 或 `Cmd+Shift+P` (Mac)
2. 输入并选择：`Configure Display Language`
3. 选择语言（如 `中文(简体)`）
4. 重启 VSCode
5. 检查扩展的菜单、设置和通知是否显示为选择的语言

### 方法 2: 使用扩展开发主机 / Method 2: Use Extension Development Host

1. 在扩展项目中按 `F5` 启动扩展开发主机
2. 在新窗口中更改语言设置
3. 重启开发主机窗口
4. 测试扩展功能

## 文件结构 / File Structure

```
DocuGenius/
├── package.json                 # 使用 %key% 占位符
├── package.nls.json            # 默认英文翻译
├── package.nls.zh-cn.json      # 中文翻译
└── src/
    ├── i18n.ts                 # 国际化管理器
    ├── extension.ts            # 使用国际化的主文件
    └── statusManager.ts        # 使用国际化的状态管理
```

## 添加新语言 / Adding New Languages

要添加新语言支持：
To add support for a new language:

1. 创建新的语言文件：`package.nls.{locale}.json`
   Create a new language file: `package.nls.{locale}.json`

2. 复制 `package.nls.json` 的内容并翻译所有值
   Copy the content of `package.nls.json` and translate all values

3. 确保所有键都存在且翻译完整
   Ensure all keys exist and are fully translated

### 示例：添加日语支持 / Example: Adding Japanese Support

创建 `package.nls.ja.json`：
Create `package.nls.ja.json`:

```json
{
  "extension.displayName": "DocuGenius",
  "extension.description": "Word、Excel、PowerPoint、PDFファイルをMarkdownに変換するインテリジェント文書コンバーター",
  "command.convertFile.title": "[DocuGenius]Markdownに変換",
  ...
}
```

## 开发指南 / Development Guide

### 在代码中使用国际化 / Using i18n in Code

```typescript
import { localize, getMessage, getStatusText } from './i18n';

// 基本用法
const message = localize('message.ready');

// 带参数的消息
const status = localize('status.converting', fileName);

// 便捷方法
const msg = getMessage('ready');
const statusText = getStatusText('ready');
```

### 添加新的本地化字符串 / Adding New Localized Strings

1. 在 `package.nls.json` 中添加新键
   Add new key in `package.nls.json`

2. 在所有语言文件中添加相应翻译
   Add corresponding translations in all language files

3. 在代码中使用 `localize()` 函数
   Use `localize()` function in code

## 测试脚本 / Test Script

运行测试脚本检查国际化配置：
Run the test script to check i18n configuration:

```bash
node test_i18n.js
```

这将验证：
This will verify:

- 所有语言文件的键是否一致
- package.json 中的占位符是否有对应的翻译
- 显示示例翻译

## 注意事项 / Notes

1. **重启要求**：更改 VSCode 语言后需要重启才能看到效果
   **Restart Required**: VSCode needs to be restarted after changing language to see the effect

2. **回退机制**：如果找不到特定语言文件，会自动回退到英文
   **Fallback Mechanism**: If a specific language file is not found, it will automatically fall back to English

3. **区域设置**：支持 `zh-cn` 这样的区域特定设置
   **Locale Settings**: Supports region-specific settings like `zh-cn`

4. **动态加载**：语言文件在扩展激活时动态加载
   **Dynamic Loading**: Language files are dynamically loaded when the extension is activated

## 故障排除 / Troubleshooting

### 问题：文本没有翻译 / Issue: Text Not Translated

1. 检查 VSCode 的语言设置
   Check VSCode's language settings

2. 确认对应的 `.nls.{locale}.json` 文件存在
   Confirm the corresponding `.nls.{locale}.json` file exists

3. 重启 VSCode
   Restart VSCode

4. 检查控制台是否有错误信息
   Check console for error messages

### 问题：部分文本未翻译 / Issue: Partial Text Not Translated

1. 检查语言文件中是否缺少某些键
   Check if some keys are missing in the language file

2. 运行 `node test_i18n.js` 检查配置
   Run `node test_i18n.js` to check configuration

3. 确保代码中使用了 `localize()` 函数
   Ensure `localize()` function is used in code
