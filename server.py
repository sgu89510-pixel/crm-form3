from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/send_lead", methods=["POST"])
def send_lead():
    data = request.json

    payload = {
        "name": data.get("name"),
        "phone": data.get("phone"),
        "country": data.get("country"),
        "car_year": data.get("car_year"),
        "comment": data.get("comment")
    }

    try:
        resp = requests.post(
            "https://ilyadudin001.amocrm.ru/import_lead.php",
            data=payload,
            timeout=15
        )

        return jsonify({
            "crm_response": resp.text,
            "crm_status": resp.status_code,
            "success": resp.ok
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)