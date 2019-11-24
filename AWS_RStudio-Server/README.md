# RStudio Server setup on AWS Cloud

## Objective: install a RStudio Server on AWS and access it via Ubuntu console.

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Amazon EC2 instance (RStudio_Server)
- 1 EIP
- 1 Route table
- 1 Security group

## Architecture
![Architecture_diagram]()

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

### 5. EC2 instance
Create an instance: **RStudio_Server** *(public)* with type Amazon Linux 2 AMI HVM and enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here).

![RStudio_Server](X)

Configure the associated security group as follows:
##### Inbound rules:
| Type            | Protocol   | Port Range  | Source             |
| --------------- | ---------- | ----------- | ------------------ |
| SSH             | TCP        | 22          | 0.0.0.0/0          |
| Custom TCP Rule | TCP        | 8787        | 0.0.0.0/0, ::/0    |

##### Outbound rules:
| Type            | Protocol   | Port Range  | Destination        |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | All         | 0.0.0.0/0          |

## Connection to RStudio Server
### Connect via SSH to server on Ubuntu console:
- Go to the local directory where *<KeyPair.pem>* is located
  ```
  cd /mnt/c/Users/Lisa/AWS
  ```
- Copy *<KeyPair.pem>* file to Ubuntu home directory and then change directory
  ```
  cp -i <KeyPair.pem> ~
  cd ~
  ```
- Allow instance to access *<KeyPair.pem>*
  ```
  chmod 400 <KeyPair.pem>
  ```
- Connect to RStudio Server
  ```
  ssh -i <"KeyPair.pem"> ec2-user@<RStudio_Server public IP>
  ```
### Configure RStudio Server
- Update the package manager
  ```
  sudo yum update -y
  ```
- Install R
  ```
  sudo amazon-linux-extras install R3.4 -y
  ```
- Download and install RStudio Server (for Red Hat / CentOS 6-7)
  ```
  wget https://download2.rstudio.org/server/centos6/x86_64/rstudio-server-rhel-1.2.5019-x86_64.rpm
  sudo yum -y install rstudio-server-rhel-1.2.5019-x86_64.rpm
  ```
### Create user (username and password)
```
sudo useradd <username>
echo <username>:<password> | sudo chpasswd
```
### Connect to your RStudio Server
- Go to browser and enter <Server public IPv4>:8787

![RStudio_Server](X)

- Log in with the username and password created

![RStudio_Server](X)

Read more about running R on AWS [here](https://aws.amazon.com/blogs/big-data/running-r-on-aws/).
