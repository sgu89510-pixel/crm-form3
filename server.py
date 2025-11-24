from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# ===== 1. ОТДАЁМ lead_form.html =====
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


# ===== 2. ПРИЁМ ДАННЫХ ИЗ ФОРМЫ =====
@app.route("/submit", methods=["POST"])
def submit():
    try:
        # Берём form-data
        name = request.form.get("name", "")
        lastname = request.form.get("lastname", "")
        country = request.form.get("country", "")
        phone = request.form.get("phone", "")
        car_year = request.form.get("car_year", "")
        comment = request.form.get("comment", "")

        # Формируем то, что примет их PHP
        payload = {
            "name": f"{name} {lastname}",
            "country": country,
            "phone": phone,
            "car_year": car_year,
            "comment": comment
        }

        # URL их API (тот, что прислал IT Support)
        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        # ОТПРАВКА ДАННЫХ КАК form-data
        response = requests.post(CRM_URL, data=payload)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ===== 3. ДЛЯ РАБОТЫ НА RENDER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)