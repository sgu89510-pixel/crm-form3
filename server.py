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
        # Принимаем JSON или form-data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        if not data:
            return jsonify({"success": False, "error": "Нет данных"}), 400

        # Формируем JSON ПРАВИЛЬНО для CRM
        payload = {
            "name": data.get("name", ""),
            "country": data.get("country", ""),
            "phone": data.get("phone", ""),
            "car_year": data.get("car_year", ""),
            "comment": data.get("comment", "")
        }

        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # ВАЖНО ❗ ТУТ ДОЛЖНО БЫТЬ json=payload
        response = requests.post(CRM_URL, json=payload, headers=headers)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)