# compress_media

macOS 下的 PDF、静态图片压缩脚本。Python 负责交互和批量处理；运行时临时编译 Swift 程序，调用 macOS 的 PDFKit、AppKit 和 CoreGraphics。原文件不会被覆盖。

## 从零安装（macOS）

本脚本只支持 macOS。需要 Python 3 和 Apple 的 Xcode Command Line Tools；无需额外安装 Python 包，也不必安装完整 Xcode。

1. 从 [Python 官网 macOS 下载页](https://www.python.org/downloads/macos/)下载并安装 Python 3。安装完成后重新打开“终端”，检查：

   ```bash
   python3 --version
   ```

   如果显示版本号，继续下一步；如果提示找不到命令，先确认安装已完成，并重新打开终端。
2. 在终端安装 Xcode Command Line Tools，按系统弹窗完成安装：

   ```bash
   xcode-select --install
   ```

   随后检查 Swift 编译器：

   ```bash
   swiftc --version
   ```

   如果系统提示命令行工具已经安装，可直接检查 `swiftc --version`。安装步骤可能需要网络连接；脚本处理文件时使用本机 macOS 框架。
3. 将整个 `python_shell` 项目放在本机；确保此目录中存在 `compress_media.py`，再运行下一节命令。

## 使用方式

在终端进入脚本所在目录并运行（把 `/path/to/python_shell` 换成实际存放项目的路径）：

```bash
cd "/path/to/python_shell/compress_media"
python3 compress_media.py
```

根据提示：

1. 输入 PDF、图片文件或文件夹路径。文件夹会递归查找受支持文件。
2. 输入**所有输出文件合计**的大小上限，单位 MB，例如 `15`。
3. 选择压缩方式。直接回车默认选 **6 自动迭代到目标**。

也可以预先传入路径和目标大小，随后仍会出现压缩方式选择：

```bash
python3 compress_media.py "/path/to/input.pdf" --max-total-size 15
```

支持 PDF 和 `.jpg`、`.jpeg`、`.png`、`.tif`、`.tiff`、`.bmp`、`.heic`、`.heif` 图片。图片格式是否能够读取，还取决于当前 macOS 的解码支持。

## 压缩方式

| 选项 | 名称 | 最长边像素上限 | JPEG 质量 |
| --- | --- | ---: | ---: |
| 1 | 清晰优先 | 3200 | 0.92 |
| 2 | 推荐画质 | 2800 | 0.88 |
| 3 | 均衡 | 2400 | 0.82 |
| 4 | 较小体积 | 2000 | 0.74 |
| 5 | 最小体积 | 1600 | 0.66 |
| 6 | 自动迭代到目标（默认） | 从 3200 逐档降低至 1000 | 从 0.92 逐档降低至 0.48 |

手动选择 1–5 时只压缩一轮，不保证达到目标。选择 6 时，每轮均**从原文件**重新处理，按合计大小判断是否达标；超过目标就降低一档，首次达标即停止。若最低档仍超标，脚本会提示实际大小超过目标。档位是固定的，不会精确压到目标值，自动模式可能耗时较长。

## 输出位置与画质注意事项

- 输入单个文件时：在该文件旁新建 `<文件名>_compressed/`。
- 输入文件夹时：在该文件夹旁新建 `<文件夹名>_compressed/`，并保留文件夹内的相对路径。
- 再次运行会为输出文件夹添加数字后缀，不覆盖之前的结果。
- PDF 会逐页转成 JPEG 图像后写入新 PDF；小字、细线可能变模糊，原有可搜索文本和矢量内容可能丢失。
- 最长边像素数是**上限**，并不会把较小的源图像或页面放大；调高 JPEG 质量也无法恢复已丢失的细节。
- 透明图片输出 PNG；其他图片输出 JPEG。PNG 不使用表中的 JPEG 质量参数。

如需保持 PDF 页面内容不经重绘、仅按页拆分，请使用仓库中的 `split_pdf` 工具。
