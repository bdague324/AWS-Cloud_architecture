# Amazon Rekognition API

## Objective: set up an environment on distant machines and use Amazon Rekognition API for object and scene detection.

![AWS](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Rekognition-API/Screenshots/AWS_rekognition.gif)

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Route table
- 2 Ubuntu instances (Front-end_server, Back-end_server)
- 2 Security groups

## Steps to create the architecture:
### 1. VPC
Create a VPC with <IP>/16 IPv4 CIDR block.

### 2. Subnet
Create a public subnet linked to the VPC with <IP>/24 IPv4 CIDR block within one AZ.

### 3. Internet Gateway
Create an Internet Gateway and attach it to the VPC.

### 4. Route Table
Create 1 Route Table:
#### Public Route Table associated to the public subnet:

| Destination        | Target                 | Status   | Propagated  |      
| ------------------ | ---------------------- | -------- | ----------- |
| `VPC IPv4 CIDR`    | local                  | active   | No          |
| 0.0.0.0/0          | `IGW id`               | active   | No          |

### 5. Front End Server instance

Coming soon
