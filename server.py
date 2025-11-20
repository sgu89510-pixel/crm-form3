from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
import time

app = Flask(__name__, static_folder="")
CORS(app)

# === ОТДАЧА ФОРМЫ ===
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")

# === ПРИЁМ ЛИДА И ОТПРАВКА В AMO ===
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # Получение токена из переменной окружения
    amo_token = os.getenv("AMO_TOKEN")
    if not amo_token:
        return jsonify({"success": False, "error": "TOKEN_NOT_FOUND"})

    # Домен CRM
    amo_domain = "ilyadudin001.amocrm.ru"

    url = f"https://{amo_domain}/api/v4/contacts"

    headers = {
        "Authorization": f"Bearer {amo_token}",
        "Content-Type": "application/json"
    }

    # === Данные из формы ===
    firstname = data.get("firstname", "")
    lastname = data.get("lastname", "")
    country = data.get("country", "")
    phone = data.get("phone", "")
    year = data.get("year", "")
    comment = data.get("comment", "")

    # === Формируем custom_fields_values ===
    custom_fields_values = [
        { "field_id": 1, "values": [ { "value": firstname } ] },
        { "field_id": 2, "values": [ { "value": country } ] },
        { "field_id": 3, "values": [ { "value": phone } ] },
        { "field_id": 4, "values": [ { "value": year } ] },
        { "field_id": 5, "values": [ { "value": comment } ] },
    ]

    payload = [
        {
            "first_name": firstname,
            "last_name": lastname,
            "custom_fields_values": custom_fields_values
        }
    ]

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        return jsonify({
            "success": response.status_code == 200,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)