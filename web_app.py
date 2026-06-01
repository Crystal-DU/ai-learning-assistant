from flask import Flask, render_template, request
from pathlib import Path
from pypdf import PdfReader
from pptx import Presentation

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    #如果用户上传文件，则读取文件内容，覆盖文本框内容
    if request.method == "POST":
        note = request.form.get("note", "")

    #文件读取
    uploaded_file = request.files.get("file")
    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()

        #根据文件类型读取内容
        if filename.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            note = ""

            #txt
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    note += text + "\n"

        #pptx
        elif filename.endswith(".pptx"):
            presentation = Presentation(uploaded_file)
            note = ""

            for slide_number, slide in enumerate(presentation.slides, start=1):
                note += f"\n--- Slide {slide_number} ---\n"

                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text = shape.text.strip()
                        if text:
                            note += text + "\n"

        else:
            note = uploaded_file.read().decode("utf-8")

        prompt = f"""
# AI Learning Assistant Prompt

You are an AI learning assistant.

Please analyze the following learning note and generate a structured summary.

## Topics Learned
- List the main topics.

## Key Takeaways
- Summarize the important points.

## Action Items
- List next actions or things to review.

## Interview Talking Points
- Explain how I can describe this learning experience in a professional setting.

## Learning Note

{note}
"""

    return render_template("index.html", prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)