import json
from minsearch import Index





def load_labor_code_data():
    # Hardcoded inside the function, just like docs_url
    file_path = "/home/lhossaine/PycharmProjects/AI_RAG_project/LLM_RAG/labor_code_chunks.json"

    with open(file_path, 'rt', encoding='utf-8') as f_in:
        documents = json.load(f_in)

    return documents


def build_index(documents):
    index = Index(
        text_fields=["content"],
        keyword_fields=["article_number"]
    )

    index.fit(documents)
    return index

# Usage:
# docs = load_labor_code_data()
# index = build_index(docs)