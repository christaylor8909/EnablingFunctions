# Offline PDF to Flashcard Generator (No OpenAI)
# Requires: pip install PyMuPDF genanki pandas

import fitz  # PyMuPDF
import pandas as pd
import genanki
import os

# === Step 1: Extract Text from PDF ===
def extract_pdf_text(pdf_path):
    text_by_page = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        text_by_page.append(text)
    return text_by_page

# === Step 2: Simple Rule-based Flashcard Extraction ===
def generate_flashcards(text_pages):
    cards = []
    for i, text in enumerate(text_pages):
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 5]
        for j in range(len(lines)-1):
            question = lines[j]
            answer = lines[j+1]
            if '?' in question or ':' in question or len(answer.split()) > 3:
                cards.append({"Question": question, "Answer": answer})
    return cards

# === Step 3: Save to CSV ===
def save_to_csv(cards, output_file):
    df = pd.DataFrame(cards)
    df.to_csv(output_file, index=False)
    print(f"✅ Saved {len(cards)} flashcards to {output_file}")

# === Step 4: Export to Anki Deck (.apkg) ===
def export_to_anki(cards, deck_name="AI Flashcards", output_file="anki_deck.apkg"):
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[{'name': 'Question'}, {'name': 'Answer'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}'
        }]
    )

    deck = genanki.Deck(2059400110, deck_name)
    for card in cards:
        note = genanki.Note(model=model, fields=[card['Question'], card['Answer']])
        deck.add_note(note)

    genanki.Package(deck).write_to_file(output_file)
    print(f"🧠 Anki deck saved to {output_file}")

# === Main Script ===
if __name__ == "__main__":
    pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')

    if not os.path.isfile(pdf_path):
        print("❌ File not found.")
        exit(1)

    pages = extract_pdf_text(pdf_path)
    cards = generate_flashcards(pages)

    save_to_csv(cards, "anki_cards.csv")
    export_to_anki(cards)

    print("✨ Done.")
