# Jumpbox setup on AWS Cloud

### Objective:
======

### Environment requirements:
- 1 VPC
- 2 subnets (1 public and 1 private) in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 3 Amazon EC2 instances (Jumpbox, NAT, FI)
-

### Steps to create the architecture:
1. Create a VPC with <IP>/16 IPv4 CIDR block
2. Create two subnets linked to the VPC with <IP>/24 IPv4 CIDR block within one AZ:
   - One public subnet which will be routed to the Internet
   - One private subnet which will **NOT** have direct access to the Internet
3. Create an Internet Gateway and attach it to the VPC
4. Connect the public subnet to the Internet via the Internet Gateway [...]
5.
6.
7.
8.

### Output:

Console:
```
test
```
