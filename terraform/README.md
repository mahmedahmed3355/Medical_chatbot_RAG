# Terraform Infrastructure

This directory manages AWS infrastructure for the Medical RAG Chatbot.

## Resources

- Amazon ECR repository
- Image vulnerability scanning on push
- ECR lifecycle policy to retain the latest 10 images

## Usage

Copy the example variables file:

cp terraform.tfvars.example terraform.tfvars

Initialize Terraform:

terraform init

Validate the configuration:

terraform validate

Preview infrastructure changes:

terraform plan

Apply the infrastructure:

terraform apply
