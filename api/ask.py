from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

system_prompt = """
Tum ek AI teacher ho jo Hindi mein jawab deta hai jaise Hitesh Choudhary sir bolte hain...
"""

@app.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    query = data.get("query", "")

    if not query:
        return JSONResponse({"error": "Query is missing"}, status_code=400)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )

    reply = response.choices[0].message.content
    return {"reply": reply}
