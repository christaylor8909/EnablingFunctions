import pandas as pd
import matplotlib.pyplot as plt

# Define regression result data (Q1 excluded)
data = {
    "Variable": [
        "Q5 - Ease of getting preferred appointment",
        "Q6 - Welcoming athmosphere",
        "Q7 - Courtesy and friendliness",
        "Q8 - Competence",
        "Q10 - Price quotation's explanation",
        "Q11 - Explanation of cost and work done",
        "Q12 - Quality of work performed"
    ],
    "Coefficient": [0.0427, 0.0909, 0.0562, 0.0721, 0.0052, 0.0742, 0.0375],
    "P-Value": [0.001, 0.000, 0.010, 0.001, 0.736, 0.000, 0.022]
}

# Create dataframe
df_plot = pd.DataFrame(data)

# Sort by absolute value of coefficients
df_plot["abs_coef"] = df_plot["Coefficient"].abs()
df_plot = df_plot.sort_values(by="abs_coef", ascending=True)

# Determine bar color based on significance
df_plot["Color"] = df_plot["P-Value"].apply(lambda p: "blue" if p < 0.05 else "grey")

# Create horizontal bar plot
plt.figure(figsize=(9, 7))
bars = plt.barh(df_plot["Variable"], df_plot["Coefficient"], color=df_plot["Color"])

# Add vertical line at 0
plt.axvline(x=0, color='black', linewidth=0.8)

# Add plot title and axis labels with bigger fonts
plt.title("Regression Coefficients (Excluding Q1 - Overall Satisfaction)", fontsize=16)
plt.xlabel("Coefficient Value", fontsize=14)
plt.ylabel("Question", fontsize=14)

# Increase font size for tick labels
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Add legend with bigger font
plt.legend(["Not Significant (Grey)", "Significant (Blue)"], fontsize=12)

# Tight layout and show plot
plt.tight_layout()

# OPTIONAL: Save plot to file (uncomment below to enable saving)
# plt.savefig("regression_coefficients_plot.png", dpi=300)

plt.show()

