# MLOps Learning Roadmap

A comprehensive repository for learning MLOps concepts, tools, and best practices with practical examples and demos.

## Overview

This repository serves as a practical guide to learning MLOps (Machine Learning Operations) concepts and tools. It provides hands-on examples, demo scripts, and resources for each topic in the MLOps roadmap.

## Repository Structure

The repository is organized into modules, each covering a specific area of MLOps:

1. [Software Engineering](./modules/01_software_engineering/README.md) - Python fundamentals for MLOps
2. [Foundations](./modules/02_foundations/README.md) - ML and MLOps core concepts
3. [Cloud Infrastructure](./modules/03_cloud_infrastructure/README.md) - Cloud platforms for ML
4. [Experimentation & Monitoring](./modules/04_experimentation_monitoring/README.md) - Tools for tracking experiments and monitoring models
5. [Orchestrators](./modules/05_orchestrators/README.md) - Workflow orchestration tools
6. [Deployment](./modules/06_deployment/README.md) - Options for deploying ML models
7. [Miscellaneous](./modules/07_miscellaneous/README.md) - Additional important topics

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda for package management
- Docker (for containerization examples)
- Git

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mlops-roadmap.git
   cd mlops-roadmap
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install core dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Each module has its own `requirements.txt` file for module-specific dependencies.

## How to Use This Repository

1. Start with the [Software Engineering](./modules/01_software_engineering/README.md) module if you're new to Python or need a refresher.
2. Each module contains:
   - A README with an overview of the concepts
   - Example code and demo scripts
   - Instructions for setting up and running the demos
   - Additional resources for further learning

3. You can follow the modules sequentially or jump to specific topics of interest.

## MLOps Roadmap

### Software Engineering (Python)
- Flask/FastAPI
- Version Control - Git
- Unit & Integration testing
- Docker
- CI/CD (GitHub Actions, CircleCI, Jenkins)
- Load testing - Locust
- A/B testing

### Foundations
- ML + MLOps concepts
- Courses + Books
- PyTorch + scikit-learn & serving

### Cloud Infrastructure
- AWS SageMaker
- GCP VertexAI
- Azure ML

### Experimentation & Monitoring
- MLflow for experimentation
- Grafana & Prometheus
- DataDog
- Weights & Biases, Arize

### Orchestrators
- KubeFlow
- Airflow
- MetaFlow

### Deployment Options
- EC2
- ECS
- Step Functions
- Kubernetes

### Miscellaneous
- IaaS - Terraform/AWS CDK
- Security
- Feature Stores

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

