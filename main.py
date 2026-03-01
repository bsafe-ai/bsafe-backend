import os
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# =========================
# CORS (IMPORTANTE)
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir a tu dominio luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# VARIABLES DE ENTORNO
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BACKEND_TOKEN = os.getenv("BACKEND_TOKEN")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY no configurada")

if not BACKEND_TOKEN:
    raise Exception("BACKEND_TOKEN no configurado")

client = OpenAI(api_key=OPENAI_API_KEY)

# =========================
# ENDPOINT PRINCIPAL
# =========================

@app.post("/ask")
async def ask(request: Request, authorization: str = Header(None)):

    # Validar token
    if authorization != f"Bearer {BACKEND_TOKEN}":
        raise HTTPException(status_code=401, detail="Token inválido")

    data = await request.json()
    user_message = data.get("message")

    if not user_message:
        return {"response": "Mensaje vacío."}

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Eres el Asistente Digital oficial de BSAFE, experto en ciberseguridad, protección de datos y consultoría tecnológica."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        answer = completion.choices[0].message.content

        # 🔥 ESTA ES LA CLAVE
        return {"response": answer}

    except Exception as e:
        return {"response": f"Error interno: {str(e)}"}


# =========================
# HEALTH CHECK
# =========================

@app.get("/")
def health():
    return {"status": "Backend BSAFE operativo"}

