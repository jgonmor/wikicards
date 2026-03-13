import json
import os
from openai import OpenAI
from .ai_classifier import AIClassifier

class DeepseekClassifier(AIClassifier):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
    
    def classify(self, title: str, description: str, categories: list[str]) -> str:
        return self.classify_batch([{"title": title, "description": description}], categories)[0]


    def classify_batch(self, articles: list[dict], categories: list[str]) -> list[str]:
        articles_text = "\n".join([
            f"{i+1}. Título: {a['title']} | Descripción: {a['description']}"
            for i, a in enumerate(articles)
        ])

        prompt = f"""Clasifica cada artículo en UNA de estas categorías: {", ".join(categories)}.

{articles_text}

Responde SOLO con un array JSON con las categorías en el mismo orden, sin explicación.
Ejemplo: ["Deportista", "Lugar", "Animal"]"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}]
        )

        categories_set = set(categories)
        if response.choices[0].message.content is None:
            return ["General" for r in categories_set]
        
        result = response.choices[0].message.content.strip()
        parsed = json.loads(result)
        return [r if r in categories_set else "General" for r in parsed]
      