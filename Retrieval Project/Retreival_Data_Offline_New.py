# Offline + OpenAI PDF Flashcard Generator (Master Version)
# Requirements: pip install openai PyMuPDF pandas

import os
import time
import fitz  # PyMuPDF
import pandas as pd
import openai
from datetime import datetime

# === SETTINGS ===
MODEL = "gpt-3.5-turbo"
DELAY_BETWEEN_REQUESTS = 21  # in seconds

# === Step 1: Extract Text from PDF ===
def extract_pdf_text(pdf_path):
    text_by_page = []
    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        text_by_page.append(text)
    return text_by_page

# === Step 2: AI-Powered Flashcard Generation ===
def generate_flashcards_ai(pages, api_key):
    openai.api_key = api_key    # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
    # Requirements: pip install openai PyMuPDF pandas
    
    import os
    import fitz  # PyMuPDF
    import pandas as pd
    import openai
    from datetime import datetime
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    # === SETTINGS ===
    MODEL = "gpt-3.5-turbo"
    DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
    MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
    
    # === Step 1: Extract Text from PDF ===
    def extract_pdf_text(pdf_path):
        with fitz.open(pdf_path) as doc:
            return [page.get_text() for page in doc]
    
    # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
    def generate_flashcards_for_page(page, api_key, page_num):
        openai.api_key = api_key
        prompt = (
            f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
            f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
        )
        try:
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            content = response.choices[0].message['content']
            entries = content.split("---")
            flashcards = []
            for entry in entries:
                lines = entry.strip().split('\n')
                q, a = None, None
                for line in lines:
                    if line.lower().startswith("q:"):
                        q = line[2:].strip()
                    elif line.lower().startswith("a:"):
                        a = line[2:].strip()
                if q and a:
                    flashcards.append({"Question": q, "Answer": a})
            print(f"✅ Page {page_num + 1} processed.")
            return flashcards
        except Exception as e:
            print(f"❌ AI error on page {page_num + 1}: {e}")
            return []
    
    def generate_flashcards_ai(pages, api_key):
        flashcards = []
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
            for future in as_completed(futures):
                flashcards.extend(future.result())
        return flashcards
    
    # === Step 3: Save Flashcards to CSV ===
    def save_to_csv(cards):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"anki_cards_{timestamp}.csv"
        pd.DataFrame(cards).to_csv(output_file, index=False)
        print(f"✅ Saved {len(cards)} flashcards to {output_file}")
    
    # === Main Entry Point ===
    if __name__ == "__main__":
        pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
        if not os.path.isfile(pdf_path):
            print("❌ File not found.")
            exit(1)
    
        api_key = input("🔐 Enter your OpenAI API key: ").strip()
        pages = extract_pdf_text(pdf_path)
        cards = generate_flashcards_ai(pages, api_key)
        save_to_csv(cards)
        print("✨ Done.")        # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
        # Requirements: pip install openai PyMuPDF pandas
        
        import os
        import fitz  # PyMuPDF
        import pandas as pd
        import openai
        from datetime import datetime
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        # === SETTINGS ===
        MODEL = "gpt-3.5-turbo"
        DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
        MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
        
        # === Step 1: Extract Text from PDF ===
        def extract_pdf_text(pdf_path):
            with fitz.open(pdf_path) as doc:
                return [page.get_text() for page in doc]
        
        # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
        def generate_flashcards_for_page(page, api_key, page_num):
            openai.api_key = api_key
            prompt = (
                f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
                f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
            )
            try:
                response = openai.ChatCompletion.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )
                content = response.choices[0].message['content']
                entries = content.split("---")
                flashcards = []
                for entry in entries:
                    lines = entry.strip().split('\n')
                    q, a = None, None
                    for line in lines:
                        if line.lower().startswith("q:"):
                            q = line[2:].strip()
                        elif line.lower().startswith("a:"):
                            a = line[2:].strip()
                    if q and a:
                        flashcards.append({"Question": q, "Answer": a})
                print(f"✅ Page {page_num + 1} processed.")
                return flashcards
            except Exception as e:
                print(f"❌ AI error on page {page_num + 1}: {e}")
                return []
        
        def generate_flashcards_ai(pages, api_key):
            flashcards = []
            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
                for future in as_completed(futures):
                    flashcards.extend(future.result())
            return flashcards
        
        # === Step 3: Save Flashcards to CSV ===
        def save_to_csv(cards):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"anki_cards_{timestamp}.csv"
            pd.DataFrame(cards).to_csv(output_file, index=False)
            print(f"✅ Saved {len(cards)} flashcards to {output_file}")
        
        # === Main Entry Point ===
        if __name__ == "__main__":
            pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
            if not os.path.isfile(pdf_path):
                print("❌ File not found.")
                exit(1)
        
            api_key = input("🔐 Enter your OpenAI API key: ").strip()
            pages = extract_pdf_text(pdf_path)
            cards = generate_flashcards_ai(pages, api_key)
            save_to_csv(cards)
            print("✨ Done.")            # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
            # Requirements: pip install openai PyMuPDF pandas
            
            import os
            import fitz  # PyMuPDF
            import pandas as pd
            import openai
            from datetime import datetime
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            # === SETTINGS ===
            MODEL = "gpt-3.5-turbo"
            DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
            MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
            
            # === Step 1: Extract Text from PDF ===
            def extract_pdf_text(pdf_path):
                with fitz.open(pdf_path) as doc:
                    return [page.get_text() for page in doc]
            
            # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
            def generate_flashcards_for_page(page, api_key, page_num):
                openai.api_key = api_key
                prompt = (
                    f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
                    f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
                )
                try:
                    response = openai.ChatCompletion.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.5
                    )
                    content = response.choices[0].message['content']
                    entries = content.split("---")
                    flashcards = []
                    for entry in entries:
                        lines = entry.strip().split('\n')
                        q, a = None, None
                        for line in lines:
                            if line.lower().startswith("q:"):
                                q = line[2:].strip()
                            elif line.lower().startswith("a:"):
                                a = line[2:].strip()
                        if q and a:
                            flashcards.append({"Question": q, "Answer": a})
                    print(f"✅ Page {page_num + 1} processed.")
                    return flashcards
                except Exception as e:
                    print(f"❌ AI error on page {page_num + 1}: {e}")
                    return []
            
            def generate_flashcards_ai(pages, api_key):
                flashcards = []
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
                    for future in as_completed(futures):
                        flashcards.extend(future.result())
                return flashcards
            
            # === Step 3: Save Flashcards to CSV ===
            def save_to_csv(cards):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"anki_cards_{timestamp}.csv"
                pd.DataFrame(cards).to_csv(output_file, index=False)
                print(f"✅ Saved {len(cards)} flashcards to {output_file}")
            
            # === Main Entry Point ===
            if __name__ == "__main__":
                pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
                if not os.path.isfile(pdf_path):
                    print("❌ File not found.")
                    exit(1)
        
                api_key = input("🔐 Enter your OpenAI API key: ").strip()
                pages = extract_pdf_text(pdf_path)
                cards = generate_flashcards_ai(pages, api_key)
                save_to_csv(cards)
                print("✨ Done.")                # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
                # Requirements: pip install openai PyMuPDF pandas
                
                import os
                import fitz  # PyMuPDF
                import pandas as pd
                import openai
                from datetime import datetime
                from concurrent.futures import ThreadPoolExecutor, as_completed
                
                # === SETTINGS ===
                MODEL = "gpt-3.5-turbo"
                DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
                MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
                
                # === Step 1: Extract Text from PDF ===
                def extract_pdf_text(pdf_path):
                    with fitz.open(pdf_path) as doc:
                        return [page.get_text() for page in doc]
                
                # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
                def generate_flashcards_for_page(page, api_key, page_num):
                    openai.api_key = api_key
                    prompt = (
                        f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
                        f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
                    )
                    try:
                        response = openai.ChatCompletion.create(
                            model=MODEL,
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.5
                        )
                        content = response.choices[0].message['content']
                        entries = content.split("---")
                        flashcards = []
                        for entry in entries:
                            lines = entry.strip().split('\n')
                            q, a = None, None
                            for line in lines:
                                if line.lower().startswith("q:"):
                                    q = line[2:].strip()
                                elif line.lower().startswith("a:"):
                                    a = line[2:].strip()
                            if q and a:
                                flashcards.append({"Question": q, "Answer": a})
                        print(f"✅ Page {page_num + 1} processed.")
                        return flashcards
                    except Exception as e:
                        print(f"❌ AI error on page {page_num + 1}: {e}")
                        return []
                
                def generate_flashcards_ai(pages, api_key):
                    flashcards = []
                    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                        futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
                        for future in as_completed(futures):
                            flashcards.extend(future.result())
                    return flashcards
                
                # === Step 3: Save Flashcards to CSV ===
                def save_to_csv(cards):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_file = f"anki_cards_{timestamp}.csv"
                    pd.DataFrame(cards).to_csv(output_file, index=False)
                    print(f"✅ Saved {len(cards)} flashcards to {output_file}")
                
                # === Main Entry Point ===
                if __name__ == "__main__":
                    pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
                    if not os.path.isfile(pdf_path):
                        print("❌ File not found.")
                        exit(1)
                
                    api_key = input("🔐 Enter your OpenAI API key: ").strip()
                    pages = extract_pdf_text(pdf_path)
                    cards = generate_flashcards_ai(pages, api_key)
                    save_to_csv(cards)
                    print("✨ Done.")                    # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
                    # Requirements: pip install openai PyMuPDF pandas
                    
                    import os
                    import fitz  # PyMuPDF
                    import pandas as pd
                    import openai
                    from datetime import datetime
                    from concurrent.futures import ThreadPoolExecutor, as_completed
                    
                    # === SETTINGS ===
                    MODEL = "gpt-3.5-turbo"
                    DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
                    MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
                    
                    # === Step 1: Extract Text from PDF ===
                    def extract_pdf_text(pdf_path):
                        with fitz.open(pdf_path) as doc:
                            return [page.get_text() for page in doc]
                    
                    # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
                    def generate_flashcards_for_page(page, api_key, page_num):
                        openai.api_key = api_key
                        prompt = (
                            f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
                            f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
                        )
                        try:
                            response = openai.ChatCompletion.create(
                                model=MODEL,
                                messages=[
                                    {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                                    {"role": "user", "content": prompt}
                                ],
                                temperature=0.5
                            )
                            content = response.choices[0].message['content']
                            entries = content.split("---")
                            flashcards = []
                            for entry in entries:
                                lines = entry.strip().split('\n')
                                q, a = None, None
                                for line in lines:
                                    if line.lower().startswith("q:"):
                                        q = line[2:].strip()
                                    elif line.lower().startswith("a:"):
                                        a = line[2:].strip()
                                if q and a:
                                    flashcards.append({"Question": q, "Answer": a})
                            print(f"✅ Page {page_num + 1} processed.")
                            return flashcards
                        except Exception as e:
                            print(f"❌ AI error on page {page_num + 1}: {e}")
                            return []
                    
                    def generate_flashcards_ai(pages, api_key):
                        flashcards = []
                        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                            futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
                            for future in as_completed(futures):
                                flashcards.extend(future.result())
                        return flashcards
                    
                    # === Step 3: Save Flashcards to CSV ===
                    def save_to_csv(cards):
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        output_file = f"anki_cards_{timestamp}.csv"
                        pd.DataFrame(cards).to_csv(output_file, index=False)
                        print(f"✅ Saved {len(cards)} flashcards to {output_file}")
                    
                    # === Main Entry Point ===
                    if __name__ == "__main__":
                        pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
                        if not os.path.isfile(pdf_path):
                            print("❌ File not found.")
                            exit(1)
                    
                        api_key = input("🔐 Enter your OpenAI API key: ").strip()
                        pages = extract_pdf_text(pdf_path)
                        cards = generate_flashcards_ai(pages, api_key)
                        save_to_csv(cards)
                        print("✨ Done.")                        # Offline + OpenAI PDF Flashcard Generator (Efficient Version)
                        # Requirements: pip install openai PyMuPDF pandas
                        
                        import os
                        import fitz  # PyMuPDF
                        import pandas as pd
                        import openai
                        from datetime import datetime
                        from concurrent.futures import ThreadPoolExecutor, as_completed
                        
                        # === SETTINGS ===
                        MODEL = "gpt-3.5-turbo"
                        DELAY_BETWEEN_REQUESTS = 21  # seconds (OpenAI rate limit for free tier)
                        MAX_WORKERS = 3  # Number of parallel requests (adjust based on your OpenAI plan)
                        
                        # === Step 1: Extract Text from PDF ===
                        def extract_pdf_text(pdf_path):
                            with fitz.open(pdf_path) as doc:
                                return [page.get_text() for page in doc]
                        
                        # === Step 2: AI-Powered Flashcard Generation (Parallelized) ===
                        def generate_flashcards_for_page(page, api_key, page_num):
                            openai.api_key = api_key
                            prompt = (
                                f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n"
                                f"{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
                            )
                            try:
                                response = openai.ChatCompletion.create(
                                    model=MODEL,
                                    messages=[
                                        {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                                        {"role": "user", "content": prompt}
                                    ],
                                    temperature=0.5
                                )
                                content = response.choices[0].message['content']
                                entries = content.split("---")
                                flashcards = []
                                for entry in entries:
                                    lines = entry.strip().split('\n')
                                    q, a = None, None
                                    for line in lines:
                                        if line.lower().startswith("q:"):
                                            q = line[2:].strip()
                                        elif line.lower().startswith("a:"):
                                            a = line[2:].strip()
                                    if q and a:
                                        flashcards.append({"Question": q, "Answer": a})
                                print(f"✅ Page {page_num + 1} processed.")
                                return flashcards
                            except Exception as e:
                                print(f"❌ AI error on page {page_num + 1}: {e}")
                                return []
                        
                        def generate_flashcards_ai(pages, api_key):
                            flashcards = []
                            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                                futures = {executor.submit(generate_flashcards_for_page, page, api_key, i): i for i, page in enumerate(pages)}
                                for future in as_completed(futures):
                                    flashcards.extend(future.result())
                            return flashcards
                        
                        # === Step 3: Save Flashcards to CSV ===
                        def save_to_csv(cards):
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            output_file = f"anki_cards_{timestamp}.csv"
                            pd.DataFrame(cards).to_csv(output_file, index=False)
                            print(f"✅ Saved {len(cards)} flashcards to {output_file}")
                        
                        # === Main Entry Point ===
                        if __name__ == "__main__":
                            pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
                            if not os.path.isfile(pdf_path):
                                print("❌ File not found.")
                                exit(1)
                        
                            api_key = input("🔐 Enter your OpenAI API key: ").strip()
                            pages = extract_pdf_text(pdf_path)
                            cards = generate_flashcards_ai(pages, api_key)
                            save_to_csv(cards)
                            print("✨ Done.")
    flashcards = []

    for i, page in enumerate(pages):
        print(f"🧠 Processing Page {i + 1}/{len(pages)}...")
        try:
            prompt = f"From the following study text, generate 3 question and answer pairs suitable for flashcards:\n\n{page}\n\nUse the format:\nQ: ...\nA: ...\n---"
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that writes flashcards for Anki."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            content = response.choices[0].message['content']
            entries = content.split("---")
            for entry in entries:
                lines = entry.strip().split('\n')
                q, a = None, None
                for line in lines:
                    if line.lower().startswith("q:"):
                        q = line[2:].strip()
                    elif line.lower().startswith("a:"):
                        a = line[2:].strip()
                if q and a:
                    flashcards.append({"Question": q, "Answer": a})
        except Exception as e:
            print(f"❌ AI error on page {i + 1}: {e}")
        time.sleep(DELAY_BETWEEN_REQUESTS)
    return flashcards

# === Step 3: Save Flashcards to CSV ===
def save_to_csv(cards):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"anki_cards_{timestamp}.csv"
    df = pd.DataFrame(cards)
    df.to_csv(output_file, index=False)
    print(f"✅ Saved {len(cards)} flashcards to {output_file}")

# === Main Entry Point ===
if __name__ == "__main__":
    pdf_path = input("📂 Enter path to your PDF file (.pdf): ").strip().strip('"')
    if not os.path.isfile(pdf_path):
        print("❌ File not found.")
        exit(1)

    api_key = input("🔐 Enter your OpenAI API key: ").strip()
    pages = extract_pdf_text(pdf_path)
    cards = generate_flashcards_ai(pages, api_key)
    save_to_csv(cards)
    print("✨ Done.")
