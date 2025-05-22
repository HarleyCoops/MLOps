# Load Testing ML Model APIs with Locust

This directory contains examples of load testing ML model APIs using Locust.

## Files

- [locustfile.py](./locustfile.py) - Locust script for load testing an ML model API

## What is Load Testing?

Load testing is the process of simulating real-world load on a system to evaluate its performance under expected or stress conditions. For ML model APIs, load testing helps to:

1. Determine the maximum throughput the API can handle
2. Identify performance bottlenecks
3. Measure response times under different loads
4. Ensure the system can handle expected traffic
5. Test the system's behavior under stress conditions

## Using Locust for Load Testing

[Locust](https://locust.io/) is an open-source load testing tool that allows you to define user behavior in Python code and swarm your system with millions of simultaneous users.

### Installation

```bash
pip install locust
```

### Running the Load Test

1. Start your ML model API (e.g., the Flask or FastAPI examples from the web frameworks module)
2. Run Locust:

```bash
locust -f locustfile.py --host=http://localhost:5000
```

3. Open the Locust web interface at http://localhost:8089
4. Configure the number of users, spawn rate, and start the test

### Understanding the Locust Script

The [locustfile.py](./locustfile.py) script defines a user class that simulates real-world interactions with an ML model API:

- `on_start`: Checks if the API is healthy before starting the test
- `predict_single`: Simulates a user making a single prediction request
- `predict_batch`: Simulates a user making a batch prediction request
- `health_check`: Simulates a user checking the health of the API

The script also includes custom metrics for tracking:
- Prediction latency
- Batch prediction latency
- Batch size distribution

### Interpreting the Results

Locust provides real-time statistics and graphs for:

- **Request Count**: Number of requests made
- **Response Time**: Min, max, average, and median response times
- **Throughput**: Requests per second
- **Failure Rate**: Percentage of failed requests
- **Custom Metrics**: Any custom metrics defined in the script

## Best Practices for Load Testing ML Model APIs

1. **Start Small**: Begin with a small number of users and gradually increase
2. **Test Different Scenarios**: Test different types of requests and batch sizes
3. **Monitor Resources**: Monitor CPU, memory, and network usage during the test
4. **Test Regularly**: Incorporate load testing into your CI/CD pipeline
5. **Test in a Production-Like Environment**: Test in an environment that closely resembles production
6. **Define Clear Success Criteria**: Define what constitutes acceptable performance
7. **Test Beyond Expected Load**: Test the system's behavior under stress conditions
8. **Analyze Bottlenecks**: Use the results to identify and address bottlenecks
9. **Test Scaling**: Test how the system scales with additional resources
10. **Test Failure Recovery**: Test how the system recovers from failures

## Common Performance Bottlenecks in ML Model APIs

1. **Model Inference Time**: The time it takes to make a prediction
2. **Data Preprocessing**: The time it takes to preprocess input data
3. **Serialization/Deserialization**: The time it takes to convert between formats
4. **Database Queries**: The time it takes to retrieve data from a database
5. **Network Latency**: The time it takes for data to travel over the network
6. **Resource Contention**: Competition for CPU, memory, or I/O resources
7. **Synchronous Operations**: Operations that block the request thread
8. **Inefficient Algorithms**: Algorithms with high time or space complexity
9. **Memory Leaks**: Gradual consumption of memory over time
10. **External Service Dependencies**: Reliance on slow or unreliable external services

## Resources

- [Locust Documentation](https://docs.locust.io/)
- [Load Testing Best Practices](https://www.blazemeter.com/blog/load-testing-best-practices)
- [Performance Testing ML Models](https://neptune.ai/blog/performance-testing-ml-models)

