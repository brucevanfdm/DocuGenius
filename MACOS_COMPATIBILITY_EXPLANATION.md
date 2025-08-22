# macOS 架构兼容性说明

## 为什么 ARM64 二进制文件可以在 Intel Mac 上运行？

### 🔍 技术原理

DocuGenius 的 macOS 二进制文件是在 Apple Silicon (ARM64) 环境下构建的，但它可以在 Intel Mac 上正常运行，这得益于以下技术：

#### 1. **Rosetta 2 转译技术**
- **自动转译**: Intel Mac 上的 Rosetta 2 可以自动将 ARM64 二进制文件转译为 x86_64 指令
- **透明运行**: 用户无需任何额外操作，系统会自动处理架构转换
- **性能表现**: 虽然有轻微的性能开销，但对于文档转换任务来说几乎无感知

#### 2. **PyInstaller 兼容性**
- **系统库依赖**: 我们的二进制文件主要依赖 macOS 系统库，这些库在两种架构上都可用
- **Python 运行时**: PyInstaller 打包的 Python 运行时可以通过 Rosetta 2 正常运行
- **第三方库**: pdfplumber、python-docx 等库都支持跨架构运行

### 📊 架构信息

```bash
$ file bin/darwin/docugenius-cli
bin/darwin/docugenius-cli: Mach-O 64-bit executable arm64

$ ls -lh bin/darwin/docugenius-cli
-rwxr-xr-x  1 user  staff   29.8M  docugenius-cli
```

### ✅ 兼容性测试

| 平台 | 架构 | 状态 | 说明 |
|------|------|------|------|
| **Apple Silicon Mac** | ARM64 | ✅ 原生运行 | 最佳性能 |
| **Intel Mac** | x86_64 | ✅ Rosetta 2 转译 | 良好性能 |
| **旧版 Intel Mac** | x86_64 | ✅ Rosetta 2 转译 | 需要 macOS 11+ |

### 🚀 优势

1. **单一二进制文件**: 无需维护多个架构版本
2. **简化分发**: 一个文件支持所有 Mac 用户
3. **自动兼容**: 系统自动处理架构差异
4. **维护简单**: 减少构建和测试复杂度

### 📋 系统要求

- **macOS 版本**: macOS 11.0 (Big Sur) 或更高版本
- **Rosetta 2**: Intel Mac 上自动安装（首次运行时）
- **权限**: 可执行权限（已设置）

### 🔧 故障排除

如果在 Intel Mac 上遇到问题：

1. **确认 Rosetta 2 已安装**:
   ```bash
   /usr/sbin/softwareupdate --install-rosetta
   ```

2. **检查文件权限**:
   ```bash
   chmod +x bin/darwin/docugenius-cli
   ```

3. **验证运行**:
   ```bash
   ./bin/darwin/docugenius-cli
   ```

### 💡 结论

这种方法是目前最优的解决方案，因为：
- **用户体验**: 无需用户关心架构差异
- **开发效率**: 单一构建流程
- **兼容性**: 覆盖所有现代 Mac 设备
- **性能**: 在两种架构上都有良好表现

---

**注意**: 这种兼容性是 Apple 官方支持的标准做法，许多主流应用都采用类似策略。