import openai
import PyPDF2
import os
import csv

# 📥 Prompt for PDF file and API key
pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
api_key = input("🔐 Enter your OpenAI API key: ").strip()

# 📄 Load and extract PDF text
if not os.path.exists(pdf_path):
    print("❌ File not found.")
    exit()

with open(pdf_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    all_text = [page.extract_text() for page in reader.pages if page.extract_text()]

openai.api_key = api_key

# 📘 Define helper to turn text into flashcards
def generate_flashcards(text, page_number):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Create 3 Anki-style flashcards based on this content (with Question and Answer format only):\n\n{text}"
            }]
        )
        content = response.choices[0].message["content"]
        print(f"✅ Page {page_number} flashcards generated.")
        return content
    except Exception as e:
        print(f"❌ OpenAI error on Page {page_number}: {e}")
        return ""

# 🧠 Process each page and store flashcards
cards = []
for i, page_text in enumerate(all_text, start=1):
    print(f"🧠 Processing Page {i}/{len(all_text)}...")
    result = generate_flashcards(page_text, i)
    for line in result.split("\n"):
        if "Q:" in line and "A:" in line:
            q = line.split("Q:")[1].split("A:")[0].strip()
            a = line.split("A:")[1].strip()
            cards.append((q, a))

# 💾 Export to CSV for Anki import
output_file = "anki_cards.csv"
with open(output_file, "w", newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Front", "Back"])
    writer.writerows(cards)

print(f"\n✅ Saved {len(cards)} flashcards to {output_file}")
