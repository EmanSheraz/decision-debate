import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[{"role": "user", "content": "Say hello in 5 words."}],
   )
print(resp.choices[0].message.content)