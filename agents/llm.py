import asyncio
import os
from groq import Groq
from dotenv import load_dotenv
import time

# 🔥 Load .env variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_sync(prompt):
    for attempt in range(3):
        try:
            res = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return res.choices[0].message.content

        except Exception as e:
            if "rate_limit" in str(e):
                print("⚠️ Rate limit hit, retrying...")
                time.sleep(5)
            else:
                raise e

    return "⚠️ Failed due to repeated rate limits"

async def call_llm(prompt):
    return await asyncio.to_thread(call_sync, prompt)