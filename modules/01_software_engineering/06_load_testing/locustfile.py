"""
Locust load testing script for ML model API.
"""
import json
import random
import time

from locust import HttpUser, between, task


class MLModelUser(HttpUser):
    """
    Simulates a user interacting with an ML model API.
    """
    
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """
        Initialize the user.
        """
        # Check if the API is healthy
        response = self.client.get("/health")
        if response.status_code != 200:
            self.environment.runner.quit()
    
    @task(3)
    def predict_single(self):
        """
        Make a single prediction request.
        """
        # Generate random features
        features = [[random.uniform(0, 10) for _ in range(5)]]
        
        # Make prediction request
        start_time = time.time()
        with self.client.post(
            "/predict",
            json={"data": features},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "predictions" in result:
                        response.success()
                    else:
                        response.failure("Response does not contain predictions")
                except json.JSONDecodeError:
                    response.failure("Response could not be decoded as JSON")
            else:
                response.failure(f"Request failed with status code {response.status_code}")
        
        # Log latency
        latency = time.time() - start_time
        self.environment.events.request_success.fire(
            request_type="POST",
            name="predict_latency",
            response_time=latency * 1000,  # Convert to milliseconds
            response_length=0
        )
    
    @task(1)
    def predict_batch(self):
        """
        Make a batch prediction request.
        """
        # Generate random batch of features
        batch_size = random.randint(10, 100)
        features = [[random.uniform(0, 10) for _ in range(5)] for _ in range(batch_size)]
        
        # Make batch prediction request
        start_time = time.time()
        with self.client.post(
            "/batch_predict",
            json={"data": features, "batch_id": f"batch-{int(time.time())}"},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if "predictions" in result and len(result["predictions"]) == batch_size:
                        response.success()
                    else:
                        response.failure("Response does not contain correct predictions")
                except json.JSONDecodeError:
                    response.failure("Response could not be decoded as JSON")
            else:
                response.failure(f"Request failed with status code {response.status_code}")
        
        # Log latency and batch size
        latency = time.time() - start_time
        self.environment.events.request_success.fire(
            request_type="POST",
            name="batch_predict_latency",
            response_time=latency * 1000,  # Convert to milliseconds
            response_length=0
        )
        self.environment.events.request_success.fire(
            request_type="POST",
            name="batch_size",
            response_time=batch_size,  # Use response_time to log batch size
            response_length=0
        )
    
    @task(5)
    def health_check(self):
        """
        Check the health of the API.
        """
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("status") == "healthy":
                        response.success()
                    else:
                        response.failure("API is not healthy")
                except json.JSONDecodeError:
                    response.failure("Response could not be decoded as JSON")
            else:
                response.failure(f"Health check failed with status code {response.status_code}")

