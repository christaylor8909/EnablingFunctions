#This code produces a monte carlo visualisation which plots a residual path
import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

# Load cleaned Excel file
file_path = r"C:\Users\t0355lp\.vscode\Python\InterviewSummaryData_CLEANED.xlsx"
df = pd.read_excel(file_path)

# Define dependent and independent variables
dependent_var = "Q2 - Recommendation - workshop"
independent_vars = [
    "Q1 - Overall satisfaction",
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

# Convert columns to numeric
df[[dependent_var] + independent_vars] = df[[dependent_var] + independent_vars].apply(pd.to_numeric, errors='coerce')

# Clean dataset
df_clean = df.dropna(subset=[dependent_var, "Q1 - Overall satisfaction"])
X = df_clean[independent_vars].fillna(df_clean[independent_vars].mean())
X = X.dropna(axis=1, how='all')
X = sm.add_constant(X)
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = df_clean.loc[X.index, dependent_var]

# Fit model
model = sm.OLS(y, X).fit()

# Get residuals
residuals = model.resid

# Plot residual path
plt.figure(figsize=(15, 6))
plt.plot(residuals.values, linewidth=2, color='blue')
plt.axhline(y=0, color='black', linestyle='--')
plt.title("Path Plot of Residuals")
plt.xlabel("Observation (in order of dataset)")
plt.ylabel("Residual Value")
plt.show()
