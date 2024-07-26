from secret import *
from openai import AzureOpenAI

ENDPOINT = AZURE_OPENAI_ENDPOINT
KEY = AZURE_OPENAI_API_KEY
MODEL = "gpt-35-turbo"


openai_client = AzureOpenAI(
    api_key=KEY,
    azure_endpoint=ENDPOINT,
    api_version="2024-05-01-preview"
)

def getResponce(prompt):
    responce = openai_client.chat.completions.create(
        model = MODEL,
        messages=[
            {"role":"system", "content": f"You are a helpful assistant. While you cannot provide medical diagnoses or specific medical advice, "
            "you can offer general information about symptoms and conditions based on common knowledge. "
            "Always remind users to consult with a healthcare professional for a proper diagnosis and treatment."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    
    )
    ai_responce = responce.choices[0].message.content
    return ai_responce