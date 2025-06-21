import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

np.random.seed(123)

n = 100        # number of observations
rho = 0        # true autocorrelation (0 = none)
n_sim = 10000  # number of simulations
dw_stats = []

for i in range(n_sim):
    # Simulate AR(1) errors
    errors = [np.random.normal()]
    for t in range(1, n):
        errors.append(rho * errors[t-1] + np.random.normal())
    errors = np.array(errors)
    
    # Simulate independent variable and dependent variable
    x = np.random.normal(size=n)
    y = 2 + 3 * x + errors
    
    # Fit linear model
    X = sm.add_constant(x)
    model = sm.OLS(y, X).fit()
    
    # Durbin-Watson statistic
    dw = sm.stats.stattools.durbin_watson(model.resid)
    dw_stats.append(dw)

# Plot histogram
plt.hist(dw_stats, bins=50, edgecolor='black')
plt.axvline(x=1.972, color='red', linewidth=2, label="Observed DW = 1.972")
plt.xlabel('Durbin-Watson Statistic')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation of DW (rho = 0)')
plt.legend()
plt.show()
