from flask import Flask, render_template, request, send_file
from docx import Document
from io import BytesIO

app = Flask(__name__)

def replace_text_preserve_style(paragraph, mapping):
    for run in paragraph.runs:
        for key, value in mapping.items():
            if key in run.text:
                run.text = run.text.replace(key, value)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        doc = Document("template.docx")
        fields = {
            "{akt_number}": request.form.get("akt_number", ""),
            "{akt_date}": request.form.get("akt_date", ""),
            "{object_description}": request.form.get("object_description", ""),
            "{contractor_name}": request.form.get("contractor_name", ""),
            "{contractor_rep}": request.form.get("contractor_rep", ""),
            "{tech_rep}": request.form.get("tech_rep", ""),
            "{author_rep}": request.form.get("author_rep", ""),
            "{additional_rep}": request.form.get("additional_rep", ""),
            "{work_description}": request.form.get("work_description", ""),
            "{project_docs}": request.form.get("project_docs", ""),
            "{materials}": request.form.get("materials", ""),
            "{proof}": request.form.get("proof", ""),
            "{deviations}": request.form.get("deviations", ""),
            "{start_date}": request.form.get("start_date", ""),
            "{end_date}": request.form.get("end_date", ""),
            "{next_work}": request.form.get("next_work", "")
        }

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
        return send_file(output, as_attachment=True, download_name="akt_sformirovannyi.docx")

    return render_template("form.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
