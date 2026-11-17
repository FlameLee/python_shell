# split_pdf

交互式 PDF 拆分脚本。按页面直接拆分，不重新渲染图片或压缩页面；拆分结果保存在源 PDF 所在目录，原文件不变。

## 环境要求

- Python 3
- `pypdf`：`python3 -m pip install pypdf`

如果 macOS 的 Homebrew Python 提示 `externally-managed-environment`，建议使用虚拟环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install pypdf
.venv/bin/python split_pdf.py
```

## 使用

在终端运行：

```bash
python3 split_pdf.py
```

1. 输入 PDF 文件的绝对路径（路径含空格时可直接粘贴，也可加单引号或双引号）。
2. 选择拆分方式：
   - **1 按数量均分**：输入文件数，例如 `4`。无法整除时，前面的文件各多一页。
   - **2 自定义每份页数**：用英文逗号隔开，从第 1 页起依次分配，例如 `12,12,剩余`，或者 `12,12,25`。页数必须恰好覆盖整个 PDF，且每份至少 1 页。
3. 在源 PDF 同目录查看输出，如 `资料_拆分01_第1-12页.pdf`。再次运行若有同名文件，脚本会使用新名称，不覆盖旧文件。

注意：加密 PDF 和不足 2 页的 PDF 不支持拆分。拆分不会使图片更清晰，也不会按目标体积压缩。
