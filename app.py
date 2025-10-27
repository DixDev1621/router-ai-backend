from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend connection

# 🔑 PolygonScan API Key
API_KEY = "12ZRKG2A616KXZXHYUHBFCBX1D1PKGM8WN"  # Polygonscan key

# 🧠 Helper function to get transactions from PolygonScan
def get_transactions(wallet):
    """
    Fetch last 20 Polygon transactions using PolygonScan API
    """
    url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={wallet}&sort=desc&apikey={API_KEY}"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
        if "result" not in data or not isinstance(data["result"], list):
            return []
        return data["result"]
    except Exception as e:
        print("❌ API Error:", e)
        return []

@app.route("/check_wallet", methods=["POST"])
def check_wallet():
    """
    Check wallet risk based on its last few transactions
    """
    data = request.get_json()
    wallet_address = data.get("walletAddress")

    if not wallet_address:
        return jsonify({"error": "No wallet address provided"}), 400

    wallet = wallet_address.strip().lower()
    txs = get_transactions(wallet)

    if not txs:
        return jsonify({
            "message": "⚠ Could not retrieve transaction history. Defaulting to low risk.",
            "risk": "low"
        })

    total_incoming = 0
    total_outgoing = 0

    for tx in txs[:20]:
        try:
            value = int(tx.get("value", "0")) / 1e18  # wei → MATIC
            to_addr = tx.get("to", "").lower()
            from_addr = tx.get("from", "").lower()

            if to_addr == wallet:
                total_incoming += value
            else:
                total_outgoing += value
        except Exception:
            continue

    # 🧩 Simple AI-like Risk Rules
    tx_count = len(txs)

    if total_incoming > 50 or tx_count > 30:
        risk = "high"
        message = "🚨 High Risk: Unusual inflow or large transaction volume detected!"
    elif total_incoming > 5 or total_outgoing > 5:
        risk = "medium"
        message = "⚠ Medium Risk: Moderate wallet activity observed."
    else:
        risk = "low"
        message = "✅ Low Risk: Normal wallet activity detected."

    return jsonify({
        "message": message,
        "risk": risk,
        "incoming": round(total_incoming, 3),
        "outgoing": round(total_outgoing, 3),
        "tx_count": tx_count
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
