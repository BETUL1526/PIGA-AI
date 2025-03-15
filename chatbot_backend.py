from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
import random
import os

# FastAPI uygulamasını başlat
app = FastAPI()

# CORS Middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm sitelere izin ver
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],  
    allow_headers=["*"],
)

# NLP modelini yükle
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Kullanıcıdan gelen isteğin formatı
class ChatRequest(BaseModel):
    user_id: str
    message: str

# BDT odaklı yanıtlar
BDT_RESPONSES = {
    "kaygı": [
        "Kaygını yönetmek için derin nefes almayı deneyebilirsin.",
        "Kaygıyla başa çıkmak için meditasyon yapabilirsin.",
        "Kaygını daha iyi anlamaya çalışmak faydalı olabilir."
    ],
    "depresyon": [
        "Bir terapiste danışmak faydalı olabilir.",
        "Depresyon zaman alır ama küçük adımlarla ilerleyebilirsin.",
        "Duygularını paylaşmak iyi gelebilir."
    ]
}

# Chat endpointi
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"💬 Gelen İstek: {request}")  # Gelen veriyi logla
    print(f"🆔 User ID: {request.user_id}, 📩 Message: {request.message}")  

    doc = nlp(request.message.lower())

    for category, responses in BDT_RESPONSES.items():
        if category in request.message.lower():
            return {"response": random.choice(responses)}

    return {"response": "Bu konuda nasıl hissettiğini biraz daha anlatabilir misin?"}

# Ana sayfa
@app.get("/")
async def root():
    return {"message": "API is running! Send requests to /chat"}

# 🚀 Render'ın PORT değişkenini algılaması için ekleme:
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render'ın PORT değişkenini al
    uvicorn.run(app, host="0.0.0.0", port=port)

    




