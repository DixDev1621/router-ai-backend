from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow cross-site access

@app.route('/checkRisk', methods=['GET'])
def check_risk():
    wallet = request.args.get('wallet', '')
    if not wallet:
        return jsonify({"risk": "error", "message": "No wallet provided"})

    # simple demo logic
    if wallet.lower().startswith("0x13c0"):
        return jsonify({"risk": "high", "message": "⚠️ High Risk: Suspicious wallet detected!"})
    elif wallet.lower().startswith("0x68d"):
        return jsonify({"risk": "medium", "message": "🟡 Medium Risk: Use caution."})
    else:
        return jsonify({"risk": "low", "message": "🟢 Safe: No suspicious activity found."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
