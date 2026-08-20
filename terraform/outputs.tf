output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.medical_rag.name
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.medical_rag.repository_url
}

output "aws_region" {
  description = "AWS deployment region"
  value       = var.aws_region
}
