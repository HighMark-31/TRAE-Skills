# Skill: Federated Learning

## Purpose
To train machine learning models across decentralized edge devices while keeping data local, preserving privacy and reducing data transfer requirements.

## When to Use
- When training on sensitive data that cannot leave devices
- When building healthcare or financial applications with privacy requirements
- When reducing data transfer costs in distributed systems
- When compliance with data protection regulations (GDPR, HIPAA)

## Procedure

### 1. Federated Learning Architecture
Set up the federated learning framework.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from copy import deepcopy
import numpy as np

class FederatedLearningServer:
    def __init__(self, global_model, learning_rate=0.01):
        self.global_model = global_model
        self.learning_rate = learning_rate
        self.client_weights = []
    
    def aggregate_models(self, client_models, client_weights=None):
        """Aggregate client models using FedAvg algorithm."""
        if client_weights is None:
            # Equal weights for all clients
            client_weights = [1.0 / len(client_models)] * len(client_models)
        
        # Get global model state dict
        global_state = self.global_model.state_dict()
        
        # Initialize aggregated state
        aggregated_state = deepcopy(global_state)
        for key in aggregated_state.keys():
            aggregated_state[key] = torch.zeros_like(aggregated_state[key])
        
        # Aggregate weights from all clients
        for client_model, weight in zip(client_models, client_weights):
            client_state = client_model.state_dict()
            for key in aggregated_state.keys():
                aggregated_state[key] += weight * client_state[key]
        
        # Update global model
        self.global_model.load_state_dict(aggregated_state)
        
        return self.global_model
    
    def distribute_model(self):
        """Send global model to clients."""
        return deepcopy(self.global_model)

class FederatedLearningClient:
    def __init__(self, local_model, local_data, optimizer_type='adam', learning_rate=0.01):
        self.local_model = local_model
        self.local_data = local_data
        self.optimizer = optim.Adam(self.local_model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss()
    
    def train_local(self, epochs=5, batch_size=32):
        """Train model on local data."""
        self.local_model.train()
        
        # Assume local_data is a DataLoader
        for epoch in range(epochs):
            for batch_x, batch_y in self.local_data:
                self.optimizer.zero_grad()
                
                outputs = self.local_model(batch_x)
                loss = self.criterion(outputs, batch_y)
                
                loss.backward()
                self.optimizer.step()
        
        return self.local_model
    
    def update_model(self, global_model):
        """Update local model with global model."""
        self.local_model.load_state_dict(global_model.state_dict())
        return self.local_model
```

### 2. Differential Privacy Integration
Add privacy guarantees to federated learning.

```python
import torch.nn.functional as F

class DifferentialPrivacyClient:
    def __init__(self, model, local_data, clip_norm=1.0, noise_multiplier=0.1):
        self.model = model
        self.local_data = local_data
        self.clip_norm = clip_norm
        self.noise_multiplier = noise_multiplier
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.CrossEntropyLoss()
    
    def clip_gradients(self):
        """Clip gradients to bound sensitivity."""
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.clip_norm)
    
    def add_noise(self, parameters):
        """Add Gaussian noise to gradients."""
        with torch.no_grad():
            for param in parameters:
                noise = torch.randn_like(param) * self.noise_multiplier * self.clip_norm
                param.grad += noise
    
    def train_with_dp(self, epochs=5):
        """Train with differential privacy."""
        self.model.train()
        
        for epoch in range(epochs):
            for batch_x, batch_y in self.local_data:
                self.optimizer.zero_grad()
                
                outputs = self.model(batch_x)
                loss = self.criterion(outputs, batch_y)
                
                loss.backward()
                
                # Apply differential privacy
                self.clip_gradients()
                self.add_noise(self.model.parameters())
                
                self.optimizer.step()
        
        return self.model
    
    def compute_privacy_spent(self, epochs, noise_multiplier, sample_rate):
        """Compute privacy budget spent."""
        # Simplified privacy accounting
        # In practice, use moments accountant or RDP accountant
        epsilon = epochs * sample_rate / noise_multiplier
        return epsilon
```

### 3. Secure Aggregation
Implement secure aggregation protocols.

```python
import hashlib
import random

class SecureAggregationServer:
    def __init__(self, global_model):
        self.global_model = global_model
        self.client_seeds = {}
    
    def distribute_seeds(self, client_ids):
        """Distribute random seeds to clients."""
        seeds = {}
        for client_id in client_ids:
            seeds[client_id] = random.randint(0, 1000000)
            self.client_seeds[client_id] = seeds[client_id]
        return seeds
    
    def secure_aggregate(self, client_updates):
        """Aggregate updates with one-time masking."""
        # In real implementation, use cryptographic protocols
        # This is a simplified version
        
        aggregated_update = {}
        
        # Remove masks (in real FL, clients mask each other's updates)
        for client_id, update in client_updates.items():
            for key, value in update.items():
                if key not in aggregated_update:
                    aggregated_update[key] = value
                else:
                    aggregated_update[key] += value
        
        # Average the updates
        num_clients = len(client_updates)
        for key in aggregated_update:
            aggregated_update[key] /= num_clients
        
        # Update global model
        global_state = self.global_model.state_dict()
        for key, value in aggregated_update.items():
            if key in global_state:
                global_state[key] += value
        
        self.global_model.load_state_dict(global_state)
        return self.global_model

class SecureAggregationClient:
    def __init__(self, model, data):
        self.model = model
        self.data = data
    
    def compute_model_update(self, global_model):
        """Compute model update (difference from global model)."""
        update = {}
        global_state = global_model.state_dict()
        local_state = self.model.state_dict()
        
        for key in global_state:
            update[key] = local_state[key] - global_state[key]
        
        return update
    
    def apply_mask(self, update, seed):
        """Apply random mask to update."""
        random.seed(seed)
        masked_update = {}
        
        for key, value in update.items():
            # Generate random mask
            mask = torch.randn_like(value) * 0.01
            masked_update[key] = value + mask
        
        return masked_update
```

### 4. Federated Learning Simulation
Simulate federated learning across multiple clients.

```python
from torch.utils.data import DataLoader, TensorDataset
import torchvision
import torchvision.transforms as transforms

def create_client_datasets(num_clients=10, samples_per_client=1000):
    """Create local datasets for each client."""
    # Load MNIST dataset
    transform = transforms.Compose([transforms.ToTensor()])
    mnist = torchvision.datasets.MNIST(root='./data', train=True, 
                                       download=True, transform=transform)
    
    # Split data among clients (non-IID)
    client_datasets = []
    data_per_client = len(mnist) // num_clients
    
    for i in range(num_clients):
        start_idx = i * data_per_client
        end_idx = (i + 1) * data_per_client
        
        # Create non-IID distribution by sorting labels
        data_subset = torch.utils.data.Subset(mnist, range(start_idx, end_idx))
        client_datasets.append(DataLoader(data_subset, batch_size=32, shuffle=True))
    
    return client_datasets

def run_federated_learning(num_rounds=10, num_clients=10, local_epochs=5):
    """Run federated learning simulation."""
    # Create global model
    global_model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(784, 128),
        nn.ReLU(),
        nn.Linear(128, 10)
    )
    
    # Create server
    server = FederatedLearningServer(global_model)
    
    # Create clients
    client_datasets = create_client_datasets(num_clients)
    clients = []
    
    for data in client_datasets:
        client_model = deepcopy(global_model)
        client = FederatedLearningClient(client_model, data)
        clients.append(client)
    
    # Training rounds
    for round_num in range(num_rounds):
        print(f"Round {round_num + 1}/{num_rounds}")
        
        # Distribute global model
        global_model_state = server.distribute_model()
        
        # Select subset of clients (client sampling)
        selected_clients = random.sample(clients, min(5, len(clients)))
        
        # Local training
        client_models = []
        for client in selected_clients:
            client.update_model(global_model_state)
            updated_model = client.train_local(epochs=local_epochs)
            client_models.append(updated_model)
        
        # Aggregate models
        server.aggregate_models(client_models)
        
        # Evaluate global model (simplified)
        print(f"  Completed training with {len(client_models)} clients")
    
    return global_model

# Usage
# global_model = run_federated_learning(num_rounds=10, num_clients=10, local_epochs=5)
# print("Federated learning completed!")
```

### 5. Monitoring and Evaluation
Monitor federated learning progress.

```python
class FederatedLearningMonitor:
    def __init__(self):
        self.metrics = {
            'round': [],
            'client_accuracies': [],
            'global_accuracy': [],
            'communication_cost': [],
            'privacy_budget': []
        }
    
    def log_round(self, round_num, client_metrics, global_accuracy, comm_cost, privacy_epsilon):
        """Log metrics for a round."""
        self.metrics['round'].append(round_num)
        self.metrics['client_accuracies'].append(client_metrics)
        self.metrics['global_accuracy'].append(global_accuracy)
        self.metrics['communication_cost'].append(comm_cost)
        self.metrics['privacy_budget'].append(privacy_epsilon)
    
    def evaluate_global_model(self, model, test_loader):
        """Evaluate global model on test data."""
        model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for batch_x, batch_y in test_loader:
                outputs = model(batch_x)
                _, predicted = torch.max(outputs.data, 1)
                total += batch_y.size(0)
                correct += (predicted == batch_y).sum().item()
        
        accuracy = 100 * correct / total
        return accuracy
    
    def generate_report(self):
        """Generate training report."""
        import matplotlib.pyplot as plt
        
        # Plot global accuracy over rounds
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.plot(self.metrics['round'], self.metrics['global_accuracy'])
        plt.xlabel('Round')
        plt.ylabel('Global Accuracy (%)')
        plt.title('Global Model Performance')
        
        plt.subplot(1, 3, 2)
        plt.plot(self.metrics['round'], self.metrics['communication_cost'])
        plt.xlabel('Round')
        plt.ylabel('Communication Cost (MB)')
        plt.title('Communication Overhead')
        
        plt.subplot(1, 3, 3)
        plt.plot(self.metrics['round'], self.metrics['privacy_budget'])
        plt.xlabel('Round')
        plt.ylabel('Privacy Budget (ε)')
        plt.title('Privacy Budget Consumption')
        
        plt.tight_layout()
        plt.savefig('federated_learning_metrics.png')
        plt.close()
        
        return "Federated learning metrics saved to federated_learning_metrics.png"

# Usage
# monitor = FederatedLearningMonitor()
# monitor.log_round(1, [85.2, 87.1, 86.5], 86.0, 5.2, 0.1)
# monitor.generate_report()
```

## Constraints
- **Communication Overhead**: Frequent model updates can be bandwidth-intensive
- **Heterogeneity**: Non-IID data across clients can hurt convergence
- **Privacy-Utility Tradeoff**: Stronger privacy protection may reduce model accuracy
- **System Complexity**: Federated learning systems are complex to implement and maintain
- **Client Availability**: Clients may be unavailable or have varying capabilities
- **Scalability**: Large numbers of clients present coordination challenges

## Expected Output
A privacy-preserving machine learning system that trains models across decentralized devices while maintaining data locality and providing strong privacy guarantees.
