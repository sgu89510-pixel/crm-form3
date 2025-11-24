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
        data = request.json

        incomingLead = {
            "name": data.get("name", "") + " " + data.get("lastname", ""),
            "country": data.get("country", ""),
            "phone": data.get("phone", ""),
            "car_year": data.get("car_year", ""),
            "comment": data.get("comment", "")
        }

        CRM_URL = "http://144.124.251.253/api/v1/Lead"

        response = requests.post(
            CRM_URL,
            json=incomingLead,                     # 👈 JSON ПРАВИЛЬНО
            headers={"Content-Type": "application/json"}  # 👈 обязательно!
        )

        return jsonify({
            "success": response.status_code in [200, 201],
            "crm_status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)