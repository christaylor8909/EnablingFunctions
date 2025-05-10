import pandas as pd
import statsmodels.api as sm
import numpy as np

# Load cleaned Excel data
df = pd.read_excel("InterviewSummaryData_CLEANED.xlsx")
df.columns = df.columns.str.strip()

# Identify Q columns
q_cols = [col for col in df.columns if col.startswith("Q") and "-" in col]

# Convert Q columns to numeric (again, to be sure)
df[q_cols] = df[q_cols].apply(pd.to_numeric, errors='coerce')

# Drop columns with more than 40% missing (likely text-based or corrupt)
threshold = 0.4
valid_q_cols = df[q_cols].loc[:, df[q_cols].isna().mean() < threshold].columns.tolist()

# Define Y (Q1) and X (Q2 onward)
y = df[valid_q_cols[0]]  # Q1
X = df[valid_q_cols[1:]] # Q2+

# Fill missing values with column means
X = X.fillna(X.mean())

# Drop remaining inf/nan rows from X and align Y
X = X.replace([np.inf, -np.inf], np.nan).dropna()
y = y.loc[X.index]

# Add constant
X = sm.add_constant(X)

# Run regression
if X.empty or y.empty:
    print("❌ Still not enough clean data to run regression.")
else:
    model = sm.OLS(y, X).fit()
    print(model.summary())
