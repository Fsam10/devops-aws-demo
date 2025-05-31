module "vpc" {
  source              = "./modules/vpc"
  cidr_block          = "10.0.0.0/16"
  vpc_name            = "devops-demo-vpc"
  public_subnet_cidr  = "10.0.1.0/24"
  availability_zone   = "us-east-1a"        # ou "eu-west-3a" si tu es à Paris
  public_subnet2_cidr = "10.0.2.0/24"
  availability_zone2  = "us-east-1b"        # ou "eu-west-3b" si tu es à Paris
}

resource "aws_s3_bucket" "app_bucket" {
  bucket = "devops-demo-app-bucket-${random_id.bucket_suffix.hex}"
  force_destroy = true

  tags = {
    Name = "devops-demo-app-bucket"
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "20.8.4"

  cluster_name    = "devops-demo-eks"
  cluster_version = "1.29"

  vpc_id          = module.vpc.vpc_id
  subnet_ids = [
    module.vpc.public_subnet_id,
    module.vpc.public_subnet2_id
  ]
  enable_irsa     = true

  # Un nœud worker t3.small (min pour Free Tier, ajuste selon ton besoin)
  eks_managed_node_groups = {
    demo = {
      desired_capacity = 1
      max_capacity     = 1
      min_capacity     = 1

      instance_types = ["t3.small"]
    }
  }

  # Optionnel : tags
  tags = {
    Environment = "dev"
    Project     = "aws-devops-demo"
  }
}
