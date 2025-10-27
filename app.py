from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = "12ZRKG2A616KXZXHYUHBFCBX1D1PKGM8WN"  # PolygonScan Key

def get_transactions(wallet):
    url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={wallet}&sort=desc&apikey={API_KEY}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        print("🔍 API Response:", data)  # Debug
        if data.get("status") == "1" and "result" in data:
            return data["result"]
        else:
            print("⚠️ No valid transaction data.")
            return []
    except Exception as e:
        print("❌ Error fetching data:", e)
        return []

@app.route("/check_wallet", methods=["POST"])
def check_wallet():
    data = request.get_json()
    wallet = data.get("walletAddress", "").strip().lower()
    if not wallet:
        return jsonify({"error": "No wallet address provided"}), 400

    txs = get_transactions(wallet)

    if not txs:
        return jsonify({
            "message": "⚠ No transaction data found – API may be slow or wallet inactive.",
            "risk": "low"
        })

    total_incoming = 0
    total_outgoing = 0
    tx_count = len(txs)

    for tx in txs[:30]:  # check last 30
        try:
            value = int(tx.get("value", "0")) / 1e18
            to_addr = tx.get("to", "").lower()
            from_addr = tx.get("from", "").lower()
            if to_addr == wallet:
                total_incoming += value
            elif from_addr == wallet:
                total_outgoing += value
        except:
            continue

    # Better AI-style rules
    if total_incoming > 100 or tx_count > 50:
        risk = "high"
        message = "🚨 High Risk: Heavy or unusual transaction activity detected!"
    elif total_incoming > 10 or total_outgoing > 10 or tx_count > 20:
        risk = "medium"
        message = "⚠ Medium Risk: Moderate wallet activity."
    else:
        risk = "low"
        message = "✅ Low Risk: Normal wallet activity."

    return jsonify({
        "message": message,
        "risk": risk,
        "incoming": round(total_incoming, 3),
        "outgoing": round(total_outgoing, 3),
        "tx_count": tx_count
    })

@app.route("/")
def home():
    return jsonify({"message": "Risk Detection Backend is Running 🚀"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
