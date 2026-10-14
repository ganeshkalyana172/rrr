"""Merge multiple PDFs or extract a page range with pypdf."""
from pathlib import Path
try: from pypdf import PdfReader, PdfWriter
except ImportError:
    print("Install dependency: python -m pip install pypdf"); raise SystemExit(1)
def merge():
    paths = [Path(s.strip().strip('"')).expanduser() for s in input("PDF paths separated by commas: ").split(",") if s.strip()]
    if len(paths) < 2 or any(not p.is_file() or p.suffix.lower() != ".pdf" for p in paths): print("Provide at least two valid PDF files."); return
    out = Path(input("Output filename [merged.pdf]: ").strip() or "merged.pdf")
    if out.suffix.lower() != ".pdf": out = out.with_suffix(".pdf")
    writer = PdfWriter()
    try:
        for p in paths:
            reader = PdfReader(str(p))
            if reader.is_encrypted: print("Encrypted PDF not supported:", p); return
            for page in reader.pages: writer.add_page(page)
        with out.open("wb") as f: writer.write(f)
        print("Merged PDF saved:", out.resolve())
    except Exception as e: print("Merge failed:", e)
def split():
    src = Path(input("PDF path: ").strip().strip('"')).expanduser()
    if not src.is_file() or src.suffix.lower() != ".pdf": print("PDF not found."); return
    try:
        reader = PdfReader(str(src))
        if reader.is_encrypted: print("Encrypted PDF not supported."); return
        total = len(reader.pages); print("Total pages:", total)
        start, end = int(input("Start page (1-based): ")), int(input("End page (1-based): "))
        if start < 1 or end < start or end > total: print("Invalid page range."); return
        out = Path(input(f"Output filename [{src.stem}_pages_{start}-{end}.pdf]: ").strip() or f"{src.stem}_pages_{start}-{end}.pdf")
        if out.suffix.lower() != ".pdf": out = out.with_suffix(".pdf")
        writer = PdfWriter()
        for i in range(start-1, end): writer.add_page(reader.pages[i])
        with out.open("wb") as f: writer.write(f)
        print("Split PDF saved:", out.resolve())
    except ValueError: print("Enter page numbers as whole numbers.")
    except Exception as e: print("Split failed:", e)
def main():
    while True:
        print("\nPDF MERGER & SPLITTER\n1 Merge PDFs\n2 Split/extract pages\n3 Exit")
        c = input("Choose: ").strip()
        if c == "1": merge()
        elif c == "2": split()
        elif c == "3": break
        else: print("Choose 1-3.")
if __name__ == "__main__": main()
