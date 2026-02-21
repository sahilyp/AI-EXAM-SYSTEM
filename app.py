from flask import Flask, render_template, request, redirect, session, jsonify
from supabase_client import supabase
from functools import wraps
import spacy, random, io, os
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ================= SETUP =================
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "exam_secret")

nlp = spacy.load("en_core_web_sm")

# ================= AUTH DECORATOR =================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/auth")
        return f(*args, **kwargs)
    return wrapper

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")

# ================= AUTH =================
@app.route("/auth")
def auth():
    return render_template("auth.html")

@app.route("/login", methods=["POST"])
def login():
    try:
        res = supabase.auth.sign_in_with_password({
            "email": request.form["email"],
            "password": request.form["password"]
        })
        session["user_id"] = res.user.id
        return redirect("/dashboard")
    except Exception:
        return render_template("auth.html", error="Invalid credentials")

@app.route("/signup", methods=["POST"])
def signup():
    try:
        supabase.auth.sign_up({
            "email": request.form["email"],
            "password": request.form["password"]
        })
        return render_template("auth.html",
            message="Verify email before login")
    except Exception:
        return render_template("auth.html", error="Signup failed")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================= DASHBOARD =================
@app.route("/dashboard")
@login_required
def dashboard():
    tests = supabase.table("tests") \
        .select("*") \
        .eq("user_id", session["user_id"]) \
        .order("created_at", desc=True) \
        .execute()
    return render_template("dashboard.html", tests=tests.data)

# ================= GENERATOR =================
@app.route("/generator")
@login_required
def generator():
    return render_template("index.html")

# ================= START TEST =================
@app.route("/test", methods=["POST"])
@login_required
def test():
    text = ""
    for file in request.files.getlist("files[]"):
        if file.filename.endswith(".pdf"):
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        else:
            text += file.read().decode("utf-8")

    session["difficulty"] = request.form["difficulty"]
    session["question_type"] = request.form["question_type"]

    questions = generate_questions(
        text,
        int(request.form["num_questions"]),
        request.form["question_type"]
    )

    session["questions"] = questions
    return redirect("/quiz")

# ================= QUIZ =================
@app.route("/quiz")
@login_required
def quiz():
    difficulty = session["difficulty"]
    time_map = {"easy": 60, "medium": 120, "hard": 180}
    questions = session["questions"]
    total_time = len(questions) * time_map[difficulty]

    return render_template(
        "quiz.html",
        questions=questions,
        difficulty=difficulty,
        total_time=total_time
    )

# ================= SAVE RESULT =================
@app.route("/save_result", methods=["POST"])
@login_required
def save_result():
    data = request.json

    pdf_url = ""

    try:
        pdf_buffer = generate_pdf(data)
        filename = f"{session['user_id']}_{random.randint(1000,9999)}.pdf"

        # upload to storage
        supabase.storage.from_("pdfs").upload(
            filename,
            pdf_buffer.getvalue(),
            {"content-type": "application/pdf"}
        )

        # get public URL correctly
        pdf_data = supabase.storage.from_("pdfs").get_public_url(filename)
        pdf_url = pdf_data.get("publicURL") if isinstance(pdf_data, dict) else pdf_data

        print("PDF URL:", pdf_url)

    except Exception as e:
        print("PDF upload error:", e)

    # 🔥 always insert DB row
    supabase.table("tests").insert({
        "user_id": session["user_id"],
        "score": data["score"],
        "total": data["total"],
        "grade": data["grade"],
        "difficulty": data["difficulty"],
        "pdf_url": pdf_url
    }).execute()

    print("Saved to DB")

    return jsonify({"ok": True})
# ================= HISTORY =================
@app.route("/history")
@login_required
def history():
    tests = supabase.table("tests") \
        .select("*") \
        .eq("user_id", session["user_id"]) \
        .order("created_at", desc=True) \
        .execute()

    return render_template("history.html", tests=tests.data)

# ================= QUESTION GENERATOR =================
def generate_questions(text, n, qtype):
    doc = nlp(text)
    sentences = [s.text for s in doc.sents if len(s.text.split()) > 6]
    random.shuffle(sentences)

    questions = []
    for sent in sentences:
        if len(questions) >= n:
            break

        tokens = nlp(sent)
        nouns = [t.text for t in tokens if t.pos_ in ["NOUN", "PROPN"]]
        if len(nouns) < 2:
            continue

        answer = random.choice(nouns)

        if qtype == "mcq":
            distractors = list(set(nouns) - {answer})
            if len(distractors) < 3:
                continue
            options = [answer] + distractors[:3]
            random.shuffle(options)
            questions.append({
                "type": "mcq",
                "question": sent.replace(answer, "______", 1),
                "options": options,
                "correct": options.index(answer)
            })

        elif qtype == "fill":
            questions.append({
                "type": "fill",
                "question": sent.replace(answer, "______", 1),
                "answer": answer
            })

        elif qtype == "qa":
            questions.append({
                "type": "qa",
                "question": f"Explain: {sent}",
                "answer": answer
            })

    return questions

# ================= PDF =================
def generate_pdf(data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 60

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "AI Exam Result Report")

    y -= 30
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Score: {data['score']} / {data['total']}")
    y -= 18
    c.drawString(50, y, f"Grade: {data['grade']}")

    y -= 25

    def wrap(text, x, y, max_width=470, lh=14):
        words = text.split()
        line = ""

        for w in words:
            test = line + w + " "
            if c.stringWidth(test, "Helvetica", 11) < max_width:
                line = test
            else:
                c.drawString(x, y, line)
                y -= lh
                line = w + " "

        if line:
            c.drawString(x, y, line)
            y -= lh

        return y

    for i, q in enumerate(data["questions"], 1):

        if y < 120:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - 60

        c.setFont("Helvetica-Bold", 11)
        y = wrap(f"Q{i}. {q['question']}", 50, y)

        c.setFont("Helvetica", 11)
        y = wrap(f"Your Answer: {q['user']}", 60, y)

        y = wrap(f"Correct Answer: {q['correct']}", 60, y)

        y -= 8

    c.save()
    buffer.seek(0)
    return buffer
# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)
