from flask import Flask, render_template, request
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/crack", methods=["POST"])
def crack():
    pdf_file = request.files.get("pdfFile")
    pattern = request.form.get("pattern").upper()

    if len(pattern) != 4 or not pattern.isalpha():
        return render_template("result.html", success=False, message="Invalid pattern! Please provide exactly 4 capital letters.")

    pdf_path = f"uploads/{pdf_file.filename}"
    pdf_file.save(pdf_path)

    password_found = None
    for year in range(1910, 2025):
        password = f"{pattern}{year}"
        try:
            reader = PdfReader(pdf_path)
            reader.decrypt(password)
            password_found = password
            break
        except:
            continue

    if password_found:
        return render_template("result.html", success=True, password=password_found)
    else:
        return render_template("result.html", success=False, message="Password not found!")

if __name__ == "__main__":
    app.run(debug=True)
