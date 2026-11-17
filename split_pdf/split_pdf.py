#!/usr/bin/env python3
"""Interactively split a PDF into multiple files without rasterizing its pages."""

import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("缺少 pypdf，请先运行：python3 -m pip install pypdf", file=sys.stderr)
    raise SystemExit(1)


# 【AI生成】
def ask_pdf_path():
    """Prompt for a PDF path and resolve pasted paths with shell quotes."""
    raw_path = input("请输入 PDF 文件地址：").strip()
    if len(raw_path) >= 2 and raw_path[0] == raw_path[-1] and raw_path[0] in {"'", '"'}:
        raw_path = raw_path[1:-1]
    return Path(raw_path).expanduser().resolve()


# 【AI生成】
def parse_page_counts(raw_value, total_pages):
    """Parse sequential page counts, optionally ending with '剩余'."""
    parts = [part.strip() for part in raw_value.split(",")]
    if not parts or any(not part for part in parts):
        raise ValueError("请用英文逗号分隔每份页数，例如：12,12,剩余")

    has_remainder = parts[-1] == "剩余"
    count_parts = parts[:-1] if has_remainder else parts
    if any(part == "剩余" for part in count_parts):
        raise ValueError("'剩余' 只能放在最后")
    if any(not re.fullmatch(r"[1-9]\d*", part) for part in count_parts):
        raise ValueError("每份页数必须是正整数")

    counts = [int(part) for part in count_parts]
    specified_pages = sum(counts)
    if has_remainder:
        if specified_pages >= total_pages:
            raise ValueError("明确填写的页数必须少于总页数，才能留出剩余页")
        counts.append(total_pages - specified_pages)
    elif specified_pages != total_pages:
        raise ValueError(f"页数合计为 {specified_pages}，但 PDF 共 {total_pages} 页")
    return counts


# 【AI生成】
def ask_split_counts(total_pages):
    """Collect a split method and return the page count for each output."""
    while True:
        print(f"\nPDF 共 {total_pages} 页。请选择拆分方式：")
        print("  1. 按文件数量均分")
        print("  2. 自定义每份页数（从前往后连续分配）")
        choice = input("请输入 1 或 2：").strip()
        if choice == "1":
            try:
                file_count = int(input("请输入要均分成几个文件：").strip())
                if not 1 <= file_count <= total_pages:
                    raise ValueError
                base, extra = divmod(total_pages, file_count)
                return [base + (1 if index < extra else 0) for index in range(file_count)]
            except ValueError:
                print(f"请输入 1 到 {total_pages} 之间的整数。", file=sys.stderr)
        elif choice == "2":
            raw_counts = input(
                "请输入每份页数，以英文逗号分隔；末尾可用“剩余”（例：12,12,剩余）："
            ).strip()
            try:
                return parse_page_counts(raw_counts, total_pages)
            except ValueError as error:
                print(f"输入无效：{error}", file=sys.stderr)
        else:
            print("请输入 1 或 2。", file=sys.stderr)


# 【AI生成】
def unique_output_paths(source, page_counts):
    """Build non-overwriting output paths beside the source PDF."""
    run_suffix = 1
    while run_suffix <= 10_000:
        paths = []
        current_page = 1
        for index, page_count in enumerate(page_counts, 1):
            end_page = current_page + page_count - 1
            run_label = "" if run_suffix == 1 else f"_{run_suffix}"
            filename = (
                f"{source.stem}{run_label}_拆分{index:02d}_第{current_page}-{end_page}页.pdf"
            )
            paths.append(source.with_name(filename))
            current_page = end_page + 1
        if not any(path.exists() for path in paths):
            return paths
        run_suffix += 1
    raise RuntimeError("无法生成不重名的输出文件名")


# 【AI生成】
def write_split_pdfs(reader, page_counts, output_paths):
    """Write the requested sequential page ranges into separate PDF files."""
    start_index = 0
    created_paths = []
    try:
        for page_count, output_path in zip(page_counts, output_paths):
            writer = PdfWriter()
            for page in reader.pages[start_index : start_index + page_count]:
                writer.add_page(page)
            if reader.metadata:
                metadata = {
                    str(key): str(value)
                    for key, value in reader.metadata.items()
                    if key and value is not None and str(key).startswith("/")
                }
                if metadata:
                    writer.add_metadata(metadata)
            with output_path.open("xb") as output_file:
                writer.write(output_file)
            created_paths.append(output_path)
            start_index += page_count
    except Exception:
        for created_path in created_paths:
            created_path.unlink(missing_ok=True)
        raise


# 【AI生成】
def main():
    """Prompt for a PDF and split it beside the source while preserving page content."""
    try:
        source = ask_pdf_path()
        if not source.is_file() or source.suffix.lower() != ".pdf":
            print("找不到该 PDF 文件，请检查路径。", file=sys.stderr)
            return 1
        reader = PdfReader(str(source), strict=False)
        if reader.is_encrypted:
            print("该 PDF 已加密，请先解除密码保护后再拆分。", file=sys.stderr)
            return 1
        total_pages = len(reader.pages)
        if total_pages < 2:
            print("PDF 至少需要 2 页才能拆分。", file=sys.stderr)
            return 1

        page_counts = ask_split_counts(total_pages)
        output_paths = unique_output_paths(source, page_counts)
        write_split_pdfs(reader, page_counts, output_paths)

        print("\n拆分完成，文件已输出到源 PDF 所在目录：")
        for output_path, page_count in zip(output_paths, page_counts):
            print(f"{output_path}（{page_count} 页）")
        return 0
    except EOFError:
        print("\n未收到输入，已取消。", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"拆分失败：{error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
