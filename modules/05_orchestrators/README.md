# Orchestrators

This module covers workflow orchestration tools for ML pipelines.

## Topics Covered

### 1. KubeFlow
- KubeFlow Pipelines
- KubeFlow Components
- KubeFlow Serving
- KubeFlow Notebooks

### 2. Airflow
- DAGs (Directed Acyclic Graphs)
- Operators
- Sensors
- Hooks
- Executors

### 3. MetaFlow
- Flows
- Steps
- Parameters
- Data
- Deployment

## Getting Started

Each orchestrator has its own directory with examples and demos:

- [KubeFlow](./01_kubeflow/)
- [Airflow](./02_airflow/)
- [MetaFlow](./03_metaflow/)

## Prerequisites

- Python 3.8+
- Docker and Kubernetes (for KubeFlow)
- Basic understanding of ML pipelines

## Installation

```bash
# Install dependencies for this module
pip install -r requirements.txt
```

## Orchestrator Comparison

| Feature | KubeFlow | Airflow | MetaFlow |
|---------|----------|---------|----------|
| **Architecture** | Kubernetes-native | Python-based | Python-based |
| **UI** | Web UI | Web UI | CLI + Web UI |
| **Scheduling** | ✅ | ✅ | ✅ |
| **Monitoring** | ✅ | ✅ | ✅ |
| **Parallelism** | ✅ | ✅ | ✅ |
| **Distributed Computing** | ✅ | ✅ | ✅ |
| **ML-specific Features** | ✅ | ❌ | ✅ |
| **Data Versioning** | ❌ | ❌ | ✅ |
| **Deployment Options** | Self-hosted | Self-hosted, Cloud | Self-hosted, Cloud |
| **Learning Curve** | Steep | Moderate | Gentle |
| **Community Size** | Large | Very Large | Growing |
| **Cloud Integration** | GCP, AWS, Azure | GCP, AWS, Azure | AWS |

## ML Pipeline Components

A typical ML pipeline consists of the following components:

1. **Data Ingestion**: Collecting data from various sources
2. **Data Validation**: Validating data quality and schema
3. **Data Preprocessing**: Cleaning and transforming data
4. **Feature Engineering**: Creating features for model training
5. **Model Training**: Training ML models
6. **Model Evaluation**: Evaluating model performance
7. **Model Validation**: Validating model against business requirements
8. **Model Registration**: Registering model in a model registry
9. **Model Deployment**: Deploying model to production
10. **Monitoring**: Monitoring model performance and data drift

## Resources

### KubeFlow
- [KubeFlow Documentation](https://www.kubeflow.org/docs/)
- [KubeFlow GitHub Repository](https://github.com/kubeflow/kubeflow)
- [KubeFlow Pipelines Examples](https://github.com/kubeflow/pipelines/tree/master/samples)

### Airflow
- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow GitHub Repository](https://github.com/apache/airflow)
- [Airflow for ML Pipelines](https://www.astronomer.io/blog/airflow-ml-pipelines/)

### MetaFlow
- [MetaFlow Documentation](https://docs.metaflow.org/)
- [MetaFlow GitHub Repository](https://github.com/Netflix/metaflow)
- [MetaFlow Tutorials](https://docs.metaflow.org/getting-started/tutorials)

