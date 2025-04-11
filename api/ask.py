from openai import OpenAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hitesh-ai-bot.vercel.app/"],  # Or use ["http://localhost:5500"] for safety
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system_prompt = """
Tum ek AI teacher ho jo Hindi mein jawab deta hai jaise Hitesh Choudhary sir bolte hain...
"""

class AskRequest(BaseModel):
    query: str

@app.post("/api/ask")
async def ask(data: AskRequest):
    query = data.query

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
