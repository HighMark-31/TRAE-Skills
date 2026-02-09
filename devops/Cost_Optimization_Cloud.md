# Skill: Cost Optimization (AWS/Cloud)

## Purpose
To reduce cloud infrastructure costs.

## When to Use
- Spot instances, rightsizing, and budgeting.
- When the specific requirement for Cost Optimization (AWS/Cloud) arises in the project.

## Procedure

### 1. Rightsizing Instances
Analyze CPU/Memory utilization and downsize over-provisioned resources.
- Use **AWS Compute Optimizer** or **Azure Advisor** to find underutilized instances.
- Switch to modern instance families (e.g., AWS Graviton/t4g) for better price-performance.

### 2. Leveraging Spot Instances
Use Spot instances for non-critical, fault-tolerant workloads (CI/CD workers, batch processing).

```hcl
# Terraform example for Spot Instance
resource "aws_instance" "worker" {
  ami           = "ami-12345678"
  instance_type = "c5.large"
  
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.05"
    }
  }
}
```

### 3. Implementing Auto-Scaling
Ensure infrastructure scales down during low-traffic periods (nights/weekends).
- Set `min_size` to the lowest possible for non-prod environments.
- Use **Scheduled Scaling** for predictable traffic patterns.

### 4. Storage Optimization
- **Cleanup**: Delete unattached EBS volumes and old S3 versions.
- **Lifecycle Policies**: Move old data to cheaper storage tiers (e.g., S3 Intelligent-Tiering or Glacier).

```hcl
# S3 Lifecycle Rule
resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket.data.id

  rule {
    id      = "archive_old_logs"
    status  = "Enabled"
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}
```

## Constraints
- **Performance Trade-offs**: Rightsizing too aggressively can lead to performance bottlenecks during peaks.
- **Spot Interruptions**: Always have a fallback strategy for Spot instances (e.g., mixing with On-Demand in an Auto Scaling Group).
- **Data Retention**: Ensure lifecycle policies comply with legal/compliance data retention requirements.

## Expected Output
A measurable reduction in monthly cloud spend (aim for 20-30%) without compromising application stability.
