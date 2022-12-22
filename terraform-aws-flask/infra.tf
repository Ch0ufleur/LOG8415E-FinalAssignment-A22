# LOG8415E - Assignment Final
# infra.tf
# Terraform configuration relative to instance definitions

# Declaring 5 instances of the t2.micro type (1 for mysql standalone, 4 for the cluster)

resource "aws_instance" "t2_instance" {
  count                       = 5
  ami                         = "ami-0a6b2839d44d781b2"
  key_name                    = "standa2"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  subnet_id              = aws_subnet.final_subnet.id
  vpc_security_group_ids = [aws_security_group.final_sg.id]
}

resource "aws_instance" "t2_instance_proxy" {
  count                       = 1
  ami                         = "ami-0a6b2839d44d781b2"
  key_name                    = "standa2"
  instance_type               = "t2.large"
  associate_public_ip_address = true
  subnet_id              = aws_subnet.final_subnet.id
  vpc_security_group_ids = [aws_security_group.proxy.id]
}
