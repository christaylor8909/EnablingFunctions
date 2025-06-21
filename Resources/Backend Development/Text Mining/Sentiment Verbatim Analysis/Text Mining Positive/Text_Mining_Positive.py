import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download nltk resources
nltk.download('punkt')
nltk.download('stopwords')

# Load data
file_path = r"C:\Users\t0355lp\.vscode\Python\InterviewSummaryData.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

df.columns = df.columns.map(lambda x: str(x).strip().replace('\u00A0', '').replace('\n', '').lower())

print("✅ Available columns:")
print(df.columns.tolist())

# Set verbatim column manually
verbatim_column = "q20 - final verbatim"

# Define positive categories and keywords
categories = {
    "Friendly and Helpful Staff": ["friendly", "helpful", "courteous", "kind", "attitude", "polite", "welcoming"],
    "Good Communication": ["communicate", "communication", "call", "update", "informed", "follow up"],
    "Quick and Efficient Service": ["quick", "efficient", "fast", "prompt", "on time", "timely"],
    "High Quality Work": ["quality", "good job", "perfect", "excellent", "workmanship", "well done"],
    "Fair Pricing / Good Value": ["fair", "good price", "reasonable", "value", "affordable"],
    "Easy Booking / Availability": ["easy", "booking", "availability", "simple", "convenient"]
}

# Prepare verbatim data
text_data = df[verbatim_column].dropna().astype(str)

# Assign categories
category_assignments = []

for text in text_data:
    text_lower = text.lower()
    assigned = False
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            category_assignments.append(category)
            assigned = True
            break
    if not assigned:
        continue  # Do not add uncategorised

# Count categories
category_counts = Counter(category_assignments)

# Prepare DataFrame
category_df = pd.DataFrame(category_counts.items(), columns=["Category", "Count"])
category_df = category_df.sort_values(by="Count", ascending=False)

# Plot bar graph
plt.figure(figsize=(12, 7))
bars = plt.barh(category_df["Category"], category_df["Count"], color='darkgreen')
plt.xlabel("Number of Mentions")
plt.title("Positive Verbatim Categories")
plt.gca().invert_yaxis()

# Add count numbers on bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f"{int(width)}", va='center')

plt.show()

# Export to Excel
output_file = "Positive_Verbatim_Category_Assignment.xlsx"
category_df.to_excel(output_file, index=False)
print(f"✅ Positive category assignment and counts saved to {output_file}")
