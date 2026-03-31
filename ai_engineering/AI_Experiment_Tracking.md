# Skill: AI Experiment Tracking

## Purpose
To systematically track machine learning experiments, including hyperparameters, metrics, artifacts, and results for reproducibility and optimization.

## When to Use
- When running multiple ML experiments with different configurations
- When comparing model performance across different approaches
- When needing to reproduce experimental results
- When optimizing hyperparameters and model architectures

## Procedure

### 1. Experiment Tracking Framework
Create a comprehensive experiment tracking system.

```python
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import hashlib
import pandas as pd
import matplotlib.pyplot as plt

class ExperimentTracker:
    """Track machine learning experiments."""
    
    def __init__(self, project_name: str, base_dir: str = "./experiments"):
        self.project_name = project_name
        self.base_dir = Path(base_dir)
        self.project_dir = self.base_dir / project_name
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        self.current_experiment = None
        self.logger = logging.getLogger(f"ExperimentTracker.{project_name}")
        
        # Initialize experiment registry
        self.registry_file = self.project_dir / "experiments_registry.json"
        self._init_registry()
    
    def _init_registry(self):
        """Initialize experiments registry."""
        if not self.registry_file.exists():
            self._save_registry({"experiments": [], "total": 0})
    
    def _load_registry(self) -> Dict[str, Any]:
        """Load experiments registry."""
        with open(self.registry_file, 'r') as f:
            return json.load(f)
    
    def _save_registry(self, registry: Dict[str, Any]):
        """Save experiments registry."""
        with open(self.registry_file, 'w') as f:
            json.dump(registry, f, indent=2)
    
    def start_experiment(self, name: str, description: str = "", tags: List[str] = None) -> str:
        """Start a new experiment."""
        experiment_id = self._generate_experiment_id(name)
        
        experiment = {
            "id": experiment_id,
            "name": name,
            "description": description,
            "tags": tags or [],
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "status": "running",
            "hyperparameters": {},
            "metrics": {},
            "artifacts": [],
            "metadata": {}
        }
        
        # Create experiment directory
        experiment_dir = self.project_dir / experiment_id
        experiment_dir.mkdir(exist_ok=True)
        
        # Update registry
        registry = self._load_registry()
        registry["experiments"].append(experiment)
        registry["total"] += 1
        self._save_registry(registry)
        
        self.current_experiment = experiment
        self.logger.info(f"Started experiment: {name} (ID: {experiment_id})")
        
        return experiment_id
    
    def log_hyperparameters(self, params: Dict[str, Any]):
        """Log hyperparameters for current experiment."""
        if not self.current_experiment:
            raise ValueError("No active experiment. Call start_experiment() first.")
        
        self.current_experiment["hyperparameters"].update(params)
        self._update_current_experiment()
        self.logger.info(f"Logged hyperparameters: {params}")
    
    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        """Log metrics for current experiment."""
        if not self.current_experiment:
            raise ValueError("No active experiment. Call start_experiment() first.")
        
        if step is not None:
            if "metric_history" not in self.current_experiment:
                self.current_experiment["metric_history"] = {}
            
            for metric_name, value in metrics.items():
                if metric_name not in self.current_experiment["metric_history"]:
                    self.current_experiment["metric_history"][metric_name] = []
                
                self.current_experiment["metric_history"][metric_name].append({
                    "step": step,
                    "value": value,
                    "timestamp": datetime.now().isoformat()
                })
        
        self.current_experiment["metrics"].update(metrics)
        self._update_current_experiment()
        self.logger.info(f"Logged metrics: {metrics}")
    
    def log_artifact(self, artifact_path: str, artifact_type: str = "file"):
        """Log an artifact for current experiment."""
        if not self.current_experiment:
            raise ValueError("No active experiment. Call start_experiment() first.")
        
        import shutil
        experiment_dir = self.project_dir / self.current_experiment["id"]
        artifact_name = Path(artifact_path).name
        dest_path = experiment_dir / "artifacts" / artifact_name
        
        # Create artifacts directory
        dest_path.parent.mkdir(exist_ok=True)
        
        # Copy artifact
        shutil.copy2(artifact_path, dest_path)
        
        artifact_info = {
            "name": artifact_name,
            "type": artifact_type,
            "original_path": artifact_path,
            "stored_path": str(dest_path),
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_experiment["artifacts"].append(artifact_info)
        self._update_current_experiment()
        self.logger.info(f"Logged artifact: {artifact_name}")
    
    def end_experiment(self, status: str = "completed"):
        """End the current experiment."""
        if not self.current_experiment:
            raise ValueError("No active experiment to end.")
        
        self.current_experiment["end_time"] = datetime.now().isoformat()
        self.current_experiment["status"] = status
        self._update_current_experiment()
        
        self.logger.info(f"Ended experiment: {self.current_experiment['name']} (status: {status})")
        self.current_experiment = None
    
    def _update_current_experiment(self):
        """Update current experiment in registry."""
        if not self.current_experiment:
            return
        
        registry = self._load_registry()
        for i, exp in enumerate(registry["experiments"]):
            if exp["id"] == self.current_experiment["id"]:
                registry["experiments"][i] = self.current_experiment
                break
        
        self._save_registry(registry)
    
    def _generate_experiment_id(self, name: str) -> str:
        """Generate unique experiment ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"exp_{timestamp}_{name_hash}"
    
    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        """Get experiment by ID."""
        registry = self._load_registry()
        for exp in registry["experiments"]:
            if exp["id"] == experiment_id:
                return exp
        return None
    
    def list_experiments(self, status: Optional[str] = None, tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """List experiments with optional filtering."""
        registry = self._load_registry()
        experiments = registry["experiments"]
        
        if status:
            experiments = [exp for exp in experiments if exp["status"] == status]
        
        if tags:
            experiments = [exp for exp in experiments if any(tag in exp["tags"] for tag in tags)]
        
        return experiments
    
    def compare_experiments(self, experiment_ids: List[str]) -> pd.DataFrame:
        """Compare experiments side by side."""
        experiments = []
        for exp_id in experiment_ids:
            exp = self.get_experiment(exp_id)
            if exp:
                experiments.append(exp)
        
        if not experiments:
            return pd.DataFrame()
        
        comparison_data = []
        for exp in experiments:
            row = {
                "id": exp["id"],
                "name": exp["name"],
                "status": exp["status"],
                **exp["hyperparameters"],
                **exp["metrics"]
            }
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
```

### 2. Automated Hyperparameter Logging
Automatically track hyperparameters.

```python
from functools import wraps

def track_hyperparameters(tracker: ExperimentTracker):
    """Decorator to automatically track function parameters as hyperparameters."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract hyperparameters from function arguments
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Log all parameters as hyperparameters
            params = dict(bound_args.arguments)
            # Remove self parameter if present
            params.pop('self', None)
            params.pop('tracker', None)
            
            tracker.log_hyperparameters(params)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
# @track_hyperparameters(tracker)
# def train_model(learning_rate, batch_size, epochs, model_type):
#     # Training code here
#     pass
```

### 3. Metrics Visualization
Create visualizations for experiment comparison.

```python
class ExperimentVisualizer:
    """Visualize experiment results."""
    
    def __init__(self, tracker: ExperimentTracker):
        self.tracker = tracker
    
    def plot_metric_comparison(self, metric_name: str, top_n: int = 10):
        """Plot metric comparison across experiments."""
        experiments = self.tracker.list_experiments(status="completed")
        
        # Filter experiments that have the metric
        valid_experiments = [
            exp for exp in experiments 
            if metric_name in exp["metrics"]
        ]
        
        if not valid_experiments:
            print(f"No experiments found with metric: {metric_name}")
            return
        
        # Sort by metric value
        valid_experiments.sort(key=lambda x: x["metrics"][metric_name])
        
        # Take top N
        top_experiments = valid_experiments[:top_n]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        names = [exp["name"] for exp in top_experiments]
        values = [exp["metrics"][metric_name] for exp in top_experiments]
        
        plt.bar(range(len(names)), values)
        plt.xticks(range(len(names)), names, rotation=45, ha='right')
        plt.ylabel(metric_name)
        plt.title(f'{metric_name} Comparison (Top {top_n})')
        plt.tight_layout()
        
        # Save plot
        output_path = self.tracker.project_dir / f"{metric_name}_comparison.png"
        plt.savefig(output_path)
        plt.close()
        
        print(f"Plot saved to: {output_path}")
    
    def plot_training_curves(self, experiment_id: str, metric_name: str):
        """Plot training curves for a specific experiment."""
        exp = self.tracker.get_experiment(experiment_id)
        
        if not exp or "metric_history" not in exp:
            print(f"No metric history found for experiment: {experiment_id}")
            return
        
        if metric_name not in exp["metric_history"]:
            print(f"Metric {metric_name} not found in experiment history")
            return
        
        # Extract data
        history = exp["metric_history"][metric_name]
        steps = [entry["step"] for entry in history]
        values = [entry["value"] for entry in history]
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(steps, values, marker='o')
        plt.xlabel("Step")
        plt.ylabel(metric_name)
        plt.title(f'{metric_name} Training Curve - {exp["name"]}')
        plt.grid(True)
        
        # Save plot
        output_path = self.tracker.project_dir / f"{experiment_id}_{metric_name}_curve.png"
        plt.savefig(output_path)
        plt.close()
        
        print(f"Training curve saved to: {output_path}")
    
    def create_experiment_report(self, experiment_id: str) -> str:
        """Create a comprehensive experiment report."""
        exp = self.tracker.get_experiment(experiment_id)
        
        if not exp:
            return f"Experiment not found: {experiment_id}"
        
        report = f"""
Experiment Report
{'=' * 50}

Name: {exp['name']}
ID: {exp['id']}
Status: {exp['status']}
Description: {exp['description']}

Timeline:
- Started: {exp['start_time']}
- Ended: {exp['end_time'] or 'Running'}

Tags: {', '.join(exp['tags']) if exp['tags'] else 'None'}

Hyperparameters:
"""
        for param, value in exp['hyperparameters'].items():
            report += f"- {param}: {value}\n"
        
        report += f"\nFinal Metrics:\n"
        for metric, value in exp['metrics'].items():
            report += f"- {metric}: {value}\n"
        
        if exp['artifacts']:
            report += f"\nArtifacts ({len(exp['artifacts'])}):\n"
            for artifact in exp['artifacts']:
                report += f"- {artifact['name']} ({artifact['type']})\n"
        
        return report
```

### 4. Model Artifact Management
Manage model artifacts and versions.

```python
import joblib
import pickle

class ModelArtifactManager:
    """Manage model artifacts with versioning."""
    
    def __init__(self, tracker: ExperimentTracker):
        self.tracker = tracker
        self.artifacts_dir = tracker.project_dir / "artifacts"
        self.artifacts_dir.mkdir(exist_ok=True)
    
    def save_model(self, model, model_name: str, framework: str = "sklearn"):
        """Save model and log as artifact."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artifact_filename = f"{model_name}_{timestamp}.joblib"
        artifact_path = self.artifacts_dir / artifact_filename
        
        # Save model
        if framework == "sklearn":
            joblib.dump(model, artifact_path)
        elif framework == "pickle":
            with open(artifact_path, 'wb') as f:
                pickle.dump(model, f)
        else:
            raise ValueError(f"Unsupported framework: {framework}")
        
        # Log artifact
        self.tracker.log_artifact(str(artifact_path), artifact_type="model")
        
        return artifact_path
    
    def load_model(self, artifact_path: str):
        """Load model from artifact."""
        if artifact_path.endswith('.joblib'):
            return joblib.load(artifact_path)
        elif artifact_path.endswith('.pkl'):
            with open(artifact_path, 'rb') as f:
                return pickle.load(f)
        else:
            raise ValueError(f"Unsupported artifact format: {artifact_path}")
    
    def compare_model_versions(self, model_name: str) -> pd.DataFrame:
        """Compare different versions of a model."""
        experiments = self.tracker.list_experiments()
        
        model_versions = []
        for exp in experiments:
            for artifact in exp['artifacts']:
                if artifact['name'].startswith(model_name) and artifact['type'] == 'model':
                    model_versions.append({
                        'experiment_id': exp['id'],
                        'experiment_name': exp['name'],
                        'artifact_name': artifact['name'],
                        'created': artifact['timestamp'],
                        **exp['metrics']
                    })
        
        return pd.DataFrame(model_versions)
```

### 5. Experiment Analysis and Insights
Analyze experiments to derive insights.

```python
class ExperimentAnalyzer:
    """Analyze experiments to provide insights."""
    
    def __init__(self, tracker: ExperimentTracker):
        self.tracker = tracker
    
    def find_best_experiment(self, metric_name: str, higher_is_better: bool = True) -> Optional[Dict[str, Any]]:
        """Find the best performing experiment for a given metric."""
        experiments = self.tracker.list_experiments(status="completed")
        
        valid_experiments = [
            exp for exp in experiments
            if metric_name in exp["metrics"]
        ]
        
        if not valid_experiments:
            return None
        
        if higher_is_better:
            best_exp = max(valid_experiments, key=lambda x: x["metrics"][metric_name])
        else:
            best_exp = min(valid_experiments, key=lambda x: x["metrics"][metric_name])
        
        return best_exp
    
    def analyze_hyperparameter_importance(self, metric_name: str) -> pd.DataFrame:
        """Analyze the importance of hyperparameters on a metric."""
        experiments = self.tracker.list_experiments(status="completed")
        
        valid_experiments = [
            exp for exp in experiments
            if metric_name in exp["metrics"]
        ]
        
        if not valid_experiments:
            return pd.DataFrame()
        
        # Create analysis data
        analysis_data = []
        for exp in valid_experiments:
            row = {
                "experiment_id": exp["id"],
                "experiment_name": exp["name"],
                "metric_value": exp["metrics"][metric_name]
            }
            # Add all hyperparameters
            row.update(exp["hyperparameters"])
            analysis_data.append(row)
        
        df = pd.DataFrame(analysis_data)
        
        # Calculate correlations for numeric hyperparameters
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            correlations = df[numeric_cols].corr()['metric_value'].sort_values(ascending=False)
            return correlations
        
        return df
    
    def generate_experiment_summary(self) -> str:
        """Generate a summary of all experiments."""
        experiments = self.tracker.list_experiments()
        
        summary = f"""
Experiment Summary for {self.tracker.project_name}
{'=' * 60}

Total Experiments: {len(experiments)}

Status Breakdown:
"""
        status_counts = {}
        for exp in experiments:
            status = exp["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for status, count in sorted(status_counts.items()):
            summary += f"- {status}: {count}\n"
        
        if status_counts.get("completed", 0) > 0:
            summary += f"\nCompleted Experiments: {status_counts['completed']}\n"
            summary += "Best performing experiments by common metrics:\n"
            
            common_metrics = {}
            for exp in experiments:
                if exp["status"] == "completed":
                    for metric in exp["metrics"].keys():
                        if metric not in common_metrics:
                            common_metrics[metric] = []
                        common_metrics[metric].append((exp["name"], exp["metrics"][metric]))
            
            for metric, values in common_metrics.items():
                best = max(values, key=lambda x: x[1])
                summary += f"- {metric}: {best[0]} ({best[1]:.4f})\n"
        
        return summary
```

### 6. Complete Example Usage
Demonstrate complete experiment tracking workflow.

```python
def example_experiment_tracking():
    """Demonstrate complete experiment tracking."""
    
    # Initialize tracker
    tracker = ExperimentTracker(project_name="sentiment_analysis")
    
    # Start experiment
    exp_id = tracker.start_experiment(
        name="random_forest_baseline",
        description="Random Forest baseline model for sentiment analysis",
        tags=["baseline", "random_forest"]
    )
    
    # Log hyperparameters
    tracker.log_hyperparameters({
        "model_type": "random_forest",
        "n_estimators": 100,
        "max_depth": 10,
        "min_samples_split": 2,
        "learning_rate": None
    })
    
    # Simulate training and log metrics
    import numpy as np
    for epoch in range(10):
        # Simulate training
        train_loss = 1.0 - (epoch * 0.08)
        val_loss = 1.0 - (epoch * 0.07) + np.random.normal(0, 0.05)
        
        tracker.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "epoch": epoch
        }, step=epoch)
    
    # Log final metrics
    tracker.log_metrics({
        "train_accuracy": 0.92,
        "val_accuracy": 0.87,
        "test_accuracy": 0.85,
        "f1_score": 0.84,
        "precision": 0.86,
        "recall": 0.82
    })
    
    # Save model artifact
    artifact_manager = ModelArtifactManager(tracker)
    import joblib
    dummy_model = {"model": "dummy_model", "accuracy": 0.85}
    joblib.dump(dummy_model, "dummy_model.joblib")
    artifact_manager.save_model(dummy_model, "sentiment_model")
    
    # End experiment
    tracker.end_experiment(status="completed")
    
    # Create visualizations
    visualizer = ExperimentVisualizer(tracker)
    visualizer.plot_metric_comparison("test_accuracy")
    visualizer.plot_training_curves(exp_id, "train_loss")
    
    # Generate report
    report = visualizer.create_experiment_report(exp_id)
    print(report)
    
    # Analyze experiments
    analyzer = ExperimentAnalyzer(tracker)
    best_exp = analyzer.find_best_experiment("test_accuracy")
    print(f"\nBest experiment: {best_exp['name']} with accuracy {best_exp['metrics']['test_accuracy']}")
    
    summary = analyzer.generate_experiment_summary()
    print(summary)

# Usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    example_experiment_tracking()
```

## Constraints
- **Storage Space**: Experiment artifacts can consume significant storage
- **Performance**: Extensive logging may impact training performance
- **Reproducibility**: Ensure complete environment capture for true reproducibility
- **Scalability**: Consider scalability for large numbers of experiments
- **Privacy**: Be careful with sensitive data in experiment logs
- **Organization**: Maintain consistent naming and tagging conventions

## Expected Output
Comprehensive experiment tracking system that captures all aspects of ML experiments, enables detailed comparison and analysis, and provides insights for model optimization.
