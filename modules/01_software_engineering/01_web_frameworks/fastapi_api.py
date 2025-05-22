"""
FastAPI example for serving a machine learning model.
"""
import pickle
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ML Model API", description="API for serving ML model predictions", version="1.0.0")

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

# Define request and response models
class PredictionRequest(BaseModel):
    data: List[List[float]]

class PredictionResponse(BaseModel):
    predictions: List[float]

class BatchPredictionRequest(BaseModel):
    data: List[List[float]]
    batch_id: Optional[str] = "unknown"

class BatchPredictionResponse(BaseModel):
    batch_id: str
    predictions: List[float]
    count: int

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Make predictions on input data.
    """
    try:
        predictions = model.predict(request.data)
        return {"predictions": predictions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch_predict", response_model=BatchPredictionResponse)
def batch_predict(request: BatchPredictionRequest):
    """
    Make batch predictions on input data.
    """
    try:
        predictions = model.predict(request.data)
        return {
            "batch_id": request.batch_id,
            "predictions": predictions,
            "count": len(predictions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

