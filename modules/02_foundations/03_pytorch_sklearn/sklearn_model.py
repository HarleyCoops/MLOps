"""
Example of creating, training, and saving a scikit-learn model.
"""
import os
import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def generate_data(n_samples=1000, n_features=10, noise=0.1):
    """
    Generate synthetic data for regression.
    
    Parameters:
    -----------
    n_samples : int
        Number of samples
    n_features : int
        Number of features
    noise : float
        Noise level
        
    Returns:
    --------
    X : numpy.ndarray
        Features
    y : numpy.ndarray
        Target
    """
    # Generate random coefficients
    true_coefficients = np.random.randn(n_features)
    
    # Generate random features
    X = np.random.randn(n_samples, n_features)
    
    # Generate target with noise
    y = X.dot(true_coefficients) + noise * np.random.randn(n_samples)
    
    return X, y


def train_linear_model(X_train, y_train):
    """
    Train a linear regression model.
    
    Parameters:
    -----------
    X_train : numpy.ndarray
        Training features
    y_train : numpy.ndarray
        Training target
        
    Returns:
    --------
    model : sklearn.pipeline.Pipeline
        Trained model pipeline
    """
    # Create a pipeline with preprocessing and model
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])
    
    # Train the model
    model.fit(X_train, y_train)
    
    return model


def train_random_forest_model(X_train, y_train):
    """
    Train a random forest regression model.
    
    Parameters:
    -----------
    X_train : numpy.ndarray
        Training features
    y_train : numpy.ndarray
        Training target
        
    Returns:
    --------
    model : sklearn.pipeline.Pipeline
        Trained model pipeline
    """
    # Create a pipeline with preprocessing and model
    model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    # Train the model
    model.fit(X_train, y_train)
    
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model.
    
    Parameters:
    -----------
    model : sklearn.pipeline.Pipeline
        Trained model pipeline
    X_test : numpy.ndarray
        Test features
    y_test : numpy.ndarray
        Test target
        
    Returns:
    --------
    metrics : dict
        Evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return {
        'mse': mse,
        'rmse': np.sqrt(mse),
        'r2': r2
    }


def save_model(model, path):
    """
    Save the model.
    
    Parameters:
    -----------
    model : sklearn.pipeline.Pipeline
        Trained model pipeline
    path : str
        Path to save the model
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Save the model
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {path}")


def load_model(path):
    """
    Load the model.
    
    Parameters:
    -----------
    path : str
        Path to the saved model
        
    Returns:
    --------
    model : sklearn.pipeline.Pipeline
        Loaded model pipeline
    """
    # Load the model
    with open(path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"Model loaded from {path}")
    
    return model


def plot_predictions(y_test, y_pred, model_name):
    """
    Plot actual vs predicted values.
    
    Parameters:
    -----------
    y_test : numpy.ndarray
        Actual values
    y_pred : numpy.ndarray
        Predicted values
    model_name : str
        Name of the model
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title(f'{model_name}: Actual vs Predicted')
    plt.grid(True)
    plt.savefig(f"{model_name.lower().replace(' ', '_')}_predictions.png")
    plt.close()


def main():
    """
    Main function.
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate data
    X, y = generate_data(n_samples=1000, n_features=10, noise=0.1)
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train linear model
    linear_model = train_linear_model(X_train, y_train)
    
    # Evaluate linear model
    linear_metrics = evaluate_model(linear_model, X_test, y_test)
    print("Linear Regression Metrics:")
    for metric, value in linear_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Train random forest model
    rf_model = train_random_forest_model(X_train, y_train)
    
    # Evaluate random forest model
    rf_metrics = evaluate_model(rf_model, X_test, y_test)
    print("\nRandom Forest Metrics:")
    for metric, value in rf_metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Save models
    save_model(linear_model, "models/linear_model.pkl")
    save_model(rf_model, "models/random_forest_model.pkl")
    
    # Load models
    loaded_linear_model = load_model("models/linear_model.pkl")
    loaded_rf_model = load_model("models/random_forest_model.pkl")
    
    # Make predictions with loaded models
    linear_pred = loaded_linear_model.predict(X_test)
    rf_pred = loaded_rf_model.predict(X_test)
    
    # Plot predictions
    plot_predictions(y_test, linear_pred, "Linear Regression")
    plot_predictions(y_test, rf_pred, "Random Forest")


if __name__ == "__main__":
    main()

