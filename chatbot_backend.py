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
</html>