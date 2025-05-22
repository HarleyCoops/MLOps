# Containerizing ML Models with Docker

This directory contains examples of containerizing machine learning models using Docker.

## Files

- [Dockerfile](./Dockerfile) - Docker configuration for building the ML model container
- [app.py](./app.py) - Flask API for serving the ML model
- [requirements.txt](./requirements.txt) - Python dependencies
- [docker-compose.yml](./docker-compose.yml) - Docker Compose configuration for running the container

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, for running with docker-compose)

## Creating a Dummy Model

Before building the Docker image, let's create a dummy model:

```python
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
```

Save this as `create_model.py` and run it to generate the model file:

```bash
python create_model.py
```

## Building and Running the Docker Container

### Using Docker

```bash
# Build the Docker image
docker build -t ml-model-api .

# Run the container
docker run -p 5000:5000 ml-model-api
```

### Using Docker Compose

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## Testing the API

Once the container is running, you can test the API:

```bash
# Health check
curl http://localhost:5000/health

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [[1.0, 2.0], [3.0, 4.0]]}'
```

## Docker Best Practices for ML Models

1. **Use Specific Base Images**: Use specific versions of base images to ensure reproducibility.
2. **Multi-Stage Builds**: Use multi-stage builds to keep the final image small.
3. **Layer Caching**: Order Dockerfile commands to maximize layer caching.
4. **Environment Variables**: Use environment variables for configuration.
5. **Health Checks**: Implement health checks to monitor container health.
6. **Non-Root User**: Run containers as a non-root user for security.
7. **Proper Logging**: Configure proper logging for monitoring.
8. **Volume Mounting**: Use volumes for model files to update models without rebuilding.
9. **Resource Limits**: Set resource limits to prevent container from consuming too many resources.
10. **Proper Tagging**: Use proper tagging for versioning.

## Example of a Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.9 AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY app.py .
COPY model.pkl .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Security Considerations

1. **Scan Images**: Regularly scan Docker images for vulnerabilities.
2. **Minimal Base Images**: Use minimal base images to reduce attack surface.
3. **No Sensitive Data**: Don't include sensitive data in Docker images.
4. **Read-Only Filesystem**: Use read-only filesystems when possible.
5. **Update Dependencies**: Regularly update dependencies to patch security vulnerabilities.

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Security](https://docs.docker.com/engine/security/)

