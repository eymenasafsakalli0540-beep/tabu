"""
Tabu (Siret-i Nebi) - basit Flask sunucusu
------------------------------------------
Tahta (bilgisayar/akıllı tahta) ve telefon aynı state'i bu sunucu
üzerinden paylaşır. Board sayfası her 1 saniyede bir /api/state'ten
okur, telefon her aksiyonda (başlat/doğru/pas/süre bitti) state'i
buraya POST eder.

RENDER.COM'A DEPLOY (önerilen — okulda flash sürücü/yerel ağ derdi olmaz):
    1. Bu klasörü bir GitHub reposuna yükleyin.
    2. render.com'da "New +" -> "Web Service" -> reponuzu seçin.
    3. Build Command:  pip install -r requirements.txt
       Start Command:  gunicorn app:app
    4. Deploy edince Render size https://xxxxx.onrender.com gibi
       gerçek bir adres verir. Okulda o adresi tahtada açmanız
       yeterli, telefon da aynı adrese QR ile bağlanır (aynı
       WiFi'da olma zorunluluğu YOK, ikisi de sadece internete
       bağlı olsun yeterli).

YEREL TEST (isteğe bağlı):
    pip install -r requirements.txt
    python app.py
    -> http://localhost:5000
"""

from flask import Flask, jsonify, request, render_template
from threading import Lock

app = Flask(__name__)

# ---- Kelime listesi ----
WORDS = [
    {"word": "HİCRET", "forbidden": ["Mekke", "Medine", "Göç", "Yıl", "Müslüman"]},
    {"word": "VEDA HUTBESİ", "forbidden": ["Son", "Hac", "Konuşma", "Arafat", "Vaaz"]},
    {"word": "VAHİY", "forbidden": ["Cebrail", "Melek", "Allah", "Ayet", "İndirmek"]},
    {"word": "ASHAB-I SUFFE", "forbidden": ["Mescit", "İlim", "Fakir", "Medine", "Eğitim"]},
    {"word": "ENSAR", "forbidden": ["Medineli", "Yardım", "Misafir", "Mekkeli", "Kardeş"]},
    {"word": "MUHACİR", "forbidden": ["Mekke", "Göç etmek", "Ayrılmak", "Medine", "Gitmek"]},
    {"word": "HUDEYBİYE ANTLAŞMASI", "forbidden": ["Barış", "Müşrik", "Anlaşma", "Mekke", "Yıl"]},
    {"word": "BEDİR SAVAŞI", "forbidden": ["İlk", "Mücadele", "Kuyu", "Zafer", "Asker"]},
    {"word": "UHUD SAVAŞI", "forbidden": ["Dağ", "Okçu", "Hata", "Şehit", "Savaş"]},
    {"word": "HENDEK SAVAŞI", "forbidden": ["Kazmak", "Savunma", "Selman-i Farisî", "Şehir", "Çukur"]},
    {"word": "MEKKE'NİN FETHİ", "forbidden": ["Almak", "Kabe", "Kanlı", "Geri dönmek", "Put"]},
    {"word": "EMİN (MUHAMMEDÜ'L-EMİN)", "forbidden": ["Güvenilir", "Dürüst", "Lakap", "Yalan", "Peygamber"]},
    {"word": "HİRA MAĞARASI", "forbidden": ["Dağ", "Nur", "İbadet", "Yalnızlık", "İlk ayet"]},
    {"word": "ASR-I SAADET", "forbidden": ["Mutluluk", "Asr", "Dönem", "Çağ", "Huzur"]},
    {"word": "EHLİBEYT / HZ. FATIMA", "forbidden": ["Aile", "Evlat", "Kız", "Hz. Fatıma", "Soy"]},
]

lock = Lock()

# ---- Sunucu tarafında tutulan tek ortak oyun durumu ----
state = {
    "teamA": {"name": "Takım A", "score": 0},
    "teamB": {"name": "Takım B", "score": 0},
    "activeTeam": "teamA",
    "timeLeft": 60,
    "running": False,
    "wordsLeft": len(WORDS),
    "lastResult": None,
}


@app.route("/")
def index():
    return render_template("index.html", words=WORDS)


@app.route("/api/words")
def get_words():
    # Kelimeler sadece telefon (kontrol) tarafına gönderilir
    return jsonify(WORDS)


@app.route("/api/state", methods=["GET"])
def get_state():
    with lock:
        return jsonify(state)


@app.route("/api/state", methods=["POST"])
def set_state():
    global state
    data = request.get_json(force=True)
    with lock:
        state.update({
            "teamA": data.get("teamA", state["teamA"]),
            "teamB": data.get("teamB", state["teamB"]),
            "activeTeam": data.get("activeTeam", state["activeTeam"]),
            "timeLeft": data.get("timeLeft", state["timeLeft"]),
            "running": data.get("running", state["running"]),
            "wordsLeft": data.get("wordsLeft", state["wordsLeft"]),
            "lastResult": data.get("lastResult", state["lastResult"]),
        })
        return jsonify(state)


@app.route("/api/reset", methods=["POST"])
def reset_state():
    global state
    with lock:
        state = {
            "teamA": {"name": "Takım A", "score": 0},
            "teamB": {"name": "Takım B", "score": 0},
            "activeTeam": "teamA",
            "timeLeft": 60,
            "running": False,
            "wordsLeft": len(WORDS),
            "lastResult": None,
        }
        return jsonify(state)


if __name__ == "__main__":
    import os
    # Render prod ortamda gunicorn kullanır; bu blok sadece yerel test içindir.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
