"""
Create a dummy ML model for demonstration purposes.
"""
import pickle

import numpy as np
from sklearn.linear_model import LinearRegression

# Create a dummy model
model = LinearRegression()
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
y = np.array([3, 7, 11, 15])
model.fit(X, y)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Dummy model created and saved as model.pkl")

# Test the model
test_data = np.array([[2, 3], [4, 5]])
predictions = model.predict(test_data)
print(f"Test predictions: {predictions}")

