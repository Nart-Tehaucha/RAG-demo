# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from retriever import retrieve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Endpoint to handle query GET requests
@app.route("/query", methods=["GET"])
def query():
    q = request.args.get("q")
    if not q:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        hits = retrieve(q)
        return jsonify(hits)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
