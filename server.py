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
        # принимаем данные с формы
        data = request.form.to_dict()

        # IP клиента
        ip_addr = request.headers.get("X-Forwarded-For", request.remote_addr)

        payload = {
            "affc": "AFF-O20FT4UUAO",
            "bxc": "BX-CL0XOBD3BRQ48",
            "vtc": "VT-HP8XSRMKVS6E7",

            "profile": {
                "firstName": data.get("firstName", ""),
                "lastName": data.get("lastName", ""),
                "email": data.get("email", ""),
                "password": data.get("password", "Qwerty123!"),
                "phone": data.get("phone", "").replace("+", "")
            },

            "ip": ip_addr,

            # 🔥 ВОРОНКА, КОТОРУЮ ТЫ ПРОСИЛ
            "funnel": "AtomKz",

            # обязательно должен быть валидный URL лендинга
            "landingURL": "https://mercedes-4371.onrender.com",

            # GEO — обязательно двухбуквенный код
            "geo": data.get("geo", "US"),

            "lang": "en",
            "landingLang": "en",

            # optional
            "comment": data.get("comment", None),
            "subId": data.get("subid", None)
        }

        headers = {
            "Authorization": "Api-Key 53486a07-a2fc-4811-9375-a4eb919f0cec",
            "Content-Type": "application/json"
        }

        url = "https://symbios.hn-crm.com/api/v1/lead/create"

        response = requests.post(url, json=payload, headers=headers)

        return jsonify({
            "success": response.status_code == 200,
            "status": response.status_code,
            "crm_response": response.text
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)