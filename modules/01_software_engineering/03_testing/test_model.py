"""
Unit tests for the MLModel class.
"""
import numpy as np
import pytest
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

from model import MLModel


class TestMLModel:
    """Test suite for the MLModel class."""
    
    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        return X_train, X_test, y_train, y_test
    
    def test_initialization(self):
        """Test model initialization."""
        model = MLModel()
        assert not model.is_fitted
        assert model.model is not None
        assert model.scaler is not None
    
    def test_fit(self, sample_data):
        """Test model fitting."""
        X_train, _, y_train, _ = sample_data
        model = MLModel()
        model.fit(X_train, y_train)
        assert model.is_fitted
    
    def test_fit_with_invalid_data(self):
        """Test model fitting with invalid data."""
        X = np.array([[1, 2], [3, 4], [5, 6]])
        y = np.array([1, 2])  # Different number of samples
        model = MLModel()
        with pytest.raises(ValueError):
            model.fit(X, y)
    
    def test_predict(self, sample_data):
        """Test model prediction."""
        X_train, X_test, y_train, _ = sample_data
        model = MLModel()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        assert len(predictions) == len(X_test)
    
    def test_predict_without_fitting(self, sample_data):
        """Test prediction without fitting the model first."""
        _, X_test, _, _ = sample_data
        model = MLModel()
        with pytest.raises(ValueError):
            model.predict(X_test)
    
    def test_score(self, sample_data):
        """Test model scoring."""
        X_train, X_test, y_train, y_test = sample_data
        model = MLModel()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        assert 0 <= score <= 1  # R^2 score should be between 0 and 1 for this data
    
    def test_get_feature_importance(self, sample_data):
        """Test getting feature importance."""
        X_train, _, y_train, _ = sample_data
        model = MLModel()
        model.fit(X_train, y_train)
        importance = model.get_feature_importance()
        assert len(importance) == X_train.shape[1]
    
    def test_get_feature_importance_without_fitting(self):
        """Test getting feature importance without fitting the model first."""
        model = MLModel()
        with pytest.raises(ValueError):
            model.get_feature_importance()


if __name__ == "__main__":
    pytest.main(["-xvs", "test_model.py"])

