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
            'depres
