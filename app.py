# app.py
from flask import Flask, request, render_template, send_from_directory
import os
from signer_engine import sign_pdf

app = Flask(__name__)

UPLOAD_DIR = "input_docs"
SIGNED_DIR = "signed_docs"
LOG_DIR = "logs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SIGNED_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("pdf_file")
        if not uploaded_file:
            return "No PDF file uploaded", 400

        filename = uploaded_file.filename
        input_path = os.path.join(UPLOAD_DIR, filename)
        output_path = os.path.join(SIGNED_DIR, f"signed_{filename}")
        log_path = os.path.join(LOG_DIR, "signer.log")
        audit_path = os.path.join(LOG_DIR, "audit_log.csv")

        uploaded_file.save(input_path)

        sign_pdf(input_path, output_path, log_path, audit_path)

        return render_template("index.html", file=f"signed_{filename}")
    return render_template("index.html")

@app.route("/signed/<filename>")
def download(filename):
    return send_from_directory(SIGNED_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)
