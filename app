from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def fetch_country_data():
    try:
        response = requests.get("https://www.travel-advisory.info/api")
        response.raise_for_status()
        data = response.json()
        return data.get("data", {})
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return {}

def lookup_country(country_code, country_data):
    if country_code in country_data:
        return country_data[country_code]["name"]
    else:
        return f"Country code '{country_code}' not found."

@app.route("/health")
def health():
    return "Service is healthy"

@app.route("/diag")
def diag():
    api_status = {"api_status": {"code": 200, "status": "ok"}}
    return jsonify(api_status)

@app.route("/convert")
def convert():
    country_code = request.args.get("countryCode")
    country_data = fetch_country_data()
    country_name = lookup_country(country_code, country_data)
    return jsonify({"countryName": country_name})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
