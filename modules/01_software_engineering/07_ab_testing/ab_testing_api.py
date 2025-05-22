"""
Example of A/B testing for ML models.
"""
import json
import pickle
import random
import uuid
from datetime import datetime
from pathlib import Path

import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

# In a real-world scenario, you would load trained models
# Here we're creating dummy models for demonstration
class ModelA:
    def predict(self, data):
        return np.mean(data, axis=1).tolist()

class ModelB:
    def predict(self, data):
        return (np.mean(data, axis=1) * 1.1).tolist()  # 10% higher predictions

# Load or create the models
MODEL_A_PATH = Path("model_a.pkl")
MODEL_B_PATH = Path("model_b.pkl")

if MODEL_A_PATH.exists():
    with open(MODEL_A_PATH, "rb") as f:
        model_a = pickle.load(f)
else:
    model_a = ModelA()
    with open(MODEL_A_PATH, "wb") as f:
        pickle.dump(model_a, f)

if MODEL_B_PATH.exists():
    with open(MODEL_B_PATH, "rb") as f:
        model_b = pickle.load(f)
else:
    model_b = ModelB()
    with open(MODEL_B_PATH, "wb") as f:
        pickle.dump(model_b, f)

# A/B test configuration
AB_TEST_CONFIG = {
    "name": "model_comparison",
    "variants": {
        "A": {"model": model_a, "weight": 0.5},
        "B": {"model": model_b, "weight": 0.5}
    },
    "metrics": ["prediction_value", "user_conversion"]
}

# In-memory storage for A/B test results
# In a real-world scenario, you would use a database
AB_TEST_RESULTS = []

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route("/predict", methods=["POST"])
def predict():
    """
    Prediction endpoint with A/B testing.
    
    Expects JSON data in the format:
    {
        "data": [[feature1, feature2, ...], [feature1, feature2, ...], ...],
        "user_id": "optional_user_id"
    }
    """
    try:
        # Get data from request
        data = request.json.get("data", [])
        user_id = request.json.get("user_id", str(uuid.uuid4()))
        
        # Validate input
        if not data or not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400
        
        # Determine which variant to use
        variant = select_variant(user_id)
        model = AB_TEST_CONFIG["variants"][variant]["model"]
        
        # Make prediction
        predictions = model.predict(data)
        
        # Log A/B test result
        log_ab_test_result(user_id, variant, predictions)
        
        # Return predictions with variant information
        return jsonify({
            "predictions": predictions,
            "variant": variant,
            "experiment": AB_TEST_CONFIG["name"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/conversion", methods=["POST"])
def record_conversion():
    """
    Record a conversion event for A/B testing.
    
    Expects JSON data in the format:
    {
        "user_id": "user_id",
        "value": optional_conversion_value
    }
    """
    try:
        # Get data from request
        user_id = request.json.get("user_id")
        value = request.json.get("value", 1.0)
        
        # Validate input
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        # Record conversion
        success = record_conversion_event(user_id, value)
        
        if success:
            return jsonify({"status": "success", "message": "Conversion recorded"})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ab_test_results", methods=["GET"])
def get_ab_test_results():
    """
    Get A/B test results.
    """
    # Calculate metrics for each variant
    results = calculate_ab_test_metrics()
    
    return jsonify(results)

def select_variant(user_id):
    """
    Select a variant for the user based on the A/B test configuration.
    
    In a real-world scenario, you would use a more sophisticated method
    to ensure consistent variant assignment for the same user.
    """
    # Simple deterministic variant selection based on user_id
    # In production, you might use a more sophisticated method
    if hash(user_id) % 100 < AB_TEST_CONFIG["variants"]["A"]["weight"] * 100:
        return "A"
    else:
        return "B"

def log_ab_test_result(user_id, variant, predictions):
    """
    Log an A/B test result.
    """
    AB_TEST_RESULTS.append({
        "user_id": user_id,
        "variant": variant,
        "predictions": predictions,
        "timestamp": datetime.now().isoformat(),
        "converted": False,
        "conversion_value": 0.0
    })

def record_conversion_event(user_id, value):
    """
    Record a conversion event for a user.
    """
    for result in AB_TEST_RESULTS:
        if result["user_id"] == user_id:
            result["converted"] = True
            result["conversion_value"] = value
            return True
    
    return False

def calculate_ab_test_metrics():
    """
    Calculate metrics for the A/B test.
    """
    metrics = {
        "experiment": AB_TEST_CONFIG["name"],
        "variants": {},
        "total_users": len(AB_TEST_RESULTS)
    }
    
    for variant in AB_TEST_CONFIG["variants"]:
        variant_results = [r for r in AB_TEST_RESULTS if r["variant"] == variant]
        conversions = [r for r in variant_results if r["converted"]]
        
        metrics["variants"][variant] = {
            "users": len(variant_results),
            "conversions": len(conversions),
            "conversion_rate": len(conversions) / len(variant_results) if variant_results else 0,
            "average_prediction": np.mean([np.mean(r["predictions"]) for r in variant_results]) if variant_results else 0,
            "total_conversion_value": sum(r["conversion_value"] for r in conversions)
        }
    
    return metrics

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

