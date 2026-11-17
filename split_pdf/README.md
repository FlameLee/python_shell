# split_pdf

交互式 PDF 拆分脚本。按页面直接拆分，不重新渲染图片或压缩页面；拆分结果保存在源 PDF 所在目录，原文件不变。

## 从零安装（macOS）

1. 从 [Python 官网 macOS 下载页](https://www.python.org/downloads/macos/)下载并安装 Python 3。安装完成后重新打开“终端”，检查：

   ```bash
   python3 --version
   ```

2. 将整个 `python_shell` 项目放在本机；在终端进入 `split_pdf` 目录：

   ```bash
   cd "/path/to/python_shell/split_pdf"
   ```

3. 为此脚本创建独立的 Python 环境，并安装 `pypdf`：

   ```bash
   python3 -m venv .venv
   .venv/bin/python -m pip install pypdf
   .venv/bin/python -c "import pypdf; print(pypdf.__version__)"
   ```

   最后一行能显示版本号，就表示安装成功。依赖只安装在这个脚本的 `.venv` 环境中，不会修改系统 Python；如果直接用其他 `python3` 启动脚本，仍可能提示缺少 `pypdf`。Homebrew Python 若阻止直接运行 `pip install`，也请使用上述虚拟环境方式。

## 使用

以后每次打开终端，进入该目录并用虚拟环境里的 Python 运行（把 `/path/to/python_shell` 换成实际存放项目的路径）：

```bash
cd "/path/to/python_shell/split_pdf"
.venv/bin/python split_pdf.py
```

1. 输入 PDF 文件的绝对路径（路径含空格时可直接粘贴，也可加单引号或双引号）。
2. 选择拆分方式：
   - **1 按数量均分**：输入文件数，例如 `4`。无法整除时，前面的文件各多一页。
   - **2 自定义每份页数**：用英文逗号隔开，从第 1 页起依次分配，例如 `12,12,剩余`，或者 `12,12,25`。页数必须恰好覆盖整个 PDF，且每份至少 1 页。
3. 在源 PDF 同目录查看输出，如 `资料_拆分01_第1-12页.pdf`。再次运行若有同名文件，脚本会使用新名称，不覆盖旧文件。

注意：加密 PDF 和不足 2 页的 PDF 不支持拆分。拆分不会使图片更清晰，也不会按目标体积压缩。
