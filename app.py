from flask import Flask, render_template, request, redirect, session, url_for, send_file
from docx import Document
from io import BytesIO
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Можно заменить
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# 👥 Пользователи: логин → хэш пароля
users = {
    "admin": generate_password_hash("admin123"),
    "worker": generate_password_hash("work2025")
}

def replace_text_preserve_style(paragraph, mapping):
    for run in paragraph.runs:
        for key, value in mapping.items():
            if key in run.text:
                run.text = run.text.replace(key, value)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect(url_for("form"))
        else:
            return render_template("login.html", error="Неверный логин или пароль")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def form():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        doc = Document("template.docx")
        fields = {f"{{{field}}}": request.form.get(field, "") for field in [
            "akt_number", "akt_date", "object_description", "contractor_name",
            "contractor_rep", "tech_rep", "author_rep", "additional_rep",
            "work_description", "project_docs", "materials", "proof",
            "deviations", "start_date", "end_date", "next_work"
        ]}

        for paragraph in doc.paragraphs:
            replace_text_preserve_style(paragraph, fields)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        replace_text_preserve_style(paragraph, fields)

        output = BytesIO()
        doc.save(output)
        output.seek(0)
        return send_file(output, as_attachment=True, download_name="akt.docx")

    return render_template("form.html", username=session['user'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)