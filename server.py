from flask import Flask, request
import requests
import random
import string

app = Flask(__name__)

API_URL = "https://bestcliq.tech/api/v1/AddLead"
API_KEY = "3f50a5cd6aba6f7cf9be37684d359190"

MAP_ID = 4175
CAMPAIGN = "RuAutoEU"

def generate_password():
    # Минимум 8 символов, заглавная буква + спецсимвол
    return "A@" + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route("/")
def index():
    return open("lead_form.html", encoding="utf-8").read()

@app.route("/submit", methods=["POST"])
def submit():
    payload = {
        "api_key": API_KEY,
        "map_id": MAP_ID,
        "email": request.form.get("email"),
        "first_name": request.form.get("first_name"),
        "second_name": request.form.get("second_name"),
        "phone": request.form.get("phone"),
        "country": "ru",            # ✅ geo маленькими буквами
        "language": "ru",
        "campaign": CAMPAIGN,
        "description": "Лид с лендинга",
        "password": generate_password()
    }

    try:
        response = requests.post(API_URL, data=payload, timeout=15)
        result = response.json()
    except Exception as e:
        return f"Ошибка отправки заявки: {str(e)}", 500

    if response.status_code == 200:
        return """
        <h2>Спасибо!</h2>
        <p>Ваша заявка успешно отправлена.</p>
        <p>Менеджер свяжется с вами в ближайшее время.</p>
        """
    else:
        return f"Ошибка API: {result}", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)