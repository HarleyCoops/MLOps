# CI/CD for ML Projects

This directory contains examples of Continuous Integration and Continuous Deployment (CI/CD) configurations for ML projects.

## Examples

- [GitHub Actions](./.github/workflows/ci.yml) - CI/CD configuration for GitHub Actions

## CI/CD for ML Projects

Continuous Integration and Continuous Deployment (CI/CD) are essential practices for ML projects to ensure code quality, reproducibility, and reliable deployments.

### CI/CD Pipeline for ML Projects

A typical CI/CD pipeline for ML projects includes the following stages:

1. **Code Linting and Formatting**: Check code quality and style
2. **Unit Testing**: Test individual components
3. **Integration Testing**: Test interactions between components
4. **Model Training**: Train the model with the latest code
5. **Model Evaluation**: Evaluate the model's performance
6. **Model Validation**: Validate the model against business requirements
7. **Model Packaging**: Package the model for deployment
8. **Deployment**: Deploy the model to the target environment
9. **Monitoring**: Monitor the model's performance in production

### GitHub Actions

GitHub Actions is a CI/CD platform that allows you to automate your build, test, and deployment pipeline directly from your GitHub repository.

The example [ci.yml](./.github/workflows/ci.yml) file demonstrates a CI/CD pipeline for an ML project using GitHub Actions, including:

- Setting up Python
- Installing dependencies
- Linting and formatting checks
- Running tests with coverage
- Building and saving the model
- Building and pushing a Docker image

### CircleCI

CircleCI is another popular CI/CD platform. Here's an example `config.yml` file for CircleCI:

```yaml
version: 2.1

orbs:
  python: circleci/python@1.4

jobs:
  test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - pytest
            - pytest-cov
            - flake8
            - black
      - run:
          name: Lint with flake8
          command: |
            flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
            flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - run:
          name: Check formatting with black
          command: |
            black --check .
      - run:
          name: Test with pytest
          command: |
            pytest --cov=. --cov-report=xml
      - store_artifacts:
          path: coverage.xml

  build:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - scikit-learn
            - pandas
            - numpy
      - run:
          name: Build model
          command: |
            python train_model.py
      - persist_to_workspace:
          root: .
          paths:
            - model.pkl

  deploy:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.7
      - attach_workspace:
          at: .
      - run:
          name: Build and push Docker image
          command: |
            docker build -t user/ml-model:latest .
            echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USERNAME --password-stdin
            docker push user/ml-model:latest

workflows:
  version: 2
  test-build-deploy:
    jobs:
      - test
      - build:
          requires:
            - test
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main
```

### Jenkins

Jenkins is a self-hosted CI/CD tool. Here's an example `Jenkinsfile` for a Jenkins pipeline:

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9'
        }
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-cov flake8 black'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                sh 'flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
                sh 'black --check .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --cov=. --cov-report=xml'
            }
            post {
                always {
                    junit 'test-results/*.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }
        
        stage('Build Model') {
            steps {
                sh 'python train_model.py'
            }
            post {
                success {
                    archiveArtifacts artifacts: 'model.pkl', fingerprint: true
                }
            }
        }
        
        stage('Build Docker Image') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t user/ml-model:latest .'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                    sh 'echo $DOCKERHUB_PASS | docker login -u $DOCKERHUB_USER --password-stdin'
                    sh 'docker push user/ml-model:latest'
                }
            }
        }
    }
}
```

## Best Practices for CI/CD in ML Projects

1. **Version Control Everything**: Code, data, models, and configurations should be version controlled.
2. **Automate Testing**: Automate unit tests, integration tests, and model validation.
3. **Reproducible Environments**: Use Docker or virtual environments to ensure reproducibility.
4. **Model Versioning**: Version your models and track their lineage.
5. **Artifact Management**: Store and version model artifacts.
6. **Environment Parity**: Ensure development, testing, and production environments are as similar as possible.
7. **Monitoring**: Implement monitoring for model performance and data drift.
8. **Rollback Strategy**: Have a strategy for rolling back to previous model versions if necessary.
9. **Security Scanning**: Include security scanning in your pipeline.
10. **Documentation**: Automate documentation generation and updates.

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CircleCI Documentation](https://circleci.com/docs/)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

