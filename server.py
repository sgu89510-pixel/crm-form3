from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AMO_DOMAIN = "ilyadudin001.amocrm.ru"
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImMxYTZiODQ1OTJlODBjNDYyMTZlZTU1NmM3NzI0YWIwMTZiODQ0ODE3NWU1NWY3ZWM5Y2UxMjgyNzJlYzZkNWVlOTRlM2RhY2EyZjQ3Mjg2In0.eyJhdWQiOiIzMDY5MzJkZC02NzIxLTRjMDYtODlhZC1hMjFiZTcwYjE5OTAiLCJqdGkiOiJjMWE2Yjg0NTkyZTgwYzQ2MjE2ZWU1NTZjNzcyNGFiMDE2Yjg0NDgxNzVlNTVmN2VjOWNlMTI4MjcyZWM2ZDVlZTk0ZTNkYWNhMmY0NzI4NiIsImlhdCI6MTc2MzExODI0MywibmJmIjoxNzYzMTE4MjQzLCJleHAiOjE3OTg3NjE2MDAsInN1YiI6IjEzMjEzNTM4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyNzY0MjkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiZDI0NDM5YTctZDU2Zi00ZjZjLWJlOWMtMzhhMzRlZjQ2ZThkIiwidXNlcl9mbGFncyI6MCwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.WooSHPw6yZyrtQGnLCUAlTV7n_jP5RdnmoHGdMs1QuhIdNWQIwgd5ZwmZaSqU5n57WbAmiYcziqT1qnsHQc_9ohxQpYx1HaO9Pf1hUtL-YYlf2uXSLwvKyuQxz1oPgsRxv-r4yRfyTgbv3lMr6qbRhI2MyQKhB0paFM8TgYY9IlDzCaqLRmmt8RggntruhFCmRBV14yWQoobwZPFtZfes40iR1H7PjYD6w3zJAbhFfP7cYsbzcif4PCI1VLm_LGEB5EpVnpPnEXQDnDMO7kx1gLmJhpGj1dLZLyVmdsgb-W_3jonTsZdSPXZSNb6ySQlYnwsOsYN13WvyzTNtRQ23w"


@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        country = data.get("country", "")
        phone = data.get("phone", "")
        year = data.get("year", "")
        comment = data.get("comment", "")

        if not first_name or not phone:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        # Формируем JSON как требует amoCRM
        payload = [
            {
                "first_name": first_name,
                "last_name": last_name,
                "custom_fields_values": [
                    {"field_name": "Страна", "values": [{"value": country}]},
                    {"field_name": "Год", "values": [{"value": year}]},
                    {"field_name": "Комментарий", "values": [{"value": comment}]},
                    {"field_name": "Телефон", "values": [{"value": phone}]}
                ]
            }
        ]

        url = f"https://{AMO_DOMAIN}/api/v4/contacts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }

        crm_response = requests.post(url, json=payload, headers=headers)
        return jsonify({
            "success": crm_response.status_code == 200,
            "crm_status": crm_response.status_code,
            "crm_response": crm_response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/")
def home():
    return "Server is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)