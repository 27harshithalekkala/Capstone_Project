import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")


def ask_gemini(context, question):
    """
    Send retrieved document context and the user's question to Gemini.
    """

    prompt = f"""
You are an Enterprise Financial Intelligence Assistant.

Answer the user's question using ONLY the information provided in the context.

Context:
{context}

Question:
{question}

If the answer is not available in the context, reply:

'I could not find this information in the uploaded documents.'
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text