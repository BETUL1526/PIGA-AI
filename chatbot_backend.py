from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import spacy
import random
import os
import time

# FastAPI uygulamasını başlat
app = FastAPI()

# CORS Middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm sitelere izin ver
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS"],  # HEAD isteğini destekle
    allow_headers=["*"],
)

# NLP modelini yükle
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# BDT odaklı yanıtlar
BDT_RESPONSES = {
    "kaygı": [
        "Kaygını yönetmek için derin nefes almayı deneyebilirsin.",
        "Kaygıyla başa çıkmak için meditasyon yapmayı düşünebilirsin.",
        "Kaygını daha iyi anlamaya çalışmak faydalı olabilir."
    ],
    "depresyon": [
        "Bir terapiste danışmak, depresyonu yönetmende yardımcı olabilir.",
        "Depresyonla başa çıkmak zaman alabilir, ancak küçük adımlarla ilerleyebilirsin.",
        "Günlük tutmak, duygularını anlamana yardımcı olabilir."
    ]
}

# İstek modeli
class ChatRequest(BaseModel):
    user_id: str
    message: str

# Chat endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print(f"Gelen istek: {request}")  # Gelen veriyi logla
    print(f"User ID: {request.user_id}, Message: {request.message}")
    
    doc = nlp(request.message.lower())
    
    # Mesajın hangi duygu kategorisine uyduğunu belirleme
    for category, responses in BDT_RESPONSES.items():
        if category in request.message.lower():
            return {"response": random.choice(responses)}
    
    return {"response": "Bu konuda nasıl hissettiğini biraz daha anlatabilir misin?"}

# Ana sayfa endpointi
@app.get("/")
def home():
    return {"message": "API is running! Send requests to /chat"}

    




