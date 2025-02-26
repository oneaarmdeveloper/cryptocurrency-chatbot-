from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# fetch crypto price from CoinGecko API
def get_crypto_price(coin_id="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        price = data.get(coin_id, {}).get("usd")
        return price
    except Exception as e:
        return None

# Route to serve the chat interface
@app.route("/")
def index():
    return render_template("index.html")

# Route to process messages from the chat interface
@app.route("/message", methods=["POST"])
def handle_message():
    user_message = request.form.get("message", "").strip().lower()
    if user_message == "!price":
        price = get_crypto_price("bitcoin")
        if price:
            reply = f"Bitcoin Price: ${price}"
        else:
            reply = "Sorry, I couldn't fetch the price at the moment."
    else:
        reply = "Sorry, command not recognized."
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
