from pathlib import Path

input_dir = Path("input")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

files = list(input_dir.glob("*.txt")) + list(input_dir.glob("*.md"))

if not files:
    print("No input files found.")
    exit()

for file in files:
    note = file.read_text()

    summary = "# AI Learning Summary\n\n"
    summary += f"## Source File\n- {file.name}\n\n"

    summary += "## Key Takeaways\n"
    sentences = note.replace("\n", " ").split(".")

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            summary += f"- {sentence}\n"

    summary += "\n## Next Actions\n"
    for sentence in sentences:
        lower_sentence = sentence.lower()
        if "next" in lower_sentence or "review" in lower_sentence or "complete" in lower_sentence:
            summary += f"- {sentence.strip()}\n"

    output_file = output_dir / f"{file.stem}_summary.md"
    output_file.write_text(summary)

    print(f"Generated: {output_file}")