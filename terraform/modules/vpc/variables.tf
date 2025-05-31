variable "cidr_block" {
  description = "CIDR du VPC"
  type        = string
}

variable "vpc_name" {
  description = "Nom du VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR du subnet public"
  type        = string
}

variable "availability_zone" {
  description = "AZ pour le subnet"
  type        = string
}

variable "public_subnet2_cidr" {
  description = "CIDR du subnet public 2"
  type        = string
}
variable "availability_zone2" {
  description = "AZ pour le subnet 2"
  type        = string
}
