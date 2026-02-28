from fastapi import FastAPI, Request, Header, HTTPException
from openai import OpenAI
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_TOKEN = os.getenv("BACKEND_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)

@app.post("/ask")
async def ask(request: Request, authorization: str = Header(None)):
    
    if authorization != f"Bearer {BACKEND_TOKEN}":
        raise HTTPException(status_code=403, detail="No autorizado")

    data = await request.json()
    message = data["message"]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Eres el Asistente Digital BSAFE. Responde de forma profesional, técnica y corporativa."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0.3
    )

    return {"response": response.choices[0].message.content}
