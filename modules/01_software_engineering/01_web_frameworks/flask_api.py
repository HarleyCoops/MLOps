"""
Simple Flask API for serving a machine learning model.
"""
import pickle
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# In a real-world scenario, you would load a trained model
# Here we're creating a dummy model for demonstration
class DummyModel:
    def predict(self, data):
        return np.mean(data, axis=1).tolist()

# Load or create the model
MODEL_PATH = Path("model.pkl")
if MODEL_PATH.exists():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
else:
    model = DummyModel()
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

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

@app.route("/batch_predict", methods=["POST"])
def batch_predict():
    """
    Batch prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...],
        "batch_id": "unique_batch_id"
    }
    """
    try:
        # Get data from request
        data = request.json.get("data", [])
        batch_id = request.json.get("batch_id", "unknown")
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make prediction
        predictions = model.predict(data)
        
        # Return predictions with batch ID
        return jsonify({
            "batch_id": batch_id,
            "predictions": predictions,
            "count": len(predictions)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

