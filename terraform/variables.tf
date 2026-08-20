variable "aws_region" {
  description = "AWS region for infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "medical-rag-chatbot"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
