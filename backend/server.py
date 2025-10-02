from flask import Flask, request, jsonify
from flask_cors import CORS
from nda_assistant import extract_text_from_pdfs, ask_openai

app = Flask(__name__)
CORS(app)  # allow frontend to connect

# Extract the NDA text once on server start
context_text = extract_text_from_pdfs()

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("query", "").strip()

    if not question:
        return jsonify({"error": "No query provided"}), 400

    print(f"Received query: {question}")

    answer = ask_openai(question, context_text)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
