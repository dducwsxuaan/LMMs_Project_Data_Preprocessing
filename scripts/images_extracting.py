import os
import fitz  # PyMuPDF

raw_folder = "data/raw"
output_folder = "data/extracted_images"

# Ensure output directory exists
os.makedirs(output_folder, exist_ok=True)

# Iterate through all PDF files in the raw folder
for pdf_file in sorted(os.listdir(raw_folder)):
    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(raw_folder, pdf_file)
    pdf_doc = fitz.open(pdf_path)

    # Use the PDF name (without extension) as prefix
    pdf_name = os.path.splitext(pdf_file)[0]

    # Extract case number (assumes filenames like case1.pdf, case2.pdf, ...)
    if pdf_name.startswith("case"):
        case_number = int(pdf_name.replace("case", ""))
    else:
        case_number = sorted(os.listdir(raw_folder)).index(pdf_file) + 1

    image_counter = 1  # counter for images inside each case

    # Loop through pages
    for page_num in range(pdf_doc.page_count):
        page = pdf_doc.load_page(page_num)
        image_list = page.get_images(full=True)

        # Extract each image on the page
        for img in image_list:
            xref = img[0]
            base_image = pdf_doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Final filename: prefix + case.image.ext
            # Example: case1_1.1.jpg, case2_2.1.jpg
            image_name = f"{pdf_name}_{case_number}.{image_counter}.{image_ext}"
            image_path = os.path.join(output_folder, image_name)

            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)

            print(f"Extracted {image_path}")
            image_counter += 1

    pdf_doc.close()

print("✅ Image extraction complete for all PDFs!")
