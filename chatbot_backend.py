from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import random
import json
import os

# BDT Terapist sınıfı
class BDTTherapist:
    def __init__(self):
        self.user_name = ""
        self.conversation_history = []
        self.message_count = 0
        self.current_emotion = None
        self.current_distortion = None
        
        # Duygular ve anahtar kelimeleri
        self.emotions = {
            'kaygı': ['kaygılı', 'endişeli', 'stresli', 'panik', 'korkuyorum', 'tedirgin', 'gergin'],
            'depresyon': ['üzgün', 'mutsuz', 'kederli', 'depresif', 'kötü', 'çaresiz', 'umutsuz', 'yorgun'],
            'öfke': ['kızgın', 'sinirli', 'öfkeli', 'rahatsız', 'delirdim', 'çıldırıyorum', 'sabırsız'],
            'suçluluk': ['suçlu', 'pişman', 'vicdan azabı', 'kötü hissetme', 'üzgünüm'],
            'utanç': ['utanıyorum', 'mahçup', 'rezil', 'kötü hissetme', 'sıkıldım'],
            'kıskançlık': ['kıskanç', 'kıskanıyorum', 'imreniyorum', 'çekemiyorum'],
            'yetersizlik': ['yetersiz', 'başarısız', 'yapamıyorum', 'beceremiyorum', 'kötüyüm'],
            'yalnızlık': ['yalnız', 'tek', 'kimse yok', 'anlaşılmıyorum', 'dışlanmış']
        }
        
        # Bilişsel çarpıtmalar ve anahtar kelimeleri
        self.cognitive_distortions = {
            'felaketleştirme': ['asla', 'her zaman', 'kesinlikle', 'kesin', 'kesinlikle olacak'],
            'ya hep ya hiç': ['ya hep', 'ya hiç', 'ya tamamen', 'ya hiç', 'ya mükemmel'],
            'zihinsel filtre': ['sadece', 'sadece kötü', 'sadece olumsuz', 'hep kötü'],
            'olumsuzluk': ['olumsuz', 'kötü', 'berbat', 'rezil', 'korkunç'],
            'duygusal çıkarım': ['hissediyorum', 'böyle hissettiğime göre', 'hissettiğim için'],
            'etiketleme': ['aptal', 'salak', 'kötü', 'berbat', 'rezil'],
            'kişiselleştirme': ['benim yüzümden', 'benim hatam', 'benim suçum'],
            'olmalı': ['olmalı', 'yapmalı', 'etmeli', 'kesinlikle yapmalı']
        }

        # Yanıtlar
        self.responses = {
            'greeting': [
                "Merhaba! Benimle konuşmak nasıl hissettiriyor?",
                "Hoş geldiniz! Bugün nasıl hissediyorsunuz?",
                "Merhaba! Sizi dinlemeye hazırım. Nasıl yardımcı olabilirim?"
            ],
            'emotion': {
                'kaygı': [
                    "Kaygı hissetmenize neden olan düşünceleriniz neler?",
                    "Bu kaygıyı yaşarken bedeninizde neler oluyor?",
                    "Kaygıyı azaltmak için şu an neler yapıyorsunuz?",
                    "Bu durumda en kötü ne olabilir? En iyi ne olabilir?",
                    "Kaygıyı yönetmek için nefes egzersizleri denediniz mi?"
                ],
                'depresyon': [
                    "Bu duyguyu yaşarken aklınızdan geçen düşünceler neler?",
                    "Günlük aktivitelerinizde değişiklik oldu mu?",
                    "Size iyi gelen şeyler neler?",
                    "Küçük adımlarla başlayarak neler yapabilirsiniz?",
                    "Size destek olabilecek kişiler var mı?"
                ],
                'öfke': [
                    "Öfkenizi tetikleyen düşünceler neler?",
                    "Öfkenizi ifade etmek için güvenli yollar neler olabilir?",
                    "Bu durumda sakinleşmek için neler yapabilirsiniz?",
                    "Öfkenizi kontrol etmek için kullandığınız yöntemler var mı?",
                    "Bu durumu farklı nasıl değerlendirebilirsiniz?"
                ],
                'suçluluk': [
                    "Suçluluk duygusuna neden olan düşünceleriniz neler?",
                    "Bu durumda başka nasıl davranabilirdiniz?",
                    "Kendinizi affetmek için neler yapabilirsiniz?",
                    "Bu durumdan ne öğrendiniz?",
                    "Gelecekte benzer durumlarda ne yapabilirsiniz?"
                ],
                'utanç': [
                    "Utanç duygusuna neden olan düşünceleriniz neler?",
                    "Bu durumu farklı nasıl değerlendirebilirsiniz?",
                    "Kendinize karşı daha anlayışlı olmak için neler yapabilirsiniz?",
                    "Bu durumdan ne öğrendiniz?",
                    "Gelecekte benzer durumlarda ne yapabilirsiniz?"
                ],
                'kıskançlık': [
                    "Kıskançlık duygusuna neden olan düşünceleriniz neler?",
                    "Bu durumu farklı nasıl değerlendirebilirsiniz?",
                    "Kendinize odaklanmak için neler yapabilirsiniz?",
                    "Bu durumdan ne öğrendiniz?",
                    "Gelecekte benzer durumlarda ne yapabilirsiniz?"
                ],
                'yetersizlik': [
                    "Yetersizlik duygusuna neden olan düşünceleriniz neler?",
                    "Bu durumu farklı nasıl değerlendirebilirsiniz?",
                    "Kendinize karşı daha anlayışlı olmak için neler yapabilirsiniz?",
                    "Bu durumdan ne öğrendiniz?",
                    "Gelecekte benzer durumlarda ne yapabilirsiniz?"
                ],
                'yalnızlık': [
                    "Yalnızlık duygusuna neden olan düşünceleriniz neler?",
                    "Bu durumu farklı nasıl değerlendirebilirsiniz?",
                    "Sosyal bağlantılarınızı güçlendirmek için neler yapabilirsiniz?",
                    "Bu durumdan ne öğrendiniz?",
                    "Gelecekte benzer durumlarda ne yapabilirsiniz?"
                ]
            },
            'cognitive_distortion': [
                "Bu düşünceyi farklı nasıl değerlendirebilirsiniz?",
                "Bu düşünceye karşı kanıtlarınız neler?",
                "Bu durumda en kötü ne olabilir? En iyi ne olabilir?",
                "Bu düşünce size nasıl yardımcı oluyor?",
                "Bu düşünceyi değiştirmek için neler yapabilirsiniz?"
            ],
            'practical_advice': [
                "Bu durumda yapabileceğiniz küçük adımlar neler?",
                "Size iyi gelen aktiviteler neler?",
                "Bu durumda size destek olabilecek kişiler var mı?",
                "Bu durumdan ne öğrendiniz?",
                "Gelecekte benzer durumlarda ne yapabilirsiniz?"
            ],
            'default': [
                "Bunu biraz daha açıklar mısınız?",
                "Bu konuda ne düşünüyorsunuz?",
                "Bu durumla ilgili nasıl hissediyorsunuz?",
                "Bana biraz daha detay verebilir misiniz?"
            ]
        }

        # BDT önerileri
        self.bdt_suggestions = {
            'kaygı': [
                "Kaygıyı yönetmek için 4-7-8 nefes tekniğini deneyebilirsiniz: 4 saniye nefes alın, 7 saniye tutun, 8 saniye verin.",
                "Kaygı verici durumları aşamalı olarak yüzleşmeyi deneyebilirsiniz. Önce en az kaygı veren durumdan başlayın.",
                "Kaygılı düşüncelerinizi bir günlüğe yazıp, gerçekçi alternatif düşünceler üretmeyi deneyebilirsiniz.",
                "Günlük rutininize gevşeme egzersizleri ekleyebilirsiniz: yoga, meditasyon veya yürüyüş gibi.",
                "Kaygı verici durumları önceden planlayıp, başa çıkma stratejileri geliştirebilirsiniz."
            ],
            'depresyon': [
                "Günlük aktivite planı oluşturup, küçük adımlarla başlayabilirsiniz. Her gün bir aktivite yapmayı hedefleyin.",
                "Olumsuz düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz.",
                "Sosyal bağlantılarınızı güçlendirmek için küçük adımlar atabilirsiniz: bir arkadaşınızı aramak gibi.",
                "Günlük rutininize keyif veren aktiviteler ekleyebilirsiniz: müzik dinlemek, resim yapmak gibi.",
                "Kendinize karşı daha anlayışlı olmayı öğrenebilirsiniz. Kendinize söylediğiniz olumsuz şeyleri fark edip değiştirebilirsiniz."
            ],
            'öfke': [
                "Öfke yönetimi için 'STOP' tekniğini kullanabilirsiniz: Stop (Dur), Take a step back (Geri çekil), Observe (Gözlemle), Proceed mindfully (Dikkatli ilerle).",
                "Öfkenizi ifade etmek için 'Ben' dilini kullanabilirsiniz: 'Ben... hissettiğimde... oluyor.'",
                "Öfke tetikleyicilerinizi bir günlüğe yazıp, bunlarla başa çıkma stratejileri geliştirebilirsiniz.",
                "Fiziksel aktivite öfkeyi azaltmada yardımcı olabilir: yürüyüş, koşu veya spor yapabilirsiniz.",
                "Öfke anında sakinleşmek için 10'a kadar sayma veya derin nefes alma tekniklerini kullanabilirsiniz."
            ],
            'suçluluk': [
                "Suçluluk duygusunu yönetmek için 'Affetme Mektubu' yazabilirsiniz: kendinize veya başkalarına.",
                "Suçluluk veren durumları analiz edip, gelecekte benzer durumlarda ne yapabileceğinizi planlayabilirsiniz.",
                "Kendinize karşı daha anlayışlı olmayı öğrenebilirsiniz. Herkes hata yapar.",
                "Suçluluk duygusunu azaltmak için yapıcı eylemlerde bulunabilirsiniz: özür dileme, telafi etme gibi.",
                "Suçluluk veren düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz."
            ],
            'utanç': [
                "Utanç duygusunu yönetmek için 'Şefkat Egzersizi' yapabilirsiniz: kendinize karşı anlayışlı olun.",
                "Utanç veren durumları analiz edip, gelecekte benzer durumlarda ne yapabileceğinizi planlayabilirsiniz.",
                "Kendinize karşı daha anlayışlı olmayı öğrenebilirsiniz. Herkes hata yapar.",
                "Utanç duygusunu azaltmak için yapıcı eylemlerde bulunabilirsiniz: özür dileme, telafi etme gibi.",
                "Utanç veren düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz."
            ],
            'kıskançlık': [
                "Kıskançlık duygusunu yönetmek için 'Şükran Günlüğü' tutabilirsiniz: her gün şükrettiğiniz 3 şeyi yazın.",
                "Kıskançlık veren durumları analiz edip, gelecekte benzer durumlarda ne yapabileceğinizi planlayabilirsiniz.",
                "Kendinize odaklanmayı öğrenebilirsiniz: kendi hedeflerinize ve başarılarınıza odaklanın.",
                "Kıskançlık duygusunu azaltmak için yapıcı eylemlerde bulunabilirsiniz: başkalarına yardım etmek gibi.",
                "Kıskançlık veren düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz."
            ],
            'yetersizlik': [
                "Yetersizlik duygusunu yönetmek için 'Başarı Günlüğü' tutabilirsiniz: her gün başardığınız 3 şeyi yazın.",
                "Yetersizlik veren durumları analiz edip, gelecekte benzer durumlarda ne yapabileceğinizi planlayabilirsiniz.",
                "Kendinize karşı daha anlayışlı olmayı öğrenebilirsiniz. Herkes hata yapar.",
                "Yetersizlik duygusunu azaltmak için yapıcı eylemlerde bulunabilirsiniz: yeni beceriler öğrenmek gibi.",
                "Yetersizlik veren düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz."
            ],
            'yalnızlık': [
                "Yalnızlık duygusunu yönetmek için 'Sosyal Bağlantı Planı' oluşturabilirsiniz: her gün bir sosyal aktivite planlayın.",
                "Yalnızlık veren durumları analiz edip, gelecekte benzer durumlarda ne yapabileceğinizi planlayabilirsiniz.",
                "Sosyal bağlantılarınızı güçlendirmeyi öğrenebilirsiniz: yeni insanlarla tanışmak, mevcut ilişkileri güçlendirmek gibi.",
                "Yalnızlık duygusunu azaltmak için yapıcı eylemlerde bulunabilirsiniz: gönüllü çalışmak gibi.",
                "Yalnızlık veren düşüncelerinizi bir günlüğe yazıp, bunlara karşı kanıtlar toplayabilirsiniz."
            ]
        }

    def detect_emotion(self, text):
        text = text.lower()
        for emotion, keywords in self.emotions.items():
            if any(keyword in text for keyword in keywords):
                return emotion
        return None

    def detect_cognitive_distortion(self, text):
        text = text.lower()
        for distortion, keywords in self.cognitive_distortions.items():
            if any(keyword in text for keyword in keywords):
                return distortion
        return None

    def get_bdt_suggestion(self):
        if self.current_emotion and self.current_emotion in self.bdt_suggestions:
            return random.choice(self.bdt_suggestions[self.current_emotion])
        return None

    def get_response(self, user_input):
        # Duygu tespiti
        emotion = self.detect_emotion(user_input)
        if emotion:
            self.current_emotion = emotion
            if emotion in self.responses['emotion']:
                return random.choice(self.responses['emotion'][emotion])

        # Bilişsel çarpıtma tespiti
        distortion = self.detect_cognitive_distortion(user_input)
        if distortion:
            self.current_distortion = distortion
            return random.choice(self.responses['cognitive_distortion'])

        # Selamlama tespiti
        if any(word in user_input.lower() for word in ['merhaba', 'selam', 'hey']):
            return random.choice(self.responses['greeting'])

        # Pratik öneri
        if any(word in user_input.lower() for word in ['ne yapmalıyım', 'nasıl yapmalıyım', 'önerir misin']):
            return random.choice(self.responses['practical_advice'])

        # Varsayılan yanıt
        return random.choice(self.responses['default'])

    def save_conversation(self):
        if not os.path.exists('conversations'):
            os.makedirs('conversations')
        
        filename = f'conversations/{self.user_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)

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

therapist = BDTTherapist()

# HTML şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BDT Terapist Bot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
            background-color: #f0f2f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #1a73e8;
            margin-bottom: 20px;
        }
        #chatbox {
            width: 100%;
            height: 500px;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow-y: auto;
            margin: auto;
            padding: 15px;
            text-align: left;
            background-color: #fff;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 5px;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: 20%;
        }
        .bot-message {
            background-color: #f5f5f5;
            margin-right: 20%;
        }
        .input-container {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        #userInput {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background-color: #1a73e8;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #1557b0;
        }
        .suggestion {
            background-color: #fff3e0;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>BDT Terapist Bot</h1>
        <div id="chatbox"></div>
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Mesajınızı yazın..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Gönder</button>
        </div>
    </div>

    <script>
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        function sendMessage() {
            let input = document.getElementById("userInput").value.trim();
            let chatbox = document.getElementById("chatbox");

            if (input === "") {
                addMessage("Hata: Lütfen bir mesaj yazın.", "error");
                return;
            }

            // Kullanıcının mesajını ekle
            addMessage(input, "user");

            // API'ye istek at
            fetch("/chat", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ message: input })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Sunucuya ulaşılamadı.");
                }
                return response.json();
            })
            .then(data => {
                // Bot yanıtını ekle
                addMessage(data.response, "bot");
            })
            .catch(error => {
                addMessage("Hata: Sunucuya bağlanılamadı. (" + error.message + ")", "error");
            });

            document.getElementById("userInput").value = ""; // Input'u temizle
            chatbox.scrollTop = chatbox.scrollHeight; // Sayfayı aşağı kaydır
        }

        function addMessage(message, type) {
            let chatbox = document.getElementById("chatbox");
            let messageDiv = document.createElement("div");
            messageDiv.className = `message ${type}-message`;
            
            let prefix = type === "user" ? "Siz" : "Terapist";
            messageDiv.innerHTML = `<strong>${prefix}:</strong> ${message}`;
            
            chatbox.appendChild(messageDiv);
            chatbox.scrollTop = chatbox.scrollHeight;
        }

        // Sayfa yüklendiğinde hoş geldin mesajı göster
        window.onload = function() {
            addMessage("Merhaba! Ben BDT terapist botuyum. Size nasıl yardımcı olabilirim?", "bot");
        };
    </script>
</body>
</html>
"""

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        if not chat_message.message:
            return {"response": "Lütfen bir mesaj yazın."}
        
        # Bot yanıtını al
        response = therapist.get_response(chat_message.message)
        
        # Her 5 mesajda bir BDT önerisi sun
        therapist.message_count += 1
        if therapist.message_count % 5 == 0:
            bdt_suggestion = therapist.get_bdt_suggestion()
            if bdt_suggestion:
                response += f"\n\nBDT temelli bir öneri sunmak istiyorum:\n{bdt_suggestion}"
        
        # Konuşma geçmişini kaydet
        therapist.conversation_history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user': chat_message.message,
            'bot': response,
            'emotion': therapist.detect_emotion(chat_message.message),
            'cognitive_distortion': therapist.detect_cognitive_distortion(chat_message.message)
        })
        
        # Konuşma geçmişini kaydet
        therapist.save_conversation()
        
        return {"response": response}
    except Exception as e:
        return {"response": f"Bir hata oluştu: {str(e)}"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("chatbot_backend:app", host="0.0.0.0", port=port, reload=True)