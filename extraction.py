import pymupdf  # PyMuPDF
import re
import json

pdf_path = "/code_du_travail.pdf"
def parse_labor_code(pdf_path):
    print("Opening PDF and extracting text...")
    doc = pymupdf.open(pdf_path)
    full_text = ""

    # 1. Extract raw text from all pages
    for page in doc:
        full_text += page.get_text("text") + "\n"

    # 2. Split the text into chunks
    # This regex cuts the text precisely where a new line starts with "Article [Number]"
    pattern = r'\n(?=Article\s+\d+)'
    raw_chunks = re.split(pattern, full_text)

    dataset = []

    # 3. Clean up the chunks and build the JSON metadata
    for chunk in raw_chunks:
        chunk = chunk.strip()

        # Find the article number to use as a metadata tag
        match = re.match(r'Article\s+(\d+)', chunk)

        if match:
            article_num = int(match.group(1))
            dataset.append({
                "id": f"loi_65_99_art_{article_num}",
                "article_number": article_num,
                "content": chunk,
                "source": "Code du Travail - Loi 65-99",
                "language": "fr"
            })

    return dataset


# Run the pipeline
pdf_filename = "/home/lhossaine/PycharmProjects/AI_RAG_project/code_du_travail.pdf"
json_filename = "labor_code_chunks.json"

dataset = parse_labor_code(pdf_filename)

# Save the results
with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

print(f"Success! Extracted {len(dataset)} articles and saved to {json_filename}.")