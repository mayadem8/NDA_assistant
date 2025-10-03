import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from tqdm import tqdm

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OpenAI API key not found. Add it to .env as OPENAI_API_KEY=sk-xxxx")

client = OpenAI(api_key=API_KEY)

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "backend" / "data"


def extract_text_from_pdfs():
    pdfs = sorted(DATA_DIR.glob("*.pdf"))
    if not pdfs:
        raise FileNotFoundError("No PDF files found in backend/data/. Please add NDA PDFs first.")

    all_text = ""

    print("📖 Extracting text from PDFs...")
    for pdf in tqdm(pdfs, desc="Parsing PDFs"):
        reader = PdfReader(str(pdf))
        pdf_text = ""
        for page in reader.pages:
            page_text = page.extract_text() or ""
            pdf_text += page_text + "\n"

        # Add filename for clarity
        all_text += f"\n---\nDocument: {pdf.name}\n{pdf_text}\n"

    print("✅ Text extraction complete.")
    return all_text.strip()


def ask_openai(question, context_text):
    prompt = (
    "You are an NDA document assistant.\n"
    "I will provide a text extracted from a bunch of NDA documents. You must ONLY use this provided text to answer questions.\n"
    "The assistant's job is to help users figure out if their company has an NDA with specific companies or persons.\n"
    "If the match is found, return names of signatories or companies exactly as they appear in the text, and NDA start/stop dates if available.\n"
    "If the match cannot be found, respond with exactly: 'No NDA found'.\n\n"
    "Rules:\n"
    "1. Do NOT use outside knowledge.\n"
    "2. Do NOT guess or make assumptions.\n"
    "3. Return answer without any extra explanations.\n"
    "4. If there are multiple possible answers, separate them with commas.\n\n"
    f"Context:\n{context_text}\n\n"
    f"Question: {question}\n"
    "Answer:"
)

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.output_text


def main():
    print("🚀 NDA Assistant starting...")

    # Step 1: Extract text
    context_text = extract_text_from_pdfs()

    # Step 2: Interactive Q&A
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        print("\nThinking...\n")
        answer = ask_openai(question, context_text)
        print("Answer:\n", answer)

if __name__ == "__main__":
    main()
