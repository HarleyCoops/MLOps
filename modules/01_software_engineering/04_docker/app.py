"""
Flask API for serving a machine learning model in a Docker container.
"""
import os
import pickle
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# Get model path from environment variable
MODEL_PATH = os.environ.get("MODEL_PATH", "model.pkl")

# Load the model
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    # Create a dummy model if the real one can't be loaded
    class DummyModel:
        def predict(self, data):
            return np.mean(data, axis=1).tolist()
    
    model = DummyModel()
    print("Created dummy model as fallback")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route("/predict", methods=["POST"])
def predict():
    """
    Prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...]
    }
    """
    try:
        # Get data from request
        data = request.json.get("data", [])
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make prediction
        predictions = model.predict(data)
        
        # Return predictions
        return jsonify({"predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

