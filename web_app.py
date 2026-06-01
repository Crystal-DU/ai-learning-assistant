from flask import Flask, render_template, request
from pypdf import PdfReader
from pptx import Presentation
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""

    if request.method == "POST":
        note = request.form.get("note", "")

        # URL import
        url = request.form.get("url", "")
        if url:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style"]):
                tag.decompose()

            # Try to find the main content of the page
            article = soup.find("main") or soup.find("article") or soup.find("div", id="mw-content-text")
            if article:
                note = article.get_text(separator="\n")
            else:
                note = soup.get_text(separator="\n")

            # Clean the note by removing short lines
            lines = note.splitlines()
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if len(line) > 40:
                    cleaned_lines.append(line)
            note = "\n".join(cleaned_lines)

        # File import
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            filename = uploaded_file.filename.lower()

            if filename.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                note = ""

                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        note += text + "\n"

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