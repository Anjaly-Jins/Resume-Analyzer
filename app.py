from flask import Flask, render_template, request
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# --------------------------
# Landing Page
# --------------------------
@app.route("/")
def landing():
    return render_template("landing.html")


# --------------------------
# Upload Page
# --------------------------
@app.route("/upload")
def upload_page():
    return render_template("upload.html")


# --------------------------
# Analyze Resume
# --------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")
    job_description = request.form.get("job_description", "")

    if not resume or resume.filename == "":
        return render_template(
            "upload.html",
            error="Please upload a resume."
        )

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    reader = PdfReader(filepath)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    documents = [resume_text, job_description]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    match_score = round(similarity * 100, 2)

    resume_lower = resume_text.lower()
    job_lower = job_description.lower()

    resume_skills = set()
    job_skills = set()

    for skill in SKILLS:

        skill = skill.lower()

        if skill in resume_lower:
            resume_skills.add(skill)

        if skill in job_lower:
            job_skills.add(skill)

    matching_skills = sorted(
        resume_skills.intersection(job_skills)
    )

    missing_skills = sorted(
        job_skills - resume_skills
    )

    recommendations = []

    for skill in missing_skills:
        recommendations.append(
            f"Consider learning or highlighting '{skill}'."
        )

    if match_score < 40:

        recommendations.append(
            "Your resume has a low ATS match. Add more relevant keywords."
        )

    elif match_score < 70:

        recommendations.append(
            "Good foundation. Improve keyword alignment."
        )

    else:

        recommendations.append(
            "Excellent ATS compatibility."
        )

    return render_template(

        "results.html",

        match_score=match_score,

        resume_text=resume_text,

        matching_skills=matching_skills,

        missing_skills=missing_skills,

        recommendations=recommendations

    )


if __name__ == "__main__":
    app.run(debug=True)