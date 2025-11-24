from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# === 1. Отдаем HTML форму ===
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


# === 2. Приём данных формы ===
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json

        name = data.get("name", "")
        lastname = data.get("lastname", "")
        country = data.get("country", "")
        phone = data.get("phone", "")
        car_year = data.get("car_year", "")
        comment = data.get("comment", "")

        # Формируем payload, КОТОРЫЙ ИХ API ОЖИДАЕТ
        incomingLead = {
            "name": f"{name} {lastname}",
            "country": country,
            "phone": phone,
            "car_year": car_year,
            "comment": comment
        }

        # === ВАЖНО ===
        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        # Отправляем POST на их сервер
        response = requests.post(CRM_URL, json=incomingLead, timeout=10)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# === Запуск сервера (Render) ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)