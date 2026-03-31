# Skill: AI Model Serving

## Purpose
To deploy and serve machine learning models in production environments with proper scaling, monitoring, and API integration.

## When to Use
- When deploying ML models to production
- When building ML-powered APIs and services
- When implementing real-time inference systems
- When scaling ML services for production traffic

## Procedure

### 1. Model Server Setup
Create a production-ready model server.

```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import joblib
import logging
import time
from datetime import datetime
import asyncio
from prometheus_client import Counter, Histogram, generate_latest
import numpy as np

# Define request/response models
class PredictionRequest(BaseModel):
    model_name: str = Field(..., description="Name of the model to use")
    model_version: str = Field(default="latest", description="Version of the model")
    input_data: Dict[str, Any] = Field(..., description="Input data for prediction")
    preprocessing: Optional[Dict[str, Any]] = Field(default=None, description="Preprocessing options")
    postprocessing: Optional[Dict[str, Any]] = Field(default=None, description="Postprocessing options")

class PredictionResponse(BaseModel):
    prediction: Any
    model_name: str
    model_version: str
    prediction_time: float
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    models_loaded: List[str]
    uptime_seconds: float
    version: str

# Create FastAPI app
app = FastAPI(
    title="ML Model Serving API",
    description="Production ML model inference server",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
prediction_counter = Counter('predictions_total', 'Total predictions', ['model_name', 'status'])
prediction_duration = Histogram('prediction_duration_seconds', 'Prediction duration', ['model_name'])

class ModelServer:
    """Production model server."""
    
    def __init__(self, model_registry_path: str = "./models"):
        self.model_registry_path = model_registry_path
        self.loaded_models = {}
        self.model_metadata = {}
        self.start_time = time.time()
        self.logger = logging.getLogger("ModelServer")
        
        # Load model registry
        self._load_model_registry()
    
    def _load_model_registry(self):
        """Load model registry."""
        import json
        registry_path = f"{self.model_registry_path}/model_registry.json"
        try:
            with open(registry_path, 'r') as f:
                self.model_registry = json.load(f)
        except FileNotFoundError:
            self.model_registry = {"models": [], "current": None}
            self.logger.warning("Model registry not found, starting with empty registry")
    
    def load_model(self, model_name: str, version: str = "latest"):
        """Load model into memory."""
        model_key = f"{model_name}_{version}"
        
        if model_key in self.loaded_models:
            return self.loaded_models[model_key]
        
        # Find model in registry
        model_info = None
        for model in self.model_registry["models"]:
            if model["model_type"] == model_name:
                if version == "latest" or model["version"] == version:
                    model_info = model
                    break
        
        if not model_info:
            raise ValueError(f"Model {model_name} version {version} not found")
        
        # Load model from disk
        model_path = model_info["model_path"]
        try:
            model = joblib.load(model_path)
            self.loaded_models[model_key] = model
            self.model_metadata[model_key] = model_info
            self.logger.info(f"Loaded model: {model_key}")
            return model
        except Exception as e:
            self.logger.error(f"Failed to load model {model_key}: {str(e)}")
            raise
    
    def unload_model(self, model_name: str, version: str = "latest"):
        """Unload model from memory."""
        model_key = f"{model_name}_{version}"
        if model_key in self.loaded_models:
            del self.loaded_models[model_key]
            del self.model_metadata[model_key]
            self.logger.info(f"Unloaded model: {model_key}")
    
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Make prediction."""
        start_time = time.time()
        model_key = f"{request.model_name}_{request.model_version}"
        
        try:
            # Load model if not in memory
            model = self.load_model(request.model_name, request.model_version)
            
            # Preprocess input
            processed_input = self._preprocess_input(request.input_data, request.preprocessing)
            
            # Make prediction
            prediction = model.predict([processed_input])[0] if hasattr(model, 'predict') else model(processed_input)
            
            # Postprocess prediction
            final_prediction = self._postprocess_prediction(prediction, request.postprocessing)
            
            prediction_time = time.time() - start_time
            
            # Record metrics
            prediction_counter.labels(model_name=request.model_name, status='success').inc()
            prediction_duration.labels(model_name=request.model_name).observe(prediction_time)
            
            return PredictionResponse(
                prediction=final_prediction,
                model_name=request.model_name,
                model_version=request.model_version,
                prediction_time=prediction_time,
                timestamp=datetime.now().isoformat(),
                metadata=self.model_metadata.get(model_key)
            )
            
        except Exception as e:
            prediction_counter.labels(model_name=request.model_name, status='error').inc()
            self.logger.error(f"Prediction failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    def _preprocess_input(self, input_data: Dict[str, Any], preprocessing: Optional[Dict[str, Any]]) -> Any:
        """Preprocess input data."""
        # Implement preprocessing logic based on model requirements
        # This is a placeholder - customize based on your model
        return input_data
    
    def _postprocess_prediction(self, prediction: Any, postprocessing: Optional[Dict[str, Any]]) -> Any:
        """Postprocess prediction."""
        # Implement postprocessing logic
        return prediction
    
    def get_health(self) -> HealthResponse:
        """Get server health status."""
        return HealthResponse(
            status="healthy",
            models_loaded=list(self.loaded_models.keys()),
            uptime_seconds=time.time() - self.start_time,
            version="1.0.0"
        )

# Create model server instance
model_server = ModelServer()

# API endpoints
@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make prediction."""
    return await model_server.predict(request)

@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return model_server.get_health()

@app.get("/models")
async def list_models():
    """List available models."""
    return {"models": model_server.model_registry["models"]}

@app.post("/models/{model_name}/load")
async def load_model_endpoint(model_name: str, version: str = "latest"):
    """Load model endpoint."""
    try:
        model_server.load_model(model_name, version)
        return {"status": "success", "message": f"Model {model_name} version {version} loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/models/{model_name}/unload")
async def unload_model_endpoint(model_name: str, version: str = "latest"):
    """Unload model endpoint."""
    model_server.unload_model(model_name, version)
    return {"status": "success", "message": f"Model {model_name} version {version} unloaded"}

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest()
```

### 2. Batch Prediction Service
Handle batch prediction requests efficiently.

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import List

class BatchPredictionService:
    """Service for batch predictions."""
    
    def __init__(self, model_server: ModelServer, max_workers: int = 4):
        self.model_server = model_server
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.logger = logging.getLogger("BatchPredictionService")
    
    async def predict_batch(self, requests: List[PredictionRequest]) -> List[PredictionResponse]:
        """Process multiple prediction requests in parallel."""
        loop = asyncio.get_event_loop()
        
        # Create tasks for parallel processing
        tasks = [
            loop.run_in_executor(
                self.executor,
                self._predict_sync,
                request
            )
            for request in requests
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Batch prediction failed for request {i}: {str(result)}")
                # Create error response
                responses.append(PredictionResponse(
                    prediction=None,
                    model_name=requests[i].model_name,
                    model_version=requests[i].model_version,
                    prediction_time=0,
                    timestamp=datetime.now().isoformat(),
                    metadata={"error": str(result)}
                ))
            else:
                responses.append(result)
        
        return responses
    
    def _predict_sync(self, request: PredictionRequest) -> PredictionResponse:
        """Synchronous prediction for thread pool."""
        return asyncio.run(self.model_server.predict(request))
    
    async def predict_streaming(self, request_generator):
        """Stream predictions as they complete."""
        loop = asyncio.get_event_loop()
        
        async for request in request_generator:
            prediction = await self.model_server.predict(request)
            yield prediction
```

### 3. Model Caching and Optimization
Implement model caching and prediction optimization.

```python
from functools import lru_cache
import hashlib
import json

class CachedModelServer(ModelServer):
    """Model server with caching capabilities."""
    
    def __init__(self, *args, cache_size: int = 1000, cache_ttl: int = 3600, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_size = cache_size
        self.cache_ttl = cache_ttl
        self.cache = {}
        self.cache_timestamps = {}
        self.logger = logging.getLogger("CachedModelServer")
    
    def _generate_cache_key(self, model_name: str, model_version: str, input_data: Dict[str, Any]) -> str:
        """Generate cache key."""
        cache_input = f"{model_name}_{model_version}_{json.dumps(input_data, sort_keys=True)}"
        return hashlib.sha256(cache_input.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get prediction from cache."""
        if cache_key in self.cache:
            cache_time = self.cache_timestamps[cache_key]
            if time.time() - cache_time < self.cache_ttl:
                self.logger.debug(f"Cache hit for key: {cache_key}")
                return self.cache[cache_key]
            else:
                # Cache expired
                del self.cache[cache_key]
                del self.cache_timestamps[cache_key]
        
        return None
    
    def _set_cache(self, cache_key: str, prediction: Any):
        """Set prediction in cache."""
        # Implement simple LRU cache
        if len(self.cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = min(self.cache_timestamps.keys(), key=lambda k: self.cache_timestamps[k])
            del self.cache[oldest_key]
            del self.cache_timestamps[oldest_key]
        
        self.cache[cache_key] = prediction
        self.cache_timestamps[cache_key] = time.time()
    
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Predict with caching."""
        cache_key = self._generate_cache_key(request.model_name, request.model_version, request.input_data)
        
        # Check cache
        cached_prediction = self._get_from_cache(cache_key)
        if cached_prediction is not None:
            return cached_prediction
        
        # Make prediction
        prediction = await super().predict(request)
        
        # Cache result
        self._set_cache(cache_key, prediction)
        
        return prediction
    
    def clear_cache(self):
        """Clear prediction cache."""
        self.cache.clear()
        self.cache_timestamps.clear()
        self.logger.info("Cache cleared")
```

### 4. Model Version Management
Manage multiple model versions and A/B testing.

```python
class ModelVersionManager:
    """Manage model versions and A/B testing."""
    
    def __init__(self, model_server: ModelServer):
        self.model_server = model_server
        self.traffic_rules = {}
        self.logger = logging.getLogger("ModelVersionManager")
    
    def set_traffic_split(self, model_name: str, version_rules: Dict[str, float]):
        """Set traffic split for model versions."""
        total_percentage = sum(version_rules.values())
        if abs(total_percentage - 1.0) > 0.01:
            raise ValueError(f"Traffic split must sum to 1.0, got {total_percentage}")
        
        self.traffic_rules[model_name] = version_rules
        self.logger.info(f"Set traffic split for {model_name}: {version_rules}")
    
    def get_model_for_request(self, model_name: str, request_id: str) -> str:
        """Determine which model version to use for request."""
        if model_name not in self.traffic_rules:
            return "latest"  # Default to latest
        
        version_rules = self.traffic_rules[model_name]
        
        # Use request_id hash for consistent routing
        hash_value = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
        random_value = (hash_value % 100) / 100.0
        
        cumulative = 0.0
        for version, percentage in version_rules.items():
            cumulative += percentage
            if random_value <= cumulative:
                return version
        
        return list(version_rules.keys())[-1]  # Fallback to last version
    
    async def predict_with_routing(self, request: PredictionRequest, request_id: str) -> PredictionResponse:
        """Predict with intelligent version routing."""
        # Determine version
        version = self.get_model_for_request(request.model_name, request_id)
        request.model_version = version
        
        # Make prediction
        prediction = await self.model_server.predict(request)
        prediction.metadata = prediction.metadata or {}
        prediction.metadata["routed_version"] = version
        prediction.metadata["request_id"] = request_id
        
        return prediction

class ABTestFramework:
    """A/B testing framework for models."""
    
    def __init__(self, version_manager: ModelVersionManager):
        self.version_manager = version_manager
        self.metrics = defaultdict(lambda: {"predictions": 0, "errors": 0, "latencies": []})
    
    async def predict_with_tracking(self, request: PredictionRequest, request_id: str) -> PredictionResponse:
        """Predict with A/B test tracking."""
        prediction = await self.version_manager.predict_with_routing(request, request_id)
        
        # Track metrics
        version = prediction.metadata.get("routed_version", "unknown")
        self.metrics[version]["predictions"] += 1
        self.metrics[version]["latencies"].append(prediction.prediction_time)
        
        return prediction
    
    def get_ab_test_results(self) -> Dict[str, Any]:
        """Get A/B test results."""
        results = {}
        for version, data in self.metrics.items():
            latencies = data["latencies"]
            results[version] = {
                "predictions": data["predictions"],
                "errors": data["errors"],
                "avg_latency": sum(latencies) / len(latencies) if latencies else 0,
                "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)] if len(latencies) > 20 else 0,
                "error_rate": data["errors"] / data["predictions"] if data["predictions"] > 0 else 0
            }
        
        return results
```

### 5. Monitoring and Observability
Implement comprehensive monitoring for model serving.

```python
from prometheus_client import Counter, Histogram, Gauge, Info
import logging
from logging.handlers import RotatingFileHandler

class ModelServingMonitor:
    """Monitor model serving metrics."""
    
    def __init__(self):
        # Prometheus metrics
        self.request_counter = Counter('model_requests_total', 'Total model requests', ['model_name', 'version', 'status'])
        self.request_duration = Histogram('model_request_duration_seconds', 'Model request duration', ['model_name', 'version'])
        self.model_load_counter = Counter('model_loads_total', 'Total model loads', ['model_name', 'version', 'status'])
        self.active_models = Gauge('active_models', 'Number of loaded models')
        self.memory_usage = Gauge('memory_usage_bytes', 'Memory usage')
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percent')
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup detailed logging."""
        logger = logging.getLogger("ModelServing")
        logger.setLevel(logging.INFO)
        
        # Rotating file handler
        handler = RotatingFileHandler('model_serving.log', maxBytes=10*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
```

## Constraints
- **Performance**: Model loading and prediction should be optimized for low latency
- **Scalability**: Design for horizontal scaling and load balancing
- **Monitoring**: Implement comprehensive monitoring and alerting
- **Error Handling**: Robust error handling and graceful degradation
- **Security**: Implement authentication, authorization, and input validation
- **Resource Management**: Monitor and manage memory, CPU, and GPU usage

## Expected Output
Production-ready model serving infrastructure with proper API design, monitoring, caching, and scalability for reliable ML model deployment.