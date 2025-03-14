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

# BDT odaklı yanıtlar
BDT_RESPONSES = {
    "kaygı": [
        "Kaygını yönetmek için derin nefes almayı deneyebilirsin. Şu an ne hissettiğini daha detaylı anlatabilir misin?",
        "Kaygılanmak doğaldır, ama üstesinden gelebilirsin




