'''import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_response(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return "Sorry, I'm facing some issues at the moment."

def save_candidate_data(data, file_path="candidates.json"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r+") as f:
        existing = json.load(f)
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)
'''

'''
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if your account supports it
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI API Error:", e)
        return "Sorry, I'm facing some issues at the moment."
def save_candidate_data(data, file_path="candidates.json"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r+") as f:
        existing = json.load(f)
        existing.append(data)
        f.seek(0)
        json.dump(existing, f, indent=4)
        '''
import os
import requests
from dotenv import load_dotenv
import json

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_llm_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://your-app-url.com",  # Replace with your Streamlit URL or localhost
            "Content-Type": "application/json"
        }

        body = {
            "model": "meta-llama/llama-3-8b-instruct",  # Or try 'meta-llama/llama-3-8b-instruct:free'
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("OpenRouter API Error:", e)
        return "Sorry, I'm facing some issues at the moment."
    

def save_candidate_data(candidate_data, file_path="candidates.json"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(candidate_data)
        f.seek(0)
        json.dump(data, f, indent=4)
        
