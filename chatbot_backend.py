from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn

app = FastAPI()

# ✅ Ana Sayfa Route'u - Bu olmazsa 404 verir!
@app.get("/")
def home():
    return {"message": "PiGa-AI API Çalışıyor!"}

# BDT Yanıtları
BDT_RESPONSES = {
    "kaygı": "Kaygını yönetmek için derin nefes almayı deneyebilirsin...",
    "olumsuz düşünce": "Olumsuz düşünceler bazen gerçeği yansıtmaz...",
    "stres": "Stres anında kısa bir mola verip rahatlatıcı bir aktivite yapabilirsin...",
    "özgüven eksikliği": "Özgüvenini artırmak için küçük başarılarını fark etmeye ne dersin?",
    "depresif hissetmek": "Bazen zor zamanlar olur, ama bu duygular geçicidir..."
}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_message = request.message.lower()
    
    # Anahtar kelimeye göre yanıt seçme
    for keyword, response in BDT_RESPONSES.items():
        if keyword in user_message:
            return {"response": response}
    
    return {"response": "Bu konuda daha fazla bilgi verebilir misin?"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render'ın verdiği PORT'u al
    uvicorn.run(app, host="0.0.0.0", port=port)

