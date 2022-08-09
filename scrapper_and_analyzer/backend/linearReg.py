# Step 1: Import packages and classes
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Step 2a: Provide data

y = [4, 5, 20, 14, 32, 22, 38, 43]
y = np.array(y)

# Step 2b: Transform input data
x_ = PolynomialFeatures(degree=2, include_bias=False).fit_transform(y)

# Step 3: Create a model and fit it
model = LinearRegression().fit(x_)

# Step 4: Get results
r_sq = model.score(x_, y)
intercept, coefficients = model.intercept_, model.coef_

# Step 5: Predict response
y_pred = model.predict(x_)
# This regression example yields the following results and predictions:

print(f"coefficient of determination: {r_sq}")
# coefficient of determination: 0.9453701449127822

print(f"intercept: {intercept}")
# intercept: 0.8430556452395876

print(f"coefficients:\n{coefficients}")
# coefficients:
# [ 2.44828275  0.16160353 -0.15259677  0.47928683 -0.4641851 ]

print(f"predicted response:\n{y_pred}")
# predicted response:
# [ 0.54047408 11.36340283 16.07809622 15.79139    29.73858619 23.50834636
# 39.05631386 41.92339046]