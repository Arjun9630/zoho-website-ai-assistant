import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.rag import ZohoRAG

load_dotenv()

# Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Initialize RAG once (expensive ops done only once)
rag = ZohoRAG()


class OpenAILLM:
    """
    OpenAI-powered LLM client with RAG and summarization support.
    """

    def generate(self, messages: list) -> dict:
        """
        Generates a structured JSON response using:
        - Full conversation context
        - Retrieved Zoho product knowledge (RAG)
        """

        user_message = messages[-1]["content"]

        # Retrieve relevant Zoho products
        relevant_products = rag.retrieve(user_message)

        # Build RAG context
        rag_context = "\n\n".join(
            json.dumps(product, indent=2) for product in relevant_products
        )

        # Inject RAG context as a system message
        messages_with_context = messages + [
            {
                "role": "system",
                "content": (
                    "Relevant Zoho product information:\n"
                    f"{rag_context}\n\n"
                    "Use this information to guide recommendations and ask relevant discovery questions."
                )
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_with_context,
            temperature=0.7,
            max_tokens=600
        )

        content = response.choices[0].message.content.strip()

        # Enforce JSON-only output safety
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "reply": "Sorry, I ran into a small issue while processing that. Could you please rephrase?",
                "extracted_info": {
                    "business_background": None,
                    "company_size": None,
                    "needs": [],
                    "wants_human_contact": False
                },
                "lead_signal": False,
                "conversation_summary": None
            }

    def summarize_conversation(self, messages: list) -> str:
        """
        Summarizes a conversation to preserve business context
        while reducing token usage.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Summarize the following conversation briefly. "
                        "Preserve business context, user needs, and any decisions made."
                    )
                }
            ] + messages,
            temperature=0.3,
            max_tokens=150
        )

        return response.choices[0].message.content.strip()
