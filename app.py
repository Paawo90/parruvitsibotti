from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# 🔹 Haetaan OpenAI API-avain ympäristömuuttujasta
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_joke", methods=["POST"])
def generate_joke():
    data = request.json
    word = data.get("word", "")

    if not word:
        return jsonify({"error": "Anna sana!"}), 400

    # 🔹 GPT-kehotus (prompt), joka luo vitsin
    prompt = f"Keksi hauska ja lyhyt vitsi, jossa esiintyy sana '{word}' ja myös sana 'parru'."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Olet hauska vitsikone."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Hallitsee luovuuden tasoa (0 = täysin tarkka, 1 = täysin luova)
            max_tokens=50  # Rajoittaa vastauksen pituutta
        )
        joke = response["choices"][0]["message"]["content"].strip()
        return jsonify({"joke": joke})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")  # 🔹 Tämä varmistaa, että Flask toimii myös Renderissä
