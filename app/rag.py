import json
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ZohoRAG:
    def __init__(self, knowledge_dir="app/knowledge/products"):
        self.knowledge_dir = knowledge_dir
        self.products = []
        self.embeddings = []

        self._load_products()
        self._embed_products()

    def _load_products(self):
        for file in os.listdir(self.knowledge_dir):
            if file.endswith(".json"):
                with open(os.path.join(self.knowledge_dir, file), "r", encoding="utf-8") as f:
                    self.products.append(json.load(f))

    def _embed_text(self, text: str):
        response = client.embeddings.create(
            model="text-embedding-3-small",  # cheap & good
            input=text
        )
        return np.array(response.data[0].embedding)

    def _embed_products(self):
        for product in self.products:
            text = self._product_to_text(product)
            embedding = self._embed_text(text)
            self.embeddings.append(embedding)

    def _product_to_text(self, product: dict) -> str:
        return f"""
        Product: {product['product_name']}
        Category: {product['category']}
        Problems solved: {', '.join(product['primary_problems_solved'])}
        Ideal for: {', '.join(product['ideal_for'])}
        Workflows: {', '.join(product['key_workflows'])}
        """

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self._embed_text(query)

        similarities = cosine_similarity(
            [query_embedding], self.embeddings
        )[0]

        top_indices = similarities.argsort()[-top_k:][::-1]

        return [self.products[i] for i in top_indices]
