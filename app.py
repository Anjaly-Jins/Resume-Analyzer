from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    resume = request.files["resume"]

    if resume:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
        resume.save(filepath)

        reader = PdfReader(filepath)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return render_template(
            "index.html",
            extracted_text=text
        )

    return "No file uploaded"

if __name__ == "__main__":
    app.run(debug=True)