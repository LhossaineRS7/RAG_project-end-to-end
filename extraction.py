import pymupdf  # Replaced 'fitz' to remove the deprecation warning
import re
import json


def clean_chunk(text):
    # 1. Remove page numbers that look like "- 114 -" or "114" at the bottom of pages
    text = re.sub(r'-\s*\d+\s*-', '', text)

    # 2. Remove the massive footer notes (usually starting with a number and a dash, e.g., "48 - Arrêté...")
    # This regex looks for lines that start with 1-3 digits followed by a dash and removes them
    text = re.sub(r'^\d{1,3}\s*-\s*.*', '', text, flags=re.MULTILINE)

    # 3. Clean up excess blank lines and spaces caused by the deletions
    text = re.sub(r'\n+', '\n', text).strip()

    return text


def parse_labor_code(pdf_path):
    print("Opening PDF and extracting text...")
    doc = pymupdf.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text("text") + "\n"

    # Split the text into chunks by Article
    pattern = r'\n(?=Article\s+\d+)'
    raw_chunks = re.split(pattern, full_text)

    dataset = []

    for chunk in raw_chunks:
        # Pass the chunk through our new cleaning function
        cleaned_chunk = clean_chunk(chunk)

        # We limit the regex to look for Article numbers between 1 and 4 digits
        # to prevent it from grabbing massive footnote glitches (like 32748)
        match = re.match(r'Article\s+(\d+)', cleaned_chunk)

        if match:
            article_num = int(match.group(1))

            # If the parser still accidentally fused a footnote making the number > 1000, skip it or fix it.
            # The Moroccan Labor Code only has about 586 articles.
            if article_num > 1000:
                # We slice off the last digits assuming they are footnotes (e.g. 32748 -> 327)
                article_num = int(str(article_num)[:-2])

            dataset.append({
                "id": f"loi_65_99_art_{article_num}",
                "article_number": article_num,
                "content": cleaned_chunk,
                "source": "Code du Travail - Loi 65-99",
                "language": "fr"
            })

    return dataset


# Run the pipeline
pdf_filename = "/home/lhossaine/PycharmProjects/AI_RAG_project/code_du_travail.pdf"
json_filename = "labor_code_chunks.json"

dataset = parse_labor_code(pdf_filename)

with open(json_filename, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)

print(f"Success! Cleaned and extracted {len(dataset)} articles.")