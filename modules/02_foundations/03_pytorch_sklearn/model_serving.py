"""
Example of serving ML models using Flask.
"""
import os
import pickle
from pathlib import Path

import numpy as np
import torch
from flask import Flask, jsonify, request

from pytorch_model import SimpleNN

app = Flask(__name__)

# Load models
MODELS_DIR = Path("models")

# Load scikit-learn models
try:
    with open(MODELS_DIR / "linear_model.pkl", "rb") as f:
        linear_model = pickle.load(f)
    with open(MODELS_DIR / "random_forest_model.pkl", "rb") as f:
        rf_model = pickle.load(f)
    sklearn_models_loaded = True
    print("scikit-learn models loaded successfully")
except Exception as e:
    sklearn_models_loaded = False
    print(f"Error loading scikit-learn models: {e}")

# Load PyTorch model
try:
    input_dim = 10  # Assuming 10 features as in the example
    hidden_dim = 20
    output_dim = 1
    pytorch_model = SimpleNN(input_dim, hidden_dim, output_dim)
    pytorch_model.load_state_dict(torch.load(MODELS_DIR / "pytorch_model.pt"))
    pytorch_model.eval()
    pytorch_model_loaded = True
    print("PyTorch model loaded successfully")
except Exception as e:
    pytorch_model_loaded = False
    print(f"Error loading PyTorch model: {e}")


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "models_loaded": {
            "sklearn": sklearn_models_loaded,
            "pytorch": pytorch_model_loaded
        }
    })


@app.route("/predict/linear", methods=["POST"])
def predict_linear():
    """
    Linear model prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...]
    }
    """
    if not sklearn_models_loaded:
        return jsonify({"error": "Linear model not loaded"}), 500
    
    try:
        # Get data from request
        data = request.json.get("data", [])
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make prediction
        predictions = linear_model.predict(data).tolist()
        
        # Return predictions
        return jsonify({"predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict/random_forest", methods=["POST"])
def predict_random_forest():
    """
    Random forest model prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...]
    }
    """
    if not sklearn_models_loaded:
        return jsonify({"error": "Random forest model not loaded"}), 500
    
    try:
        # Get data from request
        data = request.json.get("data", [])
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make prediction
        predictions = rf_model.predict(data).tolist()
        
        # Return predictions
        return jsonify({"predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict/pytorch", methods=["POST"])
def predict_pytorch():
    """
    PyTorch model prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...]
    }
    """
    if not pytorch_model_loaded:
        return jsonify({"error": "PyTorch model not loaded"}), 500
    
    try:
        # Get data from request
        data = request.json.get("data", [])
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Convert to PyTorch tensor
        tensor_data = torch.FloatTensor(data)
        
        # Make prediction
        with torch.no_grad():
            predictions = pytorch_model(tensor_data).numpy().flatten().tolist()
        
        # Return predictions
        return jsonify({"predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict/ensemble", methods=["POST"])
def predict_ensemble():
    """
    Ensemble prediction endpoint.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...]
    }
    """
    if not sklearn_models_loaded or not pytorch_model_loaded:
        return jsonify({"error": "Not all models are loaded"}), 500
    
    try:
        # Get data from request
        data = request.json.get("data", [])
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Make predictions with all models
        linear_predictions = linear_model.predict(data)
        rf_predictions = rf_model.predict(data)
        
        tensor_data = torch.FloatTensor(data)
        with torch.no_grad():
            pytorch_predictions = pytorch_model(tensor_data).numpy().flatten()
        
        # Average predictions
        ensemble_predictions = (linear_predictions + rf_predictions + pytorch_predictions) / 3
        
        # Return predictions
        return jsonify({
            "predictions": ensemble_predictions.tolist(),
            "individual_predictions": {
                "linear": linear_predictions.tolist(),
                "random_forest": rf_predictions.tolist(),
                "pytorch": pytorch_predictions.tolist()
            }
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Run the Flask app
    app.run(debug=True, host="0.0.0.0", port=5000)

