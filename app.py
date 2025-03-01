from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# 🔹 Haetaan Mistral API-avain ympäristömuuttujasta
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_joke", methods=["POST"])
def generate_joke():
    data = request.json
    word = data.get("word", "")

    if not word:
        return jsonify({"error": "Anna sana!"}), 400

    # 🔹 Mistral AI -kehotus (prompt), joka luo vitsin
    prompt = f"Keksi hauska ja lyhyt vitsi, jossa esiintyy sana '{word}' ja myös sana 'parru'."

    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistral-medium",  # Käytettävä Mistral-malli (tarkista dokumentaatio!)
        "messages": [
            {"role": "system", "content": "Olet hauska vitsikone."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,  # Säätelee luovuuden tasoa (0 = tarkka, 1 = hyvin luova)
        "max_tokens": 50  # Rajoittaa vastauksen pituutta
    }

    try:
        response = requests.post(MISTRAL_ENDPOINT, headers=headers, json=payload)
        response_json = response.json()

        if "choices" in response_json:
            joke = response_json["choices"][0]["message"]["content"].strip()
            return jsonify({"joke": joke})
        else:
            return jsonify({"error": "Virhe Mistral AI:n vastauksessa"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
