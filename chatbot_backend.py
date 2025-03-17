from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

# BDT Terapist sınıfı
class BDTTherapist:
    def __init__(self):
        self.emotions = {
            'kaygı': ['kaygılı', 'endişeli', 'stresli'],
            'depresyon': ['üzgün', 'mutsuz', 'kötü'],
            'öfke': ['kızgın', 'sinirli', 'öfkeli']
        }
        self.responses = {
            'kaygı': "Kaygıyı yönetmek için nefes egzersizleri yapabilirsiniz.",
            'depresyon': "Kendinizi iyi hissetmek için sevdiğiniz bir aktivite yapabilirsiniz.",
            'öfke': "Öfkeyi yönetmek için sakinleşme teknikleri deneyebilirsiniz."
        }

    def detect_emotion(self, text):
        text = text.lower()
        for emotion, keywords in self.emotions.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return None

    def get_response(self, user_input):
        emotion = self.detect_emotion(user_input)
        return self.responses.get(emotion, "Bunu biraz daha açıklar mısınız?")

# FastAPI uygulaması
app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

therapist = BDTTherapist()

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    if not chat_message.message:
        return {"response": "Lütfen bir mesaj yazın."}
    
    response = therapist.get_response(chat_message.message)
    return {"response": response}

# 🚀 **Hatalı satırı düzelttik!**
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("chatbot_backend:app", host="0.0.0.0", port=port, reload=True)
