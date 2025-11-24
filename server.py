from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# === 1. ОТДАЁМ lead_form.html ПРЯМО ПО АДРЕСУ "/" ===
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


# === 2. ПРИЁМ ДАННЫХ ИЗ ФОРМЫ ===
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

        # Формат, который требует их сервер:
        incomingLead = {
            "name": f"{name} {lastname}",
            "country": country,
            "phone": phone,
            "car_year": car_year,
            "comment": comment
        }

        # === ОЧЕНЬ ВАЖНО ===
        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        # <<< ДОБАВЛЕНО ЛОГИРОВАНИЕ >>>
        print("⏳ Отправляем на CRM:")
        print(incomingLead)

        response = requests.post(CRM_URL, json=incomingLead)

        print("📩 CRM ответила статусом:", response.status_code)
        print("📨 Текст ответа CRM:", response.text)

        return jsonify({
            "success": response.status_code == 200,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        print("🔥 Ошибка сервера:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# === 3. ДЛЯ РАБОТЫ НА RENDER ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)