from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


def get_client_ip():
    """Возвращает настоящий IP клиента (через Render proxy)"""
    if request.headers.get('X-Forwarded-For'):
        # Может быть несколько IP через запятую — берём первый
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        client_ip = get_client_ip()

        payload = {
            "affc": "AFF-O20FT4UUAO",
            "bxc": "BX-CL0XOBD3BRQ48",
            "vtc": "VT-HP8XSRMKVS6E7",

            "profile": {
                "firstName": data.get("firstName", ""),
                "lastName": data.get("lastName", ""),
                "email": data.get("email", ""),
                "password": "Temp12345!",
                "phone": data.get("phone", "").replace("+", "")
            },

            "ip": client_ip,                     # ⭐ РЕАЛЬНЫЙ IP ЛИДА
            "funnel": "AtomKz",
            "landingURL": "https://mercedes-4371.onrender.com",
            "geo": "KZ",
            "lang": "ru",
            "landingLang": "ru",
            "comment": None
        }

        # ✔️ правильный URL
        CRM_URL = "https://symbios.hn-crm.com/api/lead/create"

        headers = {
            "Content-Type": "application/json",
            "Api-Key": "53486a07-a2fc-4811-9375-a4eb919f0cec"
        }

        response = requests.post(CRM_URL, json=payload, headers=headers)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload     # ← можно удалить, но удобно для дебага
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)