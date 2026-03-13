from openai import OpenAI
from .ai_classifier import AIClassifier
import os

class DeepseekClassifier(AIClassifier):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def classify(self, title: str, description: str, categories: list[str]) -> str:
        prompt = f"""Clasifica este artículo de Wikipedia en UNA de estas categorías: {", ".join(categories)}.

Título: {title}
Descripción: {description}

Responde SOLO con el nombre de la categoría, sin explicación."""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=20,
            messages=[{"role": "user", "content": prompt}]
        )
        
        if response.choices[0].message.content is None:
            return "General"
        
        result = response.choices[0].message.content.strip()
        return result if result in categories else "General"