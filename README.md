
## Data Preprocessing Stage in the Large Multimodal Models project in Tropical Disease Diagnosis

### Step 1: Clone this repository 

```bash
git clone 
``` 

### Step 2: Create `/raw/` inside `/data/` and upload your raw data (pdf files) to the folder `/data/raw/`. This is just for testing the processing stage, so you just need to upload some files

### Step 3: Run the file `/scripts/pdf_file_renaming.py` so that names of all pdf files are changed to the same format
```sh
python scripts/pdf_file_renaming.py
```

### Step 4: Run the file '/scripts/images_extracting.py` to extract all images from pdf files. The images are then stored in the folder `/data/extracted_images/`
```sh
python scripts/images_extracting.py
```

All images will have the standardized naming format described below:

Format Structure
```
case{case_number}_{page_number}.{image_number}.jpeg
```

 Format Breakdown
- **`case{case_number}`**: The case identifier (e.g., `case1`, `case2`, `case3`)
- **`{page_number}`**: The page number within the PDF where the image was found
- **`{image_number}`**: The sequential number of the image on that specific page
- **`.jpeg`**: File extension (all extracted images are in JPEG format)

 Examples
- `case1_1.1.jpeg` - First image from page 1 of case1.pdf
- `case1_1.2.jpeg` - Second image from page 1 of case1.pdf
- `case2_2.1.jpeg` - First image from page 2 of case2.pdf
- `case2_2.2.jpeg` - Second image from page 2 of case2.pdf
- `case2_2.3.jpeg` - Third image from page 2 of case2.pdf
- `case3_3.1.jpeg` - First image from page 3 of case3.pdf

### Step 5: Run the file `/scripts/pdf_markdown_converting.py` to convert PDF content to markdown format. The output markdown files are then stored in the folder `/data/markdown/`

```sh
python scripts/pdf_markdown_converting.py
```

All markdown files will have the standardized naming format described below:

 Markdown File Naming Convention

 Format Structure
```
case{case_number}.md
```

### Format Breakdown
- **`case{case_number}`**: The case identifier matching the source PDF (e.g., `case1`, `case2`, `case3`)
- **`.md`**: File extension for markdown format

### Examples
- `case1.md` - Markdown conversion of case1.pdf
- `case2.md` - Markdown conversion of case2.pdf
- `case3.md` - Markdown conversion of case3.pdf

