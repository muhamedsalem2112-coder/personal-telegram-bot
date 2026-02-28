import os
import time
import requests
import numpy as np
from datetime import datetime
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sklearn.ensemble import IsolationForest

# ==============================
# تحميل الإعدادات
# ==============================
load_dotenv()

TELEGRAM_TOKEN = os.getenv("8729024348:AAHqh0vjB4SDVav03TmAwAKn6EYob-3Kfs4")
CHAT_ID = os.getenv("7943448378")
DATABASE_URL = os.getenv("DATABASE_URL")

BRUTE_FORCE_THRESHOLD = 5
BRUTE_FORCE_WINDOW = 60
HIGH_RISK_THRESHOLD = 70

# ==============================
# إعداد قاعدة البيانات
# ==============================
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    user = Column(String)
    ip = Column(String)
    event_type = Column(String)
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ==============================
# إعداد AI Model
# ==============================
model = IsolationForest(contamination=0.05)
X_train = np.random.rand(200, 3)
model.fit(X_train)

def detect_anomaly(features):
    prediction = model.predict([features])
    return 1 if prediction[0] == -1 else 0

# ==============================
# نظام تقييم الخطورة
# ==============================
def calculate_risk(event_type, anomaly_score):
    base_risk = 0

    if event_type == "login_failed":
        base_risk += 30
    elif event_type == "sql_injection":
        base_risk += 80
    elif event_type == "xss_attempt":
        base_risk += 60
    elif event_type == "data_exfiltration":
        base_risk += 75

    risk = base_risk + (anomaly_score * 40)
    return min(risk, 100)

# ==============================
# Telegram Alert
# ==============================
def send_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except:
        pass

# ==============================
# FastAPI App
# ==============================
app = FastAPI()
login_tracker = {}

@app.post("/log")
async def receive_log(request: Request):
    data = await request.json()
    
    user = data.get("user")
    ip = data.get("ip")
    event_type = data.get("event")

    if not user or not ip or not event_type:
        return {"error": "Invalid log format"}

    # ======================  
    # AI Features  
    # ======================
    features = [
        len(user),
        len(ip),
        time.time() % 100
    ]

    anomaly_score = detect_anomaly(features)
    risk_score = calculate_risk(event_type, anomaly_score)

    # ======================  
    # تخزين في DB
    # ======================
    db = SessionLocal()
    event = Event(
        user=user,
        ip=ip,
        event_type=event_type,
        risk_score=risk_score
    )
    db.add(event)
    db.commit()
    db.close()

    # ======================  
    # Brute Force Detection
    # ======================
    if event_type == "login_failed":
        login_tracker.setdefault(user, []).append(time.time())
        login_tracker[user] = [
            t for t in login_tracker[user]
            if time.time() - t < BRUTE_FORCE_WINDOW
        ]

        if len(login_tracker[user]) >= BRUTE_FORCE_THRESHOLD:
            send_alert(
                f"🚨 BRUTE FORCE DETECTED\n"
                f"User: {user}\nIP: {ip}"
            )

    # ======================  
    # High Risk Alert
    # ======================
    if risk_score >= HIGH_RISK_THRESHOLD:
        send_alert(
            f"🔥 HIGH RISK EVENT\n"
            f"User: {user}\n"
            f"IP: {ip}\n"
            f"Event: {event_type}\n"
            f"Risk Score: {risk_score}"
        )

    return {
        "status": "secured",
        "risk_score": risk_score,
        "anomaly": anomaly_score
    }