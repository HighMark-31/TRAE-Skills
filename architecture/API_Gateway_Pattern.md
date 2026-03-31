# Skill: API Gateway Pattern

## Purpose
To provide a single entry point for microservices by implementing a centralized API gateway that handles routing, authentication, rate limiting, and cross-cutting concerns.

## When to Use
- When building microservices architectures
- When you need a single entry point for multiple services
- When implementing cross-cutting concerns like auth, logging, rate limiting
- When aggregating responses from multiple services

## Procedure

### 1. Basic API Gateway Setup
Implement a basic API gateway with routing.

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from httpx import AsyncClient
import logging
from typing import Dict, Any
import asyncio

class APIGateway:
    """API Gateway for microservices."""
    
    def __init__(self):
        self.app = FastAPI(title="API Gateway")
        self.services: Dict[str, str] = {}
        self.client = AsyncClient()
        self.logger = logging.getLogger("APIGateway")
        
        # Setup middleware
        self._setup_middleware()
        
        # Setup routes
        self._setup_routes()
    
    def _setup_middleware(self):
        """Setup gateway middleware."""
        @self.app.middleware("http")
        async def log_requests(request: Request, call_next):
            start_time = asyncio.get_event_loop().time()
            
            # Log request
            self.logger.info(f"Incoming request: {request.method} {request.url.path}")
            
            # Process request
            response = await call_next(request)
            
            # Log response
            process_time = asyncio.get_event_loop().time() - start_time
            self.logger.info(f"Request completed in {process_time:.3f}s")
            
            response.headers["X-Process-Time"] = str(process_time)
            return response
    
    def _setup_routes(self):
        """Setup gateway routes."""
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "gateway": "API Gateway v1.0"}
        
        @self.app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
        async def proxy_request(service: str, path: str, request: Request):
            """Proxy request to appropriate service."""
            if service not in self.services:
                raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
            
            service_url = self.services[service]
            target_url = f"{service_url}/{path}"
            
            # Forward request
            body = await request.body()
            headers = dict(request.headers)
            
            try:
                response = await self.client.request(
                    method=request.method,
                    url=target_url,
                    headers=headers,
                    content=body,
                    timeout=30.0
                )
                
                return JSONResponse(
                    content=response.json(),
                    status_code=response.status_code,
                    headers=dict(response.headers)
                )
            
            except Exception as e:
                self.logger.error(f"Error proxying request: {str(e)}")
                raise HTTPException(status_code=503, detail="Service unavailable")
    
    def register_service(self, name: str, url: str):
        """Register a microservice."""
        self.services[name] = url
        self.logger.info(f"Registered service: {name} -> {url}")
    
    def get_app(self):
        """Get FastAPI application."""
        return self.app

# Usage
gateway = APIGateway()

# Register services
gateway.register_service("users", "http://localhost:8001")
gateway.register_service("products", "http://localhost:8002")
gateway.register_service("orders", "http://localhost:8003")

app = gateway.get_app()
```

### 2. Authentication and Authorization
Implement authentication middleware.

```python
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware for API Gateway."""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_token(self, user_id: str, permissions: list, expires_delta: timedelta = None):
        """Create JWT token."""
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "exp": expire
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    def check_permission(self, required_permission: str):
        """Check if user has required permission."""
        async def permission_checker(credentials: HTTPAuthorizationCredentials = Security(security)):
            payload = self.verify_token(credentials.credentials)
            permissions = payload.get("permissions", [])
            
            if required_permission not in permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission '{required_permission}' required"
                )
            
            return payload
        
        return permission_checker

# Integrate with gateway
auth_middleware = AuthMiddleware(secret_key="your-secret-key")

@gateway.app.get("/protected")
async def protected_endpoint(user_data: Dict = Depends(auth_middleware.check_permission("read:protected"))):
    return {"message": "Access granted", "user": user_data["user_id"]}
```

### 3. Rate Limiting
Implement rate limiting for API protection.

```python
from fastapi import Request, HTTPException
from collections import defaultdict
import time
from typing import Dict

class RateLimiter:
    """Rate limiter using sliding window algorithm."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        minute_ago = now - 60
        
        # Remove old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > minute_ago
        ]
        
        # Check if under limit
        if len(self.requests[key]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True

class RateLimitMiddleware:
    """Rate limiting middleware."""
    
    def __init__(self, limiter: RateLimiter):
        self.limiter = limiter
    
    async def __call__(self, request: Request, call_next):
        """Process request with rate limiting."""
        # Use API key or IP address as key
        api_key = request.headers.get("X-API-Key", request.client.host)
        
        if not self.limiter.is_allowed(api_key):
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        return await call_next(request)

# Integrate with gateway
rate_limiter = RateLimiter(requests_per_minute=60)
gateway.app.middleware("http")(RateLimitMiddleware(rate_limiter))
```

### 4. Service Aggregation
Implement response aggregation from multiple services.

```python
class ServiceAggregator:
    """Aggregate responses from multiple services."""
    
    def __init__(self, gateway: APIGateway):
        self.gateway = gateway
    
    async def aggregate_user_data(self, user_id: str) -> Dict[str, Any]:
        """Aggregate user data from multiple services."""
        tasks = [
            self.fetch_user_profile(user_id),
            self.fetch_user_orders(user_id),
            self.fetch_user_recommendations(user_id)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "user_id": user_id,
            "profile": results[0] if not isinstance(results[0], Exception) else None,
            "orders": results[1] if not isinstance(results[1], Exception) else None,
            "recommendations": results[2] if not isinstance(results[2], Exception) else None
        }
    
    async def fetch_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Fetch user profile."""
        service_url = self.gateway.services.get("users")
        if not service_url:
            raise ValueError("Users service not found")
        
        response = await self.gateway.client.get(f"{service_url}/users/{user_id}")
        return response.json()
    
    async def fetch_user_orders(self, user_id: str) -> Dict[str, Any]:
        """Fetch user orders."""
        service_url = self.gateway.services.get("orders")
        if not service_url:
            raise ValueError("Orders service not found")
        
        response = await self.gateway.client.get(f"{service_url}/orders/{user_id}")
        return response.json()
    
    async def fetch_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Fetch user recommendations."""
        service_url = self.gateway.services.get("products")
        if not service_url:
            raise ValueError("Products service not found")
        
        response = await self.gateway.client.get(f"{service_url}/recommendations/{user_id}")
        return response.json()

# Add aggregation endpoint
aggregator = ServiceAggregator(gateway)

@gateway.app.get("/aggregate/user/{user_id}")
async def aggregate_user_endpoint(user_id: str):
    """Aggregate user data."""
    return await aggregator.aggregate_user_data(user_id)
```

### 5. Circuit Breaker Pattern
Implement circuit breaker for fault tolerance.

```python
from enum import Enum
import asyncio

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker for service resilience."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None
    
    def record_success(self):
        """Record successful request."""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
    
    def record_failure(self):
        """Record failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def can_attempt(self) -> bool:
        """Check if request can be attempted."""
        if self.state == CircuitState.CLOSED:
            return True
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        
        return True  # HALF_OPEN state

class CircuitBreakerMiddleware:
    """Circuit breaker middleware."""
    
    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
    
    def get_breaker(self, service_name: str) -> CircuitBreaker:
        """Get or create circuit breaker for service."""
        if service_name not in self.circuit_breakers:
            self.circuit_breakers[service_name] = CircuitBreaker()
        return self.circuit_breakers[service_name]
    
    async def call_with_breaker(self, service_name: str, callable_func, *args, **kwargs):
        """Call service with circuit breaker protection."""
        breaker = self.get_breaker(service_name)
        
        if not breaker.can_attempt():
            raise HTTPException(
                status_code=503,
                detail=f"Service '{service_name}' is temporarily unavailable"
            )
        
        try:
            result = await callable_func(*args, **kwargs)
            breaker.record_success()
            return result
        except Exception as e:
            breaker.record_failure()
            raise e

# Usage
circuit_breaker = CircuitBreakerMiddleware()

@gateway.app.get("/products/{product_id}")
async def get_product(product_id: str):
    """Get product with circuit breaker protection."""
    async def fetch_product():
        service_url = gateway.services.get("products")
        response = await gateway.client.get(f"{service_url}/products/{product_id}")
        return response.json()
    
    return await circuit_breaker.call_with_breaker("products", fetch_product)
```

### 6. Configuration and Service Discovery
Implement service discovery and configuration management.

```python
import consul

class ServiceRegistry:
    """Service registry using Consul."""
    
    def __init__(self, consul_host: str = "localhost", consul_port: int = 8500):
        self.consul = consul.Consul(host=consul_host, port=consul_port)
        self.logger = logging.getLogger("ServiceRegistry")
    
    def register_service(self, service_name: str, service_id: str, address: str, port: int):
        """Register service with Consul."""
        self.consul.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=address,
            port=port,
            check=consul.Check.http(f"http://{address}:{port}/health", interval="10s")
        )
        self.logger.info(f"Registered service: {service_name} ({service_id})")
    
    def deregister_service(self, service_id: str):
        """Deregister service from Consul."""
        self.consul.agent.service.deregister(service_id)
        self.logger.info(f"Deregistered service: {service_id}")
    
    def discover_service(self, service_name: str) -> list:
        """Discover service instances."""
        _, services = self.consul.health.service(service_name, passing=True)
        
        instances = []
        for service in services:
            instance = {
                "id": service["Service"]["ID"],
                "address": service["Service"]["Address"],
                "port": service["Service"]["Port"]
            }
            instances.append(instance)
        
        return instances
    
    def get_service_url(self, service_name: str) -> str:
        """Get service URL (load balanced)."""
        instances = self.discover_service(service_name)
        if not instances:
            raise ValueError(f"No healthy instances found for {service_name}")
        
        # Simple round-robin selection
        instance = instances[0]  # Could implement proper load balancing
        return f"http://{instance['address']}:{instance['port']}"

# Integrate service discovery with gateway
service_registry = ServiceRegistry()

# Auto-discover and register services
async def refresh_services():
    """Refresh service registry."""
    service_names = ["users", "products", "orders"]
    
    for service_name in service_names:
        try:
            service_url = service_registry.get_service_url(service_name)
            gateway.register_service(service_name, service_url)
        except ValueError as e:
            gateway.logger.warning(f"Service {service_name} not available: {str(e)}")

# Schedule periodic refresh
# asyncio.create_task(periodic_refresh())
```

## Constraints
- **Single Point of Failure**: API gateway can become a bottleneck - implement high availability
- **Performance**: Gateway adds latency - optimize routing and caching
- **Complexity**: Gateway logic can become complex - keep it focused
- **Scalability**: Design gateway to scale horizontally
- **Security**: Implement proper authentication and authorization
- **Monitoring**: Monitor gateway performance and service health

## Expected Output
A robust API gateway that provides single entry point, authentication, rate limiting, service aggregation, and fault tolerance for microservices architecture.
