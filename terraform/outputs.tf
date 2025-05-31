output "vpc_id" {
  value = module.vpc.vpc_id
}
output "public_subnet_id" {
  value = module.vpc.public_subnet_id
}

output "s3_bucket_name" {
  value = aws_s3_bucket.app_bucket.bucket
}

output "eks_cluster_id" {
  value = module.eks.cluster_id
}
output "eks_cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
output "eks_cluster_security_group_id" {
  value = module.eks.cluster_primary_security_group_id
}
output "eks_node_group_role_arn" {
  value = module.eks.eks_managed_node_groups["demo"].iam_role_arn
}
