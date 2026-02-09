# Skill: Infrastructure as Code (Terraform)

## Purpose
To provision and manage infrastructure (servers, databases, networks) using declarative configuration files, ensuring reproducibility and version control.

## When to Use
- Setting up a new cloud environment (AWS, Azure, GCP).
- Managing changes to existing infrastructure.
- Preventing configuration drift.

## Procedure

### 1. Provider and Backend Configuration
Define where Terraform will manage resources and store its state.

```hcl
# main.tf
terraform {
  required_version = ">= 1.5.0"
  
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock-table"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
```

### 2. Resource Definition
Declare your infrastructure components using variables.

```hcl
# vpc.tf
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# variables.tf
variable "project_name" {
  type    = string
  default = "my-app"
}
```

### 3. Modularization
Create reusable modules for standard components.

```hcl
# root.tf
module "database" {
  source       = "./modules/rds"
  db_name      = "production_db"
  instance_class = "db.t3.micro"
}
```

### 4. Lifecycle Workflow
Standard commands to manage infrastructure.

```bash
# 1. Initialize (Downloads providers/modules)
terraform init

# 2. Plan (Shows what will happen)
terraform plan -out=tfplan

# 3. Apply (Executes changes)
terraform apply "tfplan"

# 4. Format/Validate
terraform fmt -recursive
terraform validate
```

## Constraints
- **State Security**: Never commit `.tfstate` to Git. Use remote backends with encryption.
- **Destructive Changes**: Always review `terraform plan` output carefully, especially for "replace" actions on databases.
- **Variables**: Use `terraform.tfvars` or environment variables for sensitive inputs.

## Expected Output
A modular, versioned infrastructure definition that can recreate environments consistently with a single command.
