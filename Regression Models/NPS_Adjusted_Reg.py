import pandas as pd
import statsmodels.api as sm
import numpy as np

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

# Convert relevant columns to numeric
df[[dependent_var] + independent_vars] = df[[dependent_var] + independent_vars].apply(pd.to_numeric, errors='coerce')

# Drop rows where dependent variable (Q2) or Q1 are missing
df_clean = df.dropna(subset=[dependent_var, "Q1 - Overall satisfaction"])

# Check if any rows left
if df_clean.shape[0] == 0:
    print("No rows left after dropping missing Q2 and Q1 data. Cannot run regression.")
else:
    # Fill missing independent vars with mean
    X = df_clean[independent_vars].fillna(df_clean[independent_vars].mean())

    # Drop columns with all NaN (if any)
    X = X.dropna(axis=1, how='all')

    # Add constant
    X = sm.add_constant(X)

    # Remove rows with Inf or NaN
    X = X.replace([np.inf, -np.inf], np.nan).dropna()

    # Align dependent variable
    y = df_clean.loc[X.index, dependent_var]

    # Fit regression model
    model = sm.OLS(y, X).fit()

    # Print regression results
    print(model.summary())
