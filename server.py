from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)


# === ОТДАЕМ lead_form.html ПО АДРЕСУ "/" ===
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


# === ПРИЕМ ДАННЫХ ИЗ ФОРМЫ ===
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

        # Формируем массив как в PHP
        incomingLead = {
            "name": f"{name} {lastname}",
            "country": country,
            "phone": phone,
            "car_year": car_year,
            "comment": comment
        }

        # >>> ВАЖНО: твой PHP import_lead.php принимает JSON <<<
        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        response = requests.post(
            CRM_URL,
            json=incomingLead,                       # 👈 JSON отправка
            headers={"Content-Type": "application/json"}
        )

        return jsonify({
            "success": response.status_code == 200,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# === Запуск на Render ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)