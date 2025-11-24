from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# 1 — отдаём HTML форму
@app.route("/")
def index():
    return send_from_directory("", "lead_form.html")


# 2 — принимаем данные формы и отправляем на их PHP endpoint
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.json
        
        # Достаём данные из формы
        payload = {
            "name": data.get("name", ""),
            "country": data.get("country", ""),
            "phone": data.get("phone", ""),
            "car_year": data.get("car_year", ""),
            "comment": data.get("comment", "")
        }

        # Их PHP endpoint — принимает ТОЛЬКО form-data !!!
        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        response = requests.post(CRM_URL, data=payload)

        return jsonify({
            "success": True,
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# 3 — Render host
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)