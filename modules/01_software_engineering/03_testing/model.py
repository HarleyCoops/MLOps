"""
Simple ML model class for demonstration.
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


class MLModel:
    """A simple ML model wrapper with preprocessing."""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = LinearRegression()
        self.is_fitted = False
    
    def fit(self, X, y):
        """
        Fit the model to the data.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Training data.
        y : array-like of shape (n_samples,)
            Target values.
            
        Returns:
        --------
        self : object
            Returns self.
        """
        # Check if X and y have the same number of samples
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples")
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit the model
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
        return self
    
    def predict(self, X):
        """
        Make predictions using the fitted model.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Data to predict.
            
        Returns:
        --------
        y_pred : array-like of shape (n_samples,)
            Predicted values.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet. Call fit() first.")
        
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        return self.model.predict(X_scaled)
    
    def score(self, X, y):
        """
        Calculate the coefficient of determination R^2 of the prediction.
        
        Parameters:
        -----------
        X : array-like of shape (n_samples, n_features)
            Test data.
        y : array-like of shape (n_samples,)
            True values.
            
        Returns:
        --------
        score : float
            R^2 of the prediction.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet. Call fit() first.")
        
        # Scale the features
        X_scaled = self.scaler.transform(X)
        
        # Calculate the score
        return self.model.score(X_scaled, y)
    
    def get_feature_importance(self):
        """
        Get the feature importance.
        
        Returns:
        --------
        importance : array-like of shape (n_features,)
            Feature importance.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been fitted yet. Call fit() first.")
        
        return self.model.coef_

