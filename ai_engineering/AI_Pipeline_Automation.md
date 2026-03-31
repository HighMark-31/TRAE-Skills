# Skill: AI Pipeline Automation

## Purpose
To create automated end-to-end machine learning pipelines that handle data ingestion, preprocessing, training, evaluation, and deployment.

## When to Use
- When building production ML systems
- When implementing continuous training and deployment
- When scaling ML workflows
- When ensuring reproducibility in ML experiments

## Procedure

### 1. Pipeline Framework Setup
Create a modular pipeline framework.

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List
import logging
from datetime import datetime

class PipelineStep(ABC):
    """Abstract base class for pipeline steps."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"Pipeline.{name}")
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the pipeline step."""
        pass
    
    def __call__(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute with logging."""
        self.logger.info(f"Starting step: {self.name}")
        start_time = datetime.now()
        
        try:
            result = self.execute(context)
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Completed step: {self.name} in {duration:.2f}s")
            return result
        except Exception as e:
            self.logger.error(f"Failed step: {self.name} - {str(e)}")
            raise

class Pipeline:
    """Machine learning pipeline orchestrator."""
    
    def __init__(self, name: str, steps: List[PipelineStep]):
        self.name = name
        self.steps = steps
        self.logger = logging.getLogger(f"Pipeline.{name}")
        self.context = {}
    
    def add_step(self, step: PipelineStep):
        """Add a step to the pipeline."""
        self.steps.append(step)
    
    def run(self, initial_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run the entire pipeline."""
        self.context = initial_context or {}
        
        self.logger.info(f"Starting pipeline: {self.name}")
        pipeline_start = datetime.now()
        
        try:
            for step in self.steps:
                self.context = step(self.context)
            
            duration = (datetime.now() - pipeline_start).total_seconds()
            self.logger.info(f"Pipeline {self.name} completed in {duration:.2f}s")
            
            return self.context
            
        except Exception as e:
            self.logger.error(f"Pipeline {self.name} failed: {str(e)}")
            raise
```

### 2. Data Ingestion Step
Automated data collection and loading.

```python
import pandas as pd
from sqlalchemy import create_engine
import requests
from io import StringIO

class DataIngestionStep(PipelineStep):
    """Ingest data from various sources."""
    
    def __init__(self, sources: Dict[str, Any]):
        super().__init__("data_ingestion")
        self.sources = sources
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest data from configured sources."""
        data = {}
        
        for source_name, source_config in self.sources.items():
            source_type = source_config.get('type')
            
            if source_type == 'csv':
                data[source_name] = pd.read_csv(source_config['path'])
            
            elif source_type == 'database':
                engine = create_engine(source_config['connection_string'])
                query = source_config['query']
                data[source_name] = pd.read_sql(query, engine)
            
            elif source_type == 'api':
                response = requests.get(source_config['url'])
                response.raise_for_status()
                json_data = response.json()
                data[source_name] = pd.DataFrame(json_data)
            
            elif source_type == 'json':
                data[source_name] = pd.read_json(source_config['path'])
            
            self.logger.info(f"Ingested {len(data[source_name])} rows from {source_name}")
        
        context['raw_data'] = data
        return context
```

### 3. Data Preprocessing Step
Automated data cleaning and feature engineering.

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import numpy as np

class DataPreprocessingStep(PipelineStep):
    """Preprocess and prepare data for training."""
    
    def __init__(self, preprocessing_config: Dict[str, Any]):
        super().__init__("data_preprocessing")
        self.config = preprocessing_config
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess data according to configuration."""
        raw_data = context['raw_data']
        processed_data = {}
        
        for data_name, df in raw_data.items():
            # Handle missing values
            if self.config.get('drop_missing', False):
                df = df.dropna()
            elif self.config.get('fill_missing'):
                df = df.fillna(self.config['fill_missing'])
            
            # Encode categorical variables
            if self.config.get('encode_categorical', False):
                categorical_cols = df.select_dtypes(include=['object']).columns
                for col in categorical_cols:
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))
            
            # Feature scaling
            if self.config.get('scale_features', False):
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                scaler = StandardScaler()
                df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
                
                # Store scaler for later use
                context[f'{data_name}_scaler'] = scaler
            
            processed_data[data_name] = df
            self.logger.info(f"Preprocessed {data_name}: {df.shape}")
        
        context['processed_data'] = processed_data
        return context

class DataSplitStep(PipelineStep):
    """Split data into train, validation, and test sets."""
    
    def __init__(self, target_column: str, test_size: float = 0.2, val_size: float = 0.1):
        super().__init__("data_split")
        self.target_column = target_column
        self.test_size = test_size
        self.val_size = val_size
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Split data for training."""
        processed_data = context['processed_data']
        
        for data_name, df in processed_data.items():
            if self.target_column not in df.columns:
                self.logger.warning(f"Target column {self.target_column} not in {data_name}")
                continue
            
            X = df.drop(columns=[self.target_column])
            y = df[self.target_column]
            
            # First split: separate test set
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=self.test_size, random_state=42
            )
            
            # Second split: separate validation set from training
            val_ratio = self.val_size / (1 - self.test_size)
            X_train, X_val, y_train, y_val = train_test_split(
                X_train, y_train, test_size=val_ratio, random_state=42
            )
            
            context[f'{data_name}_train'] = (X_train, y_train)
            context[f'{data_name}_val'] = (X_val, y_val)
            context[f'{data_name}_test'] = (X_test, y_test)
            
            self.logger.info(f"Split {data_name}: train={len(X_train)}, val={len(X_val)}, test={len(X_test)}")
        
        return context
```

### 4. Model Training Step
Automated model training with hyperparameter tuning.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import joblib

class ModelTrainingStep(PipelineStep):
    """Train machine learning models."""
    
    def __init__(self, model_type: str, hyperparameters: Dict[str, Any] = None):
        super().__init__("model_training")
        self.model_type = model_type
        self.hyperparameters = hyperparameters or {}
    
    def _get_model(self):
        """Get model instance based on type."""
        models = {
            'random_forest': RandomForestClassifier,
            'logistic_regression': LogisticRegression
        }
        
        if self.model_type not in models:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        return models[self.model_type](**self.hyperparameters)
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Train the model."""
        # Find training data
        train_key = None
        for key in context.keys():
            if key.endswith('_train'):
                train_key = key
                break
        
        if not train_key:
            raise ValueError("No training data found in context")
        
        X_train, y_train = context[train_key]
        
        # Get validation data if available
        val_key = train_key.replace('_train', '_val')
        X_val = y_val = None
        if val_key in context:
            X_val, y_val = context[val_key]
        
        # Create and train model
        model = self._get_model()
        
        self.logger.info(f"Training {self.model_type} model...")
        model.fit(X_train, y_train)
        
        # Evaluate on validation set
        if X_val is not None:
            val_score = model.score(X_val, y_val)
            self.logger.info(f"Validation score: {val_score:.4f}")
            context['val_score'] = val_score
        
        # Store model
        context['model'] = model
        context['model_type'] = self.model_type
        
        return context

class HyperparameterTuningStep(PipelineStep):
    """Perform hyperparameter tuning."""
    
    def __init__(self, model_type: str, param_grid: Dict[str, List], cv: int = 5):
        super().__init__("hyperparameter_tuning")
        self.model_type = model_type
        self.param_grid = param_grid
        self.cv = cv
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform grid search for hyperparameters."""
        train_key = None
        for key in context.keys():
            if key.endswith('_train'):
                train_key = key
                break
        
        X_train, y_train = context[train_key]
        
        # Get base model
        if self.model_type == 'random_forest':
            base_model = RandomForestClassifier()
        elif self.model_type == 'logistic_regression':
            base_model = LogisticRegression(max_iter=1000)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Perform grid search
        grid_search = GridSearchCV(
            base_model, 
            self.param_grid, 
            cv=self.cv, 
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        self.logger.info("Starting hyperparameter tuning...")
        grid_search.fit(X_train, y_train)
        
        # Store results
        context['model'] = grid_search.best_estimator_
        context['best_params'] = grid_search.best_params_
        context['best_score'] = grid_search.best_score_
        
        self.logger.info(f"Best parameters: {grid_search.best_params_}")
        self.logger.info(f"Best cross-validation score: {grid_search.best_score_:.4f}")
        
        return context
```

### 5. Model Evaluation Step
Comprehensive model evaluation and reporting.

```python
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

class ModelEvaluationStep(PipelineStep):
    """Evaluate trained models."""
    
    def __init__(self, save_plots: bool = True, output_dir: str = './output'):
        super().__init__("model_evaluation")
        self.save_plots = save_plots
        self.output_dir = output_dir
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate model on test set."""
        model = context.get('model')
        if not model:
            raise ValueError("No model found in context")
        
        # Find test data
        test_key = None
        for key in context.keys():
            if key.endswith('_test'):
                test_key = key
                break
        
        if not test_key:
            raise ValueError("No test data found in context")
        
        X_test, y_test = context[test_key]
        
        # Make predictions
        y_pred = model.predict(X_test)
        test_score = model.score(X_test, y_test)
        
        # Calculate metrics
        report = classification_report(y_test, y_pred, output_dict=True)
        conf_matrix = confusion_matrix(y_test, y_pred)
        
        # Store results
        context['test_score'] = test_score
        context['classification_report'] = report
        context['confusion_matrix'] = conf_matrix
        
        self.logger.info(f"Test score: {test_score:.4f}")
        
        # Generate plots
        if self.save_plots:
            self._save_confusion_matrix(conf_matrix, context.get('model_type', 'model'))
            self._save_classification_report(report, context.get('model_type', 'model'))
        
        return context
    
    def _save_confusion_matrix(self, conf_matrix, model_name):
        """Save confusion matrix plot."""
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(f'{self.output_dir}/{model_name}_confusion_matrix.png')
        plt.close()
    
    def _save_classification_report(self, report, model_name):
        """Save classification report."""
        with open(f'{self.output_dir}/{model_name}_report.txt', 'w') as f:
            f.write(f"Classification Report - {model_name}\n")
            f.write("=" * 50 + "\n\n")
            
            for class_name, metrics in report.items():
                if isinstance(metrics, dict):
                    f.write(f"Class: {class_name}\n")
                    for metric, value in metrics.items():
                        f.write(f"  {metric}: {value:.4f}\n")
                    f.write("\n")
```

### 6. Model Deployment Step
Automated model deployment and versioning.

```python
import hashlib
import json
from datetime import datetime

class ModelDeploymentStep(PipelineStep):
    """Deploy trained models."""
    
    def __init__(self, deployment_config: Dict[str, Any]):
        super().__init__("model_deployment")
        self.config = deployment_config
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Deploy model to production."""
        model = context.get('model')
        if not model:
            raise ValueError("No model found in context")
        
        # Generate model version
        model_version = self._generate_version(context)
        
        # Save model
        model_path = f"{self.config['model_dir']}/model_{model_version}.joblib"
        joblib.dump(model, model_path)
        
        # Save metadata
        metadata = {
            'version': model_version,
            'model_type': context.get('model_type', 'unknown'),
            'test_score': context.get('test_score', 0),
            'best_params': context.get('best_params', {}),
            'timestamp': datetime.now().isoformat(),
            'model_path': model_path
        }
        
        metadata_path = f"{self.config['model_dir']}/model_{model_version}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update model registry
        self._update_model_registry(metadata)
        
        context['deployed_model'] = metadata
        self.logger.info(f"Model deployed with version: {model_version}")
        
        return context
    
    def _generate_version(self, context: Dict[str, Any]) -> str:
        """Generate unique model version."""
        data_string = f"{context.get('model_type')}{context.get('test_score')}{datetime.now().timestamp()}"
        return hashlib.md5(data_string.encode()).hexdigest()[:8]
    
    def _update_model_registry(self, metadata: Dict[str, Any]):
        """Update model registry with new deployment."""
        registry_path = f"{self.config['model_dir']}/model_registry.json"
        
        # Load existing registry
        try:
            with open(registry_path, 'r') as f:
                registry = json.load(f)
        except FileNotFoundError:
            registry = {'models': [], 'current': None}
        
        # Add new model
        registry['models'].append(metadata)
        registry['current'] = metadata['version']
        
        # Save updated registry
        with open(registry_path, 'w') as f:
            json.dump(registry, f, indent=2)
```

### 7. Complete Pipeline Example
Assemble and run the complete pipeline.

```python
def create_ml_pipeline() -> Pipeline:
    """Create a complete ML pipeline."""
    
    # Define configuration
    sources = {
        'training_data': {
            'type': 'csv',
            'path': './data/training_data.csv'
        }
    }
    
    preprocessing_config = {
        'drop_missing': True,
        'encode_categorical': True,
        'scale_features': True
    }
    
    deployment_config = {
        'model_dir': './models'
    }
    
    # Create pipeline steps
    steps = [
        DataIngestionStep(sources),
        DataPreprocessingStep(preprocessing_config),
        DataSplitStep(target_column='target', test_size=0.2, val_size=0.1),
        HyperparameterTuningStep(
            model_type='random_forest',
            param_grid={
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15],
                'min_samples_split': [2, 5, 10]
            },
            cv=5
        ),
        ModelEvaluationStep(save_plots=True, output_dir='./output'),
        ModelDeploymentStep(deployment_config)
    ]
    
    return Pipeline(name="ml_training_pipeline", steps=steps)

# Usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run pipeline
    pipeline = create_ml_pipeline()
    result = pipeline.run()
    
    print("Pipeline completed successfully!")
    print(f"Test score: {result.get('test_score', 'N/A')}")
```

## Constraints
- **Data Quality**: Garbage in, garbage out - ensure data quality
- **Pipeline Complexity**: Balance between automation and flexibility
- **Resource Management**: Monitor computational resources during training
- **Version Control**: Track all pipeline steps and configurations
- **Error Handling**: Implement robust error handling and recovery
- **Scalability**: Design for data and computational scaling

## Expected Output
Automated, reproducible ML pipelines that handle data ingestion, preprocessing, training, evaluation, and deployment with proper monitoring and version control.
