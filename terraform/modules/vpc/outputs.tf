output "vpc_id" {
  value = aws_vpc.main.id
}
output "public_subnet_id" {
  value = aws_subnet.public_1.id
}
output "public_subnet2_id" {
  value = aws_subnet.public_2.id
}
