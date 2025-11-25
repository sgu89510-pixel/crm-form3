from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)


@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # Получаем реальный IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.remote_addr

        # Формируем payload строго по документации
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
            "ip": ip,
            "funnel": "AtomKz",
            "landingURL": "https://mercedes-4371.onrender.com",
            "geo": "KZ",
            "lang": "ru",
            "landingLang": "ru",
            "userAgent": request.headers.get("User-Agent"),
            "comment": None
        }

        CRM_URL = "https://symbios.hn-crm.com/api/v1/lead/create"

        headers = {
            "Content-Type": "application/json",
            "Api-Key": "53486a07-a2fc-4811-9375-a4eb919f0cec"
        }

        response = requests.post(CRM_URL, json=payload, headers=headers, timeout=30)

        return jsonify({
            "success": response.ok,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)