from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Server is running"


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    name = data.get("name", "")
    country = data.get("country", "")
    phone = data.get("phone", "")
    car_year = data.get("car_year", "")
    comment = data.get("comment", "")

    amo_url = "https://ilyadudin001.amocrm.ru/api/v4/contacts"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJh..."
    }

    payload = [
        {
            "first_name": name,
            "custom_fields_values": [
                {"field_id": 271316, "values": [{"value": country}]},
                {"field_id": 271317, "values": [{"value": phone}]},
                {"field_id": 271318, "values": [{"value": car_year}]},
                {"field_id": 271319, "values": [{"value": comment}]},
            ]
        }
    ]

    try:
        r = requests.post(amo_url, headers=headers, json=payload)
        return jsonify({
            "success": r.ok,
            "crm_status": r.status_code,
            "crm_response": r.text
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)