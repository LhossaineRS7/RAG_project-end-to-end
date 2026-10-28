from minsearch import Index
from google.genai import types
from ingest import load_labor_code_data, build_index
from tenacity import retry, stop_after_attempt, wait_exponential

documents = load_labor_code_data()
index = build_index(documents)

INSTRUCTIONS = """
Vous êtes un expert en droit du travail marocain (Loi 65-99).
Votre tâche est de répondre aux questions en vous basant uniquement sur le contexte fourni.
Si la réponse ne se trouve pas dans le contexte, répondez par "Je n'ai pas l'information."
"""

USER_PROMPT_TEMPLATE = """
QUESTION: {question}

CONTEXT:
{context}
""".strip()


class RAGBase:
    def __init__(
            self,
            index,
            llm_client,
            instructions,
            prompt_template=USER_PROMPT_TEMPLATE,
            model="gemini-3.6-flash"
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.prompt_template = prompt_template

        self.model = model

    def search(self, query, source_filter="Code du Travail - Loi 65-99"):
        boost_dict = {"content": 1.0}

        return self.index.search(
            query,
            boost_dict=boost_dict,
            num_results=5
        )

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(f"Article {doc['article_number']}:")
            lines.append(doc['content'])
            lines.append("")

        return "\n".join(lines).strip()

    def build_prompt(self, question, results):
        context = self.build_context(results)
        prompt = self.prompt_template.format(
            question=question,
            context=context
        )
        return prompt.strip()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def llm(self, prompt):
        # Google GenAI handles the roles directly in 'contents' and 'config'.

        response = self.llm_client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.instructions
            )
        )

        return response.text

    #the orchestrator method to run the pipeline!
    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer