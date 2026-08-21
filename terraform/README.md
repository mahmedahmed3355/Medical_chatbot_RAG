# Terraform Infrastructure

This directory contains the Terraform configuration for the Medical RAG Chatbot infrastructure.

## Architecture

The current infrastructure manages an AWS ECR repository used to store container images for the Medical RAG Chatbot.

The configuration includes:

- AWS provider configuration.
- Configurable deployment region.
- ECR repository for application container images.
- Image scanning on push.
- Lifecycle policy that retains the latest 10 images.
- Standard Terraform resource tags.
- Repository name and URL outputs.

## State Management

The current configuration does not define a remote backend.

Terraform therefore uses the default local state backend when commands that create or modify infrastructure state are executed.

For production or team deployments, configure a remote backend before running terraform apply.

A remote backend should provide:

- Shared state storage.
- State locking.
- Access control.
- Encryption at rest.
- Backup and recovery.

Do not commit terraform.tfstate or terraform.tfstate.backup.

## Initialization

Initialize the Terraform working directory:

    terraform init

For validation without configuring a backend:

    terraform init -backend=false

## Validation

Format and validate the configuration:

    terraform fmt -check -recursive
    terraform validate

## Security

The configuration can be scanned with Checkov:

    checkov -d terraform --framework terraform

## Variables

Copy the example variables file before customizing deployment values:

    cp terraform.tfvars.example terraform.tfvars

Do not commit files containing environment-specific secrets.

## Provider Locking

The .terraform.lock.hcl file is committed to version control to provide reproducible provider selections.
