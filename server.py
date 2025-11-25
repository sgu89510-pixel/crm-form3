from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")

@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # Получаем IP пользователя корректно
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        ip = request.remote_addr

    crm_url = "https://symbios.hn-crm.com/api/v1/lead/create"

    headers = {
        "Content-Type": "application/json",
        "Api-Key": "53486a07-a2fc-4811-9375-a4eb919f0cec"
    }

    payload = {
        "affc": "AFF-O20FT4UUAO",
        "bxc": "BX-CL0XOBD3BRQ48",
        "vtc": "VT-HP8XSRMKVS6E7",

        "profile": {
            "firstName": data.get("name", ""),
            "lastName": data.get("lastname", ""),
            "email": data.get("email", ""),
            "password": "Temp12345!",
            "phone": data.get("phone", "").replace("+", "").replace(" ", "").replace("-", "")
        },

        "ip": ip,
        "funnel": "AtomKz",
        "landingURL": "https://mercedes-4371.onrender.com",
        "geo": "KZ",
        "lang": "ru",
        "landingLang": "ru",
        "userAgent": request.headers.get("User-Agent"),
        "comment": None
    }

    try:
        response = requests.post(crm_url, headers=headers, json=payload, timeout=30)

        return jsonify({
            "crm_response": response.text,
            "crm_status": response.status_code,
            "success": response.ok
        })
    except Exception as e:
        return jsonify({"error": str(e), "success": False})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)