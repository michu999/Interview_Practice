import requests
import os
import openai

api_key = os.getenv("GEMINI_API_KEY")  # lub GOOGLE_API_KEY, zależnie jak masz w .env
url = "https://generativelanguage.googleapis.com/v1beta/models"

headers = {"x-goog-api-key": api_key}

response = requests.get(url, headers=headers)
print(response.status_code, response.json())

print('---------------------------------------------------')

api_key = os.getenv("DEEPSEEK_API_KEY")
url = "https://api.deepseek.com/v1/models"

headers = {"Authorization": f"Bearer {api_key}"}

response = requests.get(url, headers=headers)
print(response.status_code, response.json())

print('---------------------------------------------------')


openai.api_key = os.getenv("OPENAI_API_KEY")

models = openai.models.list()
for model in models.data:
    print(model.id)