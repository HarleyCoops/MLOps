# Web Frameworks for ML Model Serving

This directory contains examples of using Flask and FastAPI to serve machine learning models.

## Examples

1. [Flask API](./flask_api.py) - A simple Flask API for serving ML model predictions
2. [FastAPI API](./fastapi_api.py) - A FastAPI implementation for serving ML model predictions

## Running the Examples

### Flask API

```bash
# Install dependencies
pip install flask numpy

# Run the Flask API
python flask_api.py
```

The Flask API will be available at http://localhost:5000

### FastAPI API

```bash
# Install dependencies
pip install fastapi uvicorn numpy pydantic

# Run the FastAPI API
python fastapi_api.py
```

The FastAPI API will be available at http://localhost:8000

You can also access the automatic API documentation at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Testing the APIs

### Using curl

#### Flask API
```bash
# Health check
curl http://localhost:5000/health

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}'

# Make a batch prediction
curl -X POST http://localhost:5000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "batch_id": "batch-001"}'
```

#### FastAPI API
```bash
# Health check
curl http://localhost:8000/health

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}'

# Make a batch prediction
curl -X POST http://localhost:8000/batch_predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "batch_id": "batch-001"}'
```

### Using Python requests

```python
import requests
import json

# Flask API
response = requests.post(
    "http://localhost:5000/predict",
    json={"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}
)
print(response.json())

# FastAPI API
response = requests.post(
    "http://localhost:8000/predict",
    json={"data": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]}
)
print(response.json())
```

## Key Differences Between Flask and FastAPI

1. **Performance**: FastAPI is generally faster than Flask due to its asynchronous capabilities.
2. **Type Hints**: FastAPI uses Python type hints for request validation and documentation generation.
3. **Documentation**: FastAPI automatically generates interactive API documentation.
4. **Async Support**: FastAPI has built-in support for asynchronous request handling.
5. **Validation**: FastAPI uses Pydantic for data validation and serialization.

## Best Practices for ML Model Serving

1. **Model Loading**: Load models at startup, not on each request.
2. **Input Validation**: Validate input data before passing it to the model.
3. **Error Handling**: Implement proper error handling and return meaningful error messages.
4. **Logging**: Log predictions and errors for monitoring and debugging.
5. **Versioning**: Implement API versioning to support multiple model versions.
6. **Monitoring**: Add endpoints for monitoring model performance and health.
7. **Batch Processing**: Support batch predictions for efficiency.
8. **Caching**: Implement caching for frequently requested predictions.
9. **Authentication**: Secure your API with proper authentication.
10. **Rate Limiting**: Implement rate limiting to prevent abuse.

