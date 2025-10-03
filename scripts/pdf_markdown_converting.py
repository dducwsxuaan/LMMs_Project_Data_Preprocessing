import os
import re
import fitz  # PyMuPDF

raw_folder = "data/raw"
images_folder = "data/extracted_images"
markdown_folder = "data/markdown"

# Ensure output directory exists
os.makedirs(markdown_folder, exist_ok=True)

# Section headers you expect in each case
HEADERS = [
    "History",
    "Clinical Findings",
    "Laboratory Results",
    "Discussion",
    "Questions",
    "Answer to Question 1",
    "Answer to Question 2",
    "The Case Continued",
    "SUMMARY BOX",
    "Further Reading",
]


def split_sections(text: str) -> dict:
    """Split extracted text into sections based on known headers."""
    sections = {}
    pattern = r'(?<=\n)(' + "|".join([re.escape(h) for h in HEADERS]) + r')[\s\.:]*\n'
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    current_header = "Intro"
    sections[current_header] = ""

    for part in parts:
        clean = part.strip()
        if not clean:
            continue
        if any(clean.lower().startswith(h.lower()) for h in HEADERS):
            current_header = clean
            sections[current_header] = ""
        else:
            sections[current_header] += clean + " "

    # Final cleanup
    for key in sections:
        sections[key] = sections[key].strip()

    return sections


def make_fig_replacer(pdf_name: str):
    """Return a function that replaces 'Fig. X.Y' with a Markdown link."""
    def replacer(match):
        nums = re.findall(r"\d+\.\d+", match.group(0))
        links = []
        for n in nums:
            image_filename = f"{pdf_name}_{n}.jpeg"
            image_path = f"../extracted_images/{image_filename}"
            links.append(f"[Fig. {n}]({image_path})")
        return ", ".join(links[:-1]) + " and " + links[-1] if len(links) > 1 else links[0]
    return replacer


def build_case_header(text: str, case_number: int) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if len(lines) >= 3:
        case_title = f"# Case {lines[0]}: {lines[1]} {lines[2]}"
        author_line = f"## {lines[3]}" if len(lines) > 3 else ""
        subtitle_line = f"# {lines[4]}" if len(lines) > 4 else ""
        header_block = "\n".join([case_title, author_line, subtitle_line])
        return header_block + "\n\n" + "\n".join(lines[5:])
    return text


# Iterate through all PDF files
for idx, pdf_file in enumerate(sorted(os.listdir(raw_folder)), start=1):
    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(raw_folder, pdf_file)
    pdf_doc = fitz.open(pdf_path)

    pdf_name = os.path.splitext(pdf_file)[0]

    # Extract text
    full_text = "\n".join(page.get_text("text") for page in pdf_doc)
    pdf_doc.close()

    # Step 1: Add Case header
    full_text = build_case_header(full_text, idx)

    # Step 2: Replace figures with links
    replacer = make_fig_replacer(pdf_name)
    markdown_text = re.sub(r"Figs?\. *(\d+\.\d+(?: *[,and]* *\d+\.\d+)*)", replacer, full_text)

    # Step 3: Split into sections
    sections = split_sections(markdown_text)

    # Step 4: Assemble Markdown output
    md_lines = []
    for header, content in sections.items():
        if header == "Intro":
            md_lines.append(content + "\n")
        else:
            md_lines.append(f"## {header}\n\n{content}\n")

    final_markdown = "\n".join(md_lines)

    # Save Markdown file
    md_filename = f"{pdf_name}.md"
    md_path = os.path.join(markdown_folder, md_filename)
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(final_markdown)

    print(f"✅ Converted {pdf_file} -> {md_path}")
