from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ Home route - to confirm it’s working
@app.route('/')
def home():
    return jsonify({"message": "Risk Detection Backend is Running 🚀"})

# ✅ Risk detection route
@app.route('/check_risk/<address>', methods=['GET'])
def check_risk(address):
    # ⚠️ We are swapping risk levels as you requested
    # (High -> Low, Low -> High)
    high_risk_addresses = ['0xAb8497B0f7D7E93f6E1b7cC6A98553a25E10cC12']  # example
    medium_risk_addresses = ['0xD03E4fA6e66A44D3Af5C4b73BBeed5F94F8A76C7']

    if address in high_risk_addresses:
        risk = "low"      # swapped
    elif address in medium_risk_addresses:
        risk = "medium"
    else:
        risk = "high"     # swapped

    return jsonify({"address": address, "risk": risk})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
