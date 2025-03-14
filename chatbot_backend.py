from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Bilişsel Davranışçı Terapi (BDT) odaklı yanıtlar
BDT_RESPONSES = {
    "kaygı": "Kaygını yönetmek için derin nefes almayı deneyebilirsin. Şu an ne hissettiğini daha detaylı anlatabilir misin?",
    "olumsuz düşünce": "Olumsuz düşünceler bazen gerçeği yansıtmaz. Daha dengeli bir bakış açısıyla nasıl değerlendirebilirsin?",
    "stres": "Stres anında kısa bir mola verip rahatlatıcı bir aktivite yapabilirsin. Daha önce sana iyi gelen bir yöntem var mıydı?",
    "özgüven eksikliği": "Özgüvenini artırmak için küçük başarılarını fark etmeye ne dersin? Son zamanlarda başardığın bir şeyi düşünebilir misin?",
    "depresif hissetmek": "Bazen zor zamanlar olur, ama bu duygular geçicidir. Seni mutlu eden bir aktiviteyi denemek ister misin?"
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
    
    return {"response": "Bu konuda daha fazla bilgi verebilir misin? Seni daha iyi anlamak istiyorum."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
