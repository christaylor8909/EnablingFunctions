import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned Excel file
file_path = r"C:\Users\t0355lp\.vscode\Python\InterviewSummaryData_CLEANED.xlsx"
df = pd.read_excel(file_path)

# Define columns to check distribution
columns_to_check = [
    "Q1 - Overall satisfaction",
    "Q2 - Recommendation - workshop",
    "Q5 - Ease of getting preferred appointment",
    "Q6 - Welcoming athmosphere",
    "Q7 - Courtesy and friendliness",
    "Q8 - Competence",
    "Q9 - Transport assistance offer",
    "Q10 - Price quotation's explanation",
    "Q11 - Explanation of cost and work done",
    "Q12 - Quality of work performed",
    "Q15 - Respect of time to repair",
    "Q16 - Informed of the delay"
]

# Convert to numeric (just in case)
df[columns_to_check] = df[columns_to_check].apply(pd.to_numeric, errors='coerce')

# Plot histograms
for col in columns_to_check:
    plt.figure(figsize=(7, 5))
    plt.hist(df[col].dropna(), bins=10, color='skyblue', edgecolor='black')
    plt.title(f"Distribution of {col}", fontsize=14)
    plt.xlabel("Score", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    plt.show()

# Plot boxplots
for col in columns_to_check:
    plt.figure(figsize=(7, 5))
    plt.boxplot(df[col].dropna(), vert=False)
    plt.title(f"Boxplot of {col}", fontsize=14)
    plt.xlabel("Score", fontsize=12)
    plt.xticks(fontsize=11)
    plt.tight_layout()
    plt.show()
