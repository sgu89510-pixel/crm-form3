from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")

@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    if not data:
        return jsonify({"error": "Нет данных", "success": False})

    # Получение IP клиента
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.remote_addr

    crm_url = "https://symbios.hn-crm.com/api/external/integration/lead"

    headers = {
        "Content-Type": "application/json",
        "api-key": "53486a07-a2fc-4811-9375-a4eb919f0cec"
    }

    payload = {
        "affc": "AFF-O20FT4UUAO",
        "bxc": "BX-CL0XOBD3BRQ48",
        "vtc": "VT-HP8XSRMKVS6E7",

        "profile": {
            "firstName": data.get("firstName", ""),
            "lastName": data.get("lastName", ""),
            "email": data.get("email", ""),
            "password": "TempPass123!",
            "phone": data.get("phone", "").replace("+", "").replace(" ", "")
        },

        "ip": ip,
        "funnel": "AtomKz",
        "landingURL": "https://mercedes-4371.onrender.com",
        "geo": "KZ",
        "lang": "ru",
        "landingLang": "ru",
        "comment": "",
        "userAgent": request.headers.get("User-Agent", "")
    }

    try:
        resp = requests.post(crm_url, json=payload, headers=headers, timeout=30)
        return jsonify({
            "crm_response": resp.text,
            "crm_status": resp.status_code,
            "success": resp.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)