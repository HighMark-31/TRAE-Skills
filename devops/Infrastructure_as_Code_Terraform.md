# Skill: Infrastructure as Code (Terraform)

## Purpose
To provision and manage infrastructure (servers, databases, networks) using declarative configuration files, ensuring reproducibility and version control.

## When to Use
- Setting up a new cloud environment (AWS, Azure, GCP).
- Managing changes to existing infrastructure.
- Preventing configuration drift.

## Procedure
1.  **Install Terraform**: Ensure CLI is available.
2.  **Define Provider**: Create `main.tf` and configure the provider (e.g., `provider "aws" { region = "us-east-1" }`).
3.  **Define Resources**: Declare resources like `resource "aws_instance" "web" { ... }`.
4.  **Initialize**: Run `terraform init` to download provider plugins.
5.  **Plan**: Run `terraform plan` to preview changes. Verify strictly.
6.  **Apply**: Run `terraform apply` to execute changes.
7.  **State Management**: Store `terraform.tfstate` in a remote backend (S3 + DynamoDB for locking) to allow team collaboration.

## Constraints
- Never commit `.tfstate` files to Git (contains secrets).
- Use `terraform validate` and `tflint` before applying.
- Lock state to prevent concurrent modifications.

## Expected Output
A set of `.tf` files that can spin up the entire infrastructure stack automatically.
