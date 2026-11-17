# python_shell

存放可在终端运行的 Python 工具脚本。每个功能独立放在一个文件夹中，具体用法见对应目录的 README。

| 文件夹 | 用途 |
| --- | --- |
| [`compress_media/`](compress_media/README.md) | 压缩 PDF 和图片。使用 macOS 框架处理，支持选择画质档位或按目标体积逐档尝试。 |
| [`split_pdf/`](split_pdf/README.md) | 按文件数量均分 PDF，或按自定义页数拆分 PDF；在源文件目录输出，不重新渲染页面。 |

运行脚本前，请按各目录 README 安装所需依赖；两个脚本的依赖和适用环境不同。
