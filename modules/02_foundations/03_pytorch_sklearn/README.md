# PyTorch and scikit-learn Models

This directory contains examples of creating, training, and serving machine learning models using PyTorch and scikit-learn.

## Files

- [pytorch_model.py](./pytorch_model.py) - Example of creating and training a PyTorch model
- [sklearn_model.py](./sklearn_model.py) - Example of creating and training scikit-learn models
- [model_serving.py](./model_serving.py) - Example of serving models using Flask

## Running the Examples

### PyTorch Model

```bash
# Install dependencies
pip install torch numpy matplotlib

# Run the PyTorch example
python pytorch_model.py
```

This will:
1. Generate synthetic data
2. Create and train a simple neural network
3. Save the trained model to `models/pytorch_model.pt`
4. Load the model and make predictions
5. Generate a plot of the training and validation losses

### scikit-learn Models

```bash
# Install dependencies
pip install scikit-learn numpy matplotlib

# Run the scikit-learn example
python sklearn_model.py
```

This will:
1. Generate synthetic data
2. Create and train linear regression and random forest models
3. Save the trained models to `models/linear_model.pkl` and `models/random_forest_model.pkl`
4. Load the models and make predictions
5. Generate plots of actual vs predicted values

### Model Serving

```bash
# Install dependencies
pip install flask torch scikit-learn numpy

# Run the model serving example
python model_serving.py
```

This will start a Flask API server at http://localhost:5000 with the following endpoints:

- `/health` - Health check endpoint
- `/predict/linear` - Linear regression model prediction endpoint
- `/predict/random_forest` - Random forest model prediction endpoint
- `/predict/pytorch` - PyTorch model prediction endpoint
- `/predict/ensemble` - Ensemble prediction endpoint (average of all models)

## Testing the Model Serving API

### Using curl

```bash
# Health check
curl http://localhost:5000/health

# Linear regression prediction
curl -X POST http://localhost:5000/predict/linear \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}'

# Random forest prediction
curl -X POST http://localhost:5000/predict/random_forest \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}'

# PyTorch prediction
curl -X POST http://localhost:5000/predict/pytorch \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}'

# Ensemble prediction
curl -X POST http://localhost:5000/predict/ensemble \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}'
```

### Using Python requests

```python
import requests
import json

# Health check
response = requests.get("http://localhost:5000/health")
print(response.json())

# Linear regression prediction
response = requests.post(
    "http://localhost:5000/predict/linear",
    json={"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}
)
print(response.json())

# Random forest prediction
response = requests.post(
    "http://localhost:5000/predict/random_forest",
    json={"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}
)
print(response.json())

# PyTorch prediction
response = requests.post(
    "http://localhost:5000/predict/pytorch",
    json={"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}
)
print(response.json())

# Ensemble prediction
response = requests.post(
    "http://localhost:5000/predict/ensemble",
    json={"data": [[1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]]}
)
print(response.json())
```

## Model Serialization Formats

### PyTorch

PyTorch models can be serialized using:

1. **torch.save/torch.load**: The default PyTorch serialization format
2. **ONNX**: Open Neural Network Exchange format for interoperability
3. **TorchScript**: A way to serialize and optimize PyTorch models

Example of converting a PyTorch model to ONNX:

```python
import torch
import torch.onnx

# Assuming model is a PyTorch model
dummy_input = torch.randn(1, 10)  # Example input
torch.onnx.export(model, dummy_input, "model.onnx")
```

### scikit-learn

scikit-learn models can be serialized using:

1. **pickle**: The default Python serialization format
2. **joblib**: A more efficient alternative to pickle for large NumPy arrays
3. **ONNX**: Open Neural Network Exchange format for interoperability

Example of using joblib:

```python
from joblib import dump, load

# Save the model
dump(model, "model.joblib")

# Load the model
model = load("model.joblib")
```

## Best Practices for Model Serving

1. **Model Versioning**: Version your models to track changes
2. **Input Validation**: Validate input data before passing it to the model
3. **Error Handling**: Implement proper error handling
4. **Logging**: Log predictions and errors for monitoring
5. **Monitoring**: Monitor model performance and resource usage
6. **Scaling**: Implement strategies for scaling model serving
7. **Caching**: Cache predictions for frequently requested inputs
8. **Batching**: Batch predictions for efficiency
9. **Asynchronous Processing**: Use asynchronous processing for long-running predictions
10. **Model Reloading**: Implement strategies for reloading models without downtime

## Resources

- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [scikit-learn Documentation](https://scikit-learn.org/stable/documentation.html)
- [ONNX Documentation](https://onnx.ai/onnx/index.html)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Model Serving Best Practices](https://www.tensorflow.org/tfx/serving/serving_basic)

