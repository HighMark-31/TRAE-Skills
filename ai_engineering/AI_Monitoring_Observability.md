# Skill: AI Monitoring and Observability

## Purpose
To implement comprehensive monitoring, logging, and observability for AI systems in production to ensure reliability, performance, and safety.

## When to Use
- When deploying AI models to production
- When monitoring model performance and drift
- When troubleshooting AI system issues
- When ensuring SLA compliance and user satisfaction

## Procedure

### 1. Model Performance Monitoring
Track key performance metrics in real-time.

```python
import time
import logging
from datetime import datetime
from collections import defaultdict
import json

class ModelPerformanceMonitor:
    def __init__(self, model_name):
        self.model_name = model_name
        self.metrics = defaultdict(list)
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Setup logging configuration."""
        logger = logging.getLogger(f"{self.model_name}_monitor")
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def log_prediction(self, input_data, prediction, latency_ms, metadata=None):
        """Log individual prediction with metadata."""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            'timestamp': timestamp,
            'model': self.model_name,
            'input_hash': hash(str(input_data)),
            'prediction': str(prediction),
            'latency_ms': latency_ms,
            'metadata': metadata or {}
        }
        
        self.metrics['predictions'].append(log_entry)
        self.logger.info(f"Prediction logged: {latency_ms}ms")
        
        return log_entry
    
    def log_feedback(self, prediction_id, feedback):
        """Log user feedback on predictions."""
        feedback_entry = {
            'prediction_id': prediction_id,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        
        self.metrics['feedback'].append(feedback_entry)
        self.logger.info(f"Feedback received: {feedback}")
        
        return feedback_entry
    
    def calculate_metrics(self, time_window_minutes=5):
        """Calculate performance metrics over time window."""
        cutoff_time = datetime.now().timestamp() - (time_window_minutes * 60)
        
        recent_predictions = [
            p for p in self.metrics['predictions']
            if datetime.fromisoformat(p['timestamp']).timestamp() > cutoff_time
        ]
        
        if not recent_predictions:
            return {'error': 'No recent predictions'}
        
        latencies = [p['latency_ms'] for p in recent_predictions]
        
        metrics = {
            'total_predictions': len(recent_predictions),
            'avg_latency_ms': sum(latencies) / len(latencies),
            'p50_latency': sorted(latencies)[len(latencies) // 2],
            'p95_latency': sorted(latencies)[int(len(latencies) * 0.95)],
            'p99_latency': sorted(latencies)[int(len(latencies) * 0.99)],
            'max_latency': max(latencies),
            'min_latency': min(latencies)
        }
        
        # Calculate accuracy if feedback available
        if self.metrics['feedback']:
            recent_feedback = [
                f for f in self.metrics['feedback']
                if datetime.fromisoformat(f['timestamp']).timestamp() > cutoff_time
            ]
            
            if recent_feedback:
                correct = sum(1 for f in recent_feedback if f['feedback'] == 'correct')
                metrics['accuracy'] = correct / len(recent_feedback)
        
        return metrics
    
    def check_sla_compliance(self, sla_max_latency_ms=500):
        """Check if SLA requirements are met."""
        metrics = self.calculate_metrics()
        
        if 'error' in metrics:
            return {'status': 'error', 'message': metrics['error']}
        
        compliance = {
            'sla_max_latency_ms': sla_max_latency_ms,
            'p95_latency': metrics['p95_latency'],
            'sla_met': metrics['p95_latency'] <= sla_max_latency_ms,
            'avg_latency': metrics['avg_latency_ms']
        }
        
        if not compliance['sla_met']:
            self.logger.warning(f"SLA violation: P95 latency {metrics['p95_latency']:.2f}ms exceeds {sla_max_latency_ms}ms")
        
        return compliance

# Usage
# monitor = ModelPerformanceMonitor("sentiment_model")
# 
# start_time = time.time()
# prediction = model.predict("This is great!")
# latency = (time.time() - start_time) * 1000
# 
# monitor.log_prediction("This is great!", prediction, latency)
# 
# metrics = monitor.calculate_metrics()
# sla_status = monitor.check_sla_compliance(sla_max_latency_ms=500)
```

### 2. Data Drift Detection
Monitor and detect data distribution changes.

```python
import numpy as np
from scipy import stats
from typing import Dict, List

class DataDriftDetector:
    def __init__(self, reference_data, significance_level=0.05):
        """
        Initialize with reference (training) data.
        
        Args:
            reference_data: Dictionary of feature names to arrays
            significance_level: Threshold for detecting drift
        """
        self.reference_data = reference_data
        self.significance_level = significance_level
        self.drift_history = []
    
    def calculate_kl_divergence(self, p, q):
        """Calculate Kullback-Leibler divergence."""
        # Add small epsilon to avoid division by zero
        epsilon = 1e-10
        p = p + epsilon
        q = q + epsilon
        
        return np.sum(p * np.log(p / q))
    
    def detect_drift(self, new_data):
        """Detect drift in new data compared to reference."""
        drift_report = {
            'timestamp': datetime.now().isoformat(),
            'features': {},
            'overall_drift_detected': False
        }
        
        for feature in self.reference_data.keys():
            if feature not in new_data:
                continue
            
            ref_values = self.reference_data[feature]
            new_values = new_data[feature]
            
            # Kolmogorov-Smirnov test
            ks_statistic, ks_pvalue = stats.ks_2samp(ref_values, new_values)
            
            # Calculate distribution statistics
            ref_mean, ref_std = np.mean(ref_values), np.std(ref_values)
            new_mean, new_std = np.mean(new_values), np.std(new_values)
            
            # Feature drift detected if p-value < significance level
            feature_drift = ks_pvalue < self.significance_level
            
            feature_report = {
                'drift_detected': feature_drift,
                'ks_statistic': ks_statistic,
                'ks_pvalue': ks_pvalue,
                'reference_mean': ref_mean,
                'new_mean': new_mean,
                'reference_std': ref_std,
                'new_std': new_std,
                'mean_shift': abs(new_mean - ref_mean)
            }
            
            drift_report['features'][feature] = feature_report
            
            if feature_drift:
                drift_report['overall_drift_detected'] = True
        
        self.drift_history.append(drift_report)
        return drift_report
    
    def get_drift_summary(self, window_size=10):
        """Get summary of recent drift detections."""
        recent_drift = self.drift_history[-window_size:]
        
        if not recent_drift:
            return {'status': 'No drift history available'}
        
        summary = {
            'total_checks': len(recent_drift),
            'drift_detected_count': sum(1 for r in recent_drift if r['overall_drift_detected']),
            'drift_rate': sum(1 for r in recent_drift if r['overall_drift_detected']) / len(recent_drift),
            'most_drifted_features': self._get_most_drifted_features(recent_drift)
        }
        
        return summary
    
    def _get_most_drifted_features(self, drift_reports):
        """Identify features with most frequent drift."""
        feature_drift_counts = defaultdict(int)
        
        for report in drift_reports:
            for feature, feature_report in report['features'].items():
                if feature_report['drift_detected']:
                    feature_drift_counts[feature] += 1
        
        return sorted(feature_drift_counts.items(), key=lambda x: x[1], reverse=True)

# Usage
# reference_data = {
#     'age': np.random.normal(35, 10, 1000),
#     'income': np.random.normal(50000, 15000, 1000)
# }
# 
# detector = DataDriftDetector(reference_data)
# 
# # Simulate new data with drift
# new_data = {
#     'age': np.random.normal(45, 10, 100),  # Drifted age
#     'income': np.random.normal(52000, 15000, 100)  # Similar income
# }
# 
# drift_report = detector.detect_drift(new_data)
# print(drift_report)
```

### 3. Error Analysis and Tracking
Track and analyze model errors.

```python
class ErrorAnalyzer:
    def __init__(self):
        self.errors = []
        self.error_categories = defaultdict(int)
    
    def log_error(self, input_data, prediction, ground_truth, error_type, metadata=None):
        """Log model error with details."""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'input_data': str(input_data),
            'prediction': prediction,
            'ground_truth': ground_truth,
            'error_type': error_type,
            'metadata': metadata or {}
        }
        
        self.errors.append(error_entry)
        self.error_categories[error_type] += 1
        
        return error_entry
    
    def analyze_error_patterns(self):
        """Analyze patterns in errors."""
        if not self.errors:
            return {'status': 'No errors to analyze'}
        
        analysis = {
            'total_errors': len(self.errors),
            'error_types': dict(self.error_categories),
            'error_rate_by_type': {},
            'recent_errors': self.errors[-10:]  # Last 10 errors
        }
        
        # Calculate error rates
        total_errors = len(self.errors)
        for error_type, count in self.error_categories.items():
            analysis['error_rate_by_type'][error_type] = count / total_errors
        
        return analysis
    
    def identify_error_clusters(self, feature_extractor=None):
        """Identify clusters of similar errors."""
        if not self.errors:
            return {'status': 'No errors to cluster'}
        
        # Extract error features
        error_features = []
        for error in self.errors:
            if feature_extractor:
                features = feature_extractor(error['input_data'])
            else:
                features = hash(error['input_data'])
            
            error_features.append({
                'error': error,
                'features': features
            })
        
        # Simple clustering by error type
        clusters = defaultdict(list)
        for item in error_features:
            error_type = item['error']['error_type']
            clusters[error_type].append(item['error'])
        
        return {
            'num_clusters': len(clusters),
            'cluster_sizes': {k: len(v) for k, v in clusters.items()},
            'clusters': dict(clusters)
        }
    
    def generate_error_report(self):
        """Generate comprehensive error report."""
        patterns = self.analyze_error_patterns()
        clusters = self.identify_error_clusters()
        
        report = {
            'summary': {
                'total_errors': patterns['total_errors'],
                'error_types': patterns['error_types']
            },
            'patterns': patterns,
            'clusters': clusters
        }
        
        return report

# Usage
# error_analyzer = ErrorAnalyzer()
# 
# # Log some errors
# error_analyzer.log_error(
#     input_data="Great product!",
#     prediction="negative",
#     ground_truth="positive",
#     error_type="sentiment_misclassification"
# )
# 
# report = error_analyzer.generate_error_report()
```

### 4. System Health Monitoring
Monitor overall AI system health.

```python
import psutil
import GPUtil

class AISystemHealthMonitor:
    def __init__(self):
        self.health_metrics = []
    
    def collect_system_metrics(self):
        """Collect system resource usage."""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_sent': psutil.net_io_counters().bytes_sent,
            'network_recv': psutil.net_io_counters().bytes_recv
        }
        
        # GPU metrics if available
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                metrics['gpu_usage'] = gpus[0].load * 100
                metrics['gpu_memory'] = gpus[0].memoryUtil * 100
        except:
            pass
        
        self.health_metrics.append(metrics)
        return metrics
    
    def check_health_status(self, thresholds=None):
        """Check if system is healthy based on thresholds."""
        if thresholds is None:
            thresholds = {
                'cpu_percent': 80,
                'memory_percent': 85,
                'disk_usage': 90,
                'gpu_usage': 90
            }
        
        latest_metrics = self.collect_system_metrics()
        health_status = {
            'status': 'healthy',
            'alerts': [],
            'metrics': latest_metrics
        }
        
        # Check each metric against threshold
        for metric, threshold in thresholds.items():
            if metric in latest_metrics:
                value = latest_metrics[metric]
                if value > threshold:
                    health_status['status'] = 'warning'
                    health_status['alerts'].append({
                        'metric': metric,
                        'value': value,
                        'threshold': threshold,
                        'message': f'{metric} ({value:.1f}%) exceeds threshold ({threshold}%)'
                    })
        
        return health_status
    
    def generate_health_report(self):
        """Generate system health report."""
        health_status = self.check_health_status()
        
        report = f"""
System Health Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}

Status: {health_status['status'].upper()}

System Metrics:
- CPU Usage: {health_status['metrics']['cpu_percent']:.1f}%
- Memory Usage: {health_status['metrics']['memory_percent']:.1f}%
- Disk Usage: {health_status['metrics']['disk_usage']:.1f}%
"""
        
        if 'gpu_usage' in health_status['metrics']:
            report += f"- GPU Usage: {health_status['metrics']['gpu_usage']:.1f}%\n"
        
        if health_status['alerts']:
            report += "\nAlerts:\n"
            for alert in health_status['alerts']:
                report += f"  ⚠️ {alert['message']}\n"
        else:
            report += "\n✅ All systems operating within normal parameters.\n"
        
        return report

# Usage
# health_monitor = AISystemHealthMonitor()
# health_report = health_monitor.generate_health_report()
# print(health_report)
```

### 5. Integration with Monitoring Platforms
Export metrics to monitoring platforms.

```python
class MonitoringPlatformIntegration:
    def __init__(self, platform='prometheus'):
        self.platform = platform
        self.metrics_buffer = []
    
    def export_to_prometheus(self, metrics):
        """Format metrics for Prometheus."""
        prometheus_metrics = []
        
        for metric_name, value in metrics.items():
            # Convert metric name to Prometheus format
            prom_name = metric_name.lower().replace(' ', '_')
            prometheus_metrics.append(f"{prom_name} {value}")
        
        return '\n'.join(prometheus_metrics)
    
    def export_to_datadog(self, metrics):
        """Format metrics for Datadog."""
        datadog_metrics = []
        
        for metric_name, value in metrics.items():
            metric_data = {
                'metric': f'ai.{metric_name.lower().replace(" ", ".")}',
                'points': [[int(time.time()), value]],
                'type': 'gauge'
            }
            datadog_metrics.append(metric_data)
        
        return datadog_metrics
    
    def send_metrics(self, metrics, api_endpoint):
        """Send metrics to monitoring platform."""
        if self.platform == 'prometheus':
            formatted_metrics = self.export_to_prometheus(metrics)
            # In real implementation, push to Prometheus Pushgateway
            print(f"Sending to Prometheus:\n{formatted_metrics}")
        
        elif self.platform == 'datadog':
            formatted_metrics = self.export_to_datadog(metrics)
            # In real implementation, use Datadog API
            print(f"Sending to Datadog: {formatted_metrics}")
        
        return {'status': 'sent', 'count': len(metrics)}

# Usage
# integration = MonitoringPlatformIntegration('prometheus')
# 
# metrics = {
#     'model_latency_ms': 145.2,
#     'prediction_count': 1000,
#     'error_rate': 0.02
# }
# 
# integration.send_metrics(metrics, 'http://pushgateway:9091')
```

## Constraints
- **Performance Overhead**: Monitoring should not significantly impact system performance
- **Storage Costs**: Extensive logging can generate large amounts of data
- **Privacy**: Ensure sensitive data is not logged or is properly anonymized
- **Real-time Requirements**: Balance between real-time monitoring and batch processing
- **Alert Fatigue**: Configure thresholds to avoid excessive false alarms
- **Data Retention**: Implement proper data retention policies for logs and metrics

## Expected Output
Comprehensive monitoring and observability for AI systems with real-time performance tracking, drift detection, error analysis, and system health monitoring for reliable production deployment.
