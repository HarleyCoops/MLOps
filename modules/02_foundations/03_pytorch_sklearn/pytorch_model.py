"""
Example of creating, training, and saving a PyTorch model.
"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset


class SimpleNN(nn.Module):
    """
    A simple neural network for regression.
    """
    
    def __init__(self, input_dim, hidden_dim, output_dim):
        """
        Initialize the neural network.
        
        Parameters:
        -----------
        input_dim : int
            Input dimension
        hidden_dim : int
            Hidden dimension
        output_dim : int
            Output dimension
        """
        super(SimpleNN, self).__init__()
        
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.activation = nn.ReLU()
        self.layer2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        """
        Forward pass.
        
        Parameters:
        -----------
        x : torch.Tensor
            Input tensor
            
        Returns:
        --------
        torch.Tensor
            Output tensor
        """
        x = self.layer1(x)
        x = self.activation(x)
        x = self.layer2(x)
        return x


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


def train_model(model, X_train, y_train, X_val, y_val, epochs=100, batch_size=32, lr=0.01):
    """
    Train the PyTorch model.
    
    Parameters:
    -----------
    model : torch.nn.Module
        PyTorch model
    X_train : numpy.ndarray
        Training features
    y_train : numpy.ndarray
        Training target
    X_val : numpy.ndarray
        Validation features
    y_val : numpy.ndarray
        Validation target
    epochs : int
        Number of epochs
    batch_size : int
        Batch size
    lr : float
        Learning rate
        
    Returns:
    --------
    model : torch.nn.Module
        Trained PyTorch model
    train_losses : list
        Training losses
    val_losses : list
        Validation losses
    """
    # Convert data to PyTorch tensors
    X_train_tensor = torch.FloatTensor(X_train)
    y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)
    X_val_tensor = torch.FloatTensor(X_val)
    y_val_tensor = torch.FloatTensor(y_val).unsqueeze(1)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Training loop
    train_losses = []
    val_losses = []
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        
        for X_batch, y_batch in train_loader:
            # Zero the gradients
            optimizer.zero_grad()
            
            # Forward pass
            y_pred = model(X_batch)
            
            # Compute loss
            loss = criterion(y_pred, y_batch)
            
            # Backward pass
            loss.backward()
            
            # Update weights
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        train_losses.append(train_loss)
        
        # Validation
        model.eval()
        with torch.no_grad():
            y_val_pred = model(X_val_tensor)
            val_loss = criterion(y_val_pred, y_val_tensor).item()
            val_losses.append(val_loss)
        
        # Print progress
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
    
    return model, train_losses, val_losses


def save_model(model, path):
    """
    Save the PyTorch model.
    
    Parameters:
    -----------
    model : torch.nn.Module
        PyTorch model
    path : str
        Path to save the model
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Save the model
    torch.save(model.state_dict(), path)
    print(f"Model saved to {path}")


def load_model(path, input_dim, hidden_dim, output_dim):
    """
    Load the PyTorch model.
    
    Parameters:
    -----------
    path : str
        Path to the saved model
    input_dim : int
        Input dimension
    hidden_dim : int
        Hidden dimension
    output_dim : int
        Output dimension
        
    Returns:
    --------
    model : torch.nn.Module
        Loaded PyTorch model
    """
    # Create a new model instance
    model = SimpleNN(input_dim, hidden_dim, output_dim)
    
    # Load the model weights
    model.load_state_dict(torch.load(path))
    
    # Set the model to evaluation mode
    model.eval()
    
    print(f"Model loaded from {path}")
    
    return model


def plot_losses(train_losses, val_losses):
    """
    Plot the training and validation losses.
    
    Parameters:
    -----------
    train_losses : list
        Training losses
    val_losses : list
        Validation losses
    """
    plt.figure(figsize=(10, 6))
    plt.plot(train_losses, label="Training Loss")
    plt.plot(val_losses, label="Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Training and Validation Losses")
    plt.legend()
    plt.grid(True)
    plt.savefig("losses.png")
    plt.close()


def main():
    """
    Main function.
    """
    # Set random seed for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Generate data
    X, y = generate_data(n_samples=1000, n_features=10, noise=0.1)
    
    # Split data into training and validation sets
    train_size = int(0.8 * len(X))
    X_train, X_val = X[:train_size], X[train_size:]
    y_train, y_val = y[:train_size], y[train_size:]
    
    # Create model
    input_dim = X_train.shape[1]
    hidden_dim = 20
    output_dim = 1
    model = SimpleNN(input_dim, hidden_dim, output_dim)
    
    # Train model
    model, train_losses, val_losses = train_model(
        model, X_train, y_train, X_val, y_val, epochs=100, batch_size=32, lr=0.01
    )
    
    # Plot losses
    plot_losses(train_losses, val_losses)
    
    # Save model
    save_model(model, "models/pytorch_model.pt")
    
    # Load model
    loaded_model = load_model("models/pytorch_model.pt", input_dim, hidden_dim, output_dim)
    
    # Make predictions with loaded model
    X_val_tensor = torch.FloatTensor(X_val)
    with torch.no_grad():
        y_val_pred = loaded_model(X_val_tensor).numpy()
    
    # Calculate mean squared error
    mse = np.mean((y_val_pred.flatten() - y_val) ** 2)
    print(f"Mean Squared Error: {mse:.4f}")


if __name__ == "__main__":
    main()

