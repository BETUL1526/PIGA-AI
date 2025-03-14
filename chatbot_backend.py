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
    allow_origins=["*"],  # Tüm sitelerden gelen isteklere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NLP modelini yükle
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Ana sayfa endpointi
@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}

# BDT odaklı yanıtlar
BDT_RESPONSES = {
    "kaygı": [
        "Kaygını yönetmek için derin nefes almayı deneyebilirsin. Şu an ne hissettiğini daha detaylı anlatabilir misin?",
        "Kaygılanmak doğaldır, ama üstesinden gelebilirsin. Birlikte bunu konuşabiliriz."
    ],
    "olumsuz düşünce": [
        "Olumsuz düşünceler bazen gerçeği yansıtmaz. Daha dengeli bir bakış açısıyla nasıl değerlendirebilirsin?",
        "Bu düşüncelerin doğruluğunu test etmek ister misin? Birlikte analiz edebiliriz."
    ],
    "stres": [
        "Stres anında kısa bir mola verip rahatlatıcı bir aktivite yapabilirsin. Daha önce sana iyi gelen bir yöntem var mıydı?",
        "Stresli hissediyorsan, biraz hareket etmek veya su içmek yardımcı olabilir."
    ],
    "özgüven eksikliği": [
        "Özgüvenini artırmak için küçük başarılarını fark etmeye ne dersin? Son zamanlarda başardığın bir şeyi düşünebilir misin?",
        "Bence düşündüğünden daha güçlüsün. Küçük adımlarla başlamak iyi olabilir!"
    ],
    "depresif hissetmek": [
        "Bazen zor zamanlar olur, ama bu duygular geçicidir. Seni mutlu eden bir aktiviteyi denemek ister misin?",
        "Etrafındaki destekleyici insanlarla konuşmak iyi gelebilir. Sen yalnız değilsin!"
    ],
    "selam": [
        "Merhaba! Sana nasıl yardımcı olabilirim?",
        "Selam! Bugün nasılsın?",
        "Hey! Kendini nasıl hissediyorsun?"
    ]
}

# Kullanıcı geçmişini saklamak için basit bir hafıza
user_memory = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_message = request.message.lower()
    doc = nlp(user_message)
    
    # Kullanıcının geçmişini al
    user_history = user_memory.get(request.user_id, [])
    user_history.append(user_message)
    user_memory[request.user_id] = user_history[-5:]  # Son 5 mesajı sakla
    
    # Anahtar kelime bazlı yanıt üret
    for keyword, responses in BDT_RESPONSES.items():
        if any(keyword in token.text for token in doc):
            return {"response": random.choice(responses), "memory": user_memory[request.user_id]}
    
    # Önceki mesajlara göre bağlamsal yanıt üret
    if len(user_history) > 1:
        return {"response": "Bunu daha önce konuşmuştuk, biraz daha detay verebilir misin?", "memory": user_memory[request.user_id]}
    
    return {"response": "Söylediklerini anlıyorum. Bunu biraz daha açabilir misin?", "memory": user_memory[request.user_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


