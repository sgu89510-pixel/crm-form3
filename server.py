from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import random
import string

app = Flask(__name__)

# Генерация валидного пароля
def generate_password():
    letters = string.ascii_letters
    digits = string.digits
    special = "!@#$%^&*"
    pwd = ''.join(random.choice(letters) for _ in range(5))
    pwd += random.choice(digits)
    pwd += random.choice(special)
    return pwd

@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.form.to_dict()

        # Проверка данных
        required = ["first_name", "second_name", "phone", "email"]
        for r in required:
            if not data.get(r):
                return jsonify({"success": False, "error": f"Missing field: {r}"}), 400

        # IP пользователя
        forwarded = request.headers.get("X-Forwarded-For", "")
        ip = forwarded.split(",")[0] if forwarded else request.remote_addr

        # Тело запроса
        payload = {
            "api_key": "3f50a5cd6aba6f7cf9be37684d359190",
            "map_id": 4175,
            "email": data["email"],
            "first_name": data["first_name"],
            "second_name": data["second_name"],
            "phone": data["phone"].replace("+", "").strip(),
            "country": "ru",
            "language": "en",
            "campaign": "RuAutoEU",
            "description": "Auto lead from RU",
            "password": generate_password()
        }

        url = "https://bestcliq.tech/api/v1/AddLead"

        response = requests.post(url, data=payload)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text,
            "sent_payload": payload
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
