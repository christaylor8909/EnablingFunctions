import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Download nltk data
nltk.download('punkt')
nltk.download('stopwords')

# Load data
file_path = r"C:\Users\t0355lp\.vscode\Python\InterviewSummaryData.xlsx"
df = pd.read_excel(file_path, sheet_name=0)

df.columns = df.columns.map(lambda x: str(x).strip().replace('\u00A0', '').replace('\n', '').lower())

# SHOW columns to find the right one
print("✅ Available columns:")
print(df.columns.tolist())

# SET manually the verbatim column
verbatim_column = "q20 - final verbatim"

# Define keywords for each category
categories = {
    "Quality of Work": ["quality", "repair", "fix", "issue", "problem", "workmanship", "fault"],
    "Delays / Waiting": ["delay", "wait", "waiting", "time", "slow", "late"],
    "Communication / Follow-up": ["call", "follow up", "communicate", "communication", "update", "contact"],
    "Pricing / Cost": ["price", "cost", "expensive", "charge", "quotation", "quote"],
    "Booking / Availability": ["book", "booking", "appointment", "availability"],
    "Staff Attitude / Professionalism": ["rude", "attitude", "professionalism", "unfriendly", "helpful", "courteous"]
}

# Prepare text
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
        category_assignments.append("Other / Uncategorised")

# Count categories
category_counts = Counter(category_assignments)

# Create DataFrame for plotting
category_df = pd.DataFrame(category_counts.items(), columns=["Category", "Count"])
category_df = category_df.sort_values(by="Count", ascending=False)

# Plot bar graph
plt.figure(figsize=(12, 7))
plt.barh(category_df["Category"], category_df["Count"], color='darkred')
plt.xlabel("Number of Mentions")
plt.title("Negative Verbatim Categories")
plt.gca().invert_yaxis()
plt.show()

# Export to Excel
output_file = "Verbatim_Category_Assignment.xlsx"
category_df.to_excel(output_file, index=False)
print(f"✅ Category assignment and counts saved to {output_file}")
