from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder="")
CORS(app)

# === ОТДАЧА ФОРМЫ ===
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "lead_form.html")


# === ПРИЁМ ЛИДА И ПЕРЕДАЧА В amoCRM ===
@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    # ===== собираем нужные данные =====
    payload = {
        "name": data.get("name", ""),
        "phone": data.get("phone", ""),
        "country": data.get("country", ""),
        "car_year": data.get("car_year", ""),
        "comment": data.get("comment", "")
    }

    # ===== отправляем POST в их import_lead.php =====
    crm_url = "https://ilyadudin001.amocrm.ru/import_lead.php"

    try:
        response = requests.post(crm_url, data=payload, timeout=20)
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