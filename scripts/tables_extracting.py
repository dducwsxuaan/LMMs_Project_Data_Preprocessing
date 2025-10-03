
import os
import fitz  # PyMuPDF

raw_folder = "data/raw"
output_folder = "data/tables_extracted"
os.makedirs(output_folder, exist_ok=True)

pdf_path = "data/raw/case3.pdf"
pdf_doc = fitz.open(pdf_path)
# print(f"Opened {pdf_path} with {pdf_doc.page_count} pages.")
find = pdf_doc[0].find_tables()
print(find.tables[0].extract())