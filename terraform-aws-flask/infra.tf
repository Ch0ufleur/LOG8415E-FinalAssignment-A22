# LOG8415E - Assignment 1
# infra.tf
# Terraform configuration relative to instance definitions

# Declaring 5 instances of the t2.micro type (1 for mysql standalone, 4 for the cluster)

resource "aws_instance" "t2_instance" {
  count                       = 5
  ami                         = "ami-061dbd1209944525c"
  instance_type               = "t2.micro"
  associate_public_ip_address = true
#  user_data = templatefile("../scripts/instance-config.sh.tftpl", {
#    number = count.index + 5
#  })
  subnet_id              = aws_subnet.final_subnet.id
  vpc_security_group_ids = [aws_security_group.final_sg.id]
}
