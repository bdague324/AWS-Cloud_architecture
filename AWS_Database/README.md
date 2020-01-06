# Create a database using RDS instance

## Objective: create a relational database using RDS instance on AWS cloud and connect to it using Python.

## Environment requirements:
- 1 VPC
- 2 public subnets in 2 different Availability Zones
- 1 Internet Gateway associated with the public subnets
- 1 Amazon RDS instance
- 1 database
- 1 EC2 instance
- 1 EIP
- 1 Security group
- 1 Route table

## Architecture
![Architecture_diagram](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Database/Screenshots/Architecture_diagram.png)

## Steps to create the architecture:
### 1. VPC
- Create a VPC with <IP>/16 IPv4 CIDR block
- Once created, select the VPC, click on "Actions" and enable DNS resolution and DNS hostnames

### 2. Internet Gateway
Create an Internet Gateway and attach it to the VPC.

### 3. Subnets
Create two public subnets linked to the VPC with <IP>/24 IPv4 CIDR block in two different Availability Zones.

### 4. Route table
#### Public Route Table associated to the public subnets:

| Destination        | Target                 | Status   | Propagated  |      
| ------------------ | ---------------------- | -------- | ----------- |
| `VPC IPv4 CIDR`    | local                  | active   | No          |
| 0.0.0.0/0          | `IGW id`               | active   | No          |

### 5. Security Group
Create a Security Group:
##### Inbound rules:
| Type            | Protocol   | Port Range  | Source             |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | 0 - 65535   | `local IPv4`       |

##### Outbound rules:
| Type            | Protocol   | Port Range  | Destination        |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | All         | 0.0.0.0/0          |

### 6. IAM role
Go to the IAM service page and click on "roles" and then "create role".
Select "EC2 instance" and then select "Administrator Access" in the permissions policies tab.

### 7. RDS instance & database
Go to the RDS service page and click on "create database".
Then setup your database as follows:

| Parameter                    | Value                                       |
| ---------------------------- | ------------------------------------------- |
| Database creation method     | Standard Create                             |
| Engine options               | MySQL                                       |
| Templates                    | Free tier                                   |
| DB instance identifier       | 'name your DB instance'                     |
| Credentials settings         | Set 'Master username' and 'Master password' |
| Storage autoscaling          | Disable                                     |
| Connectivity                 | Select 'VPC'                                |
| Publicly accessible          | Yes                                         |
| VPC security groups          | Select the one created previously           |
| Initial database name        | 'name your database'                        |
| Backup > automatic backups   | Disable                                     |

### 8. Connect to database using MySQL Workbench
- Download MySQL Workbench [here](https://www.mysql.com/products/workbench/)
- Click on "+" in MySQL Connections section
- Fill in "Connection Name" field
- Fill in "Hostname" field with the endpoint of your database (go to AWS RDS > Database > Connectivity and Security > Endpoint)
- Fill in port: 3306
- Fill in username and password
- Click on "Test Connection"

Note that a pop-up window will appear showing the following statement "Successfully made the MySQL connection".

### 9. Create EC2 instance with IAM role
Create an instance: **Name** *(public)* with type Amazon Linux 2 AMI HVM *(ami-00068cd7555f543d5)* and enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here).

### 10. Connect to database using Python

### 11. Insert data into database

### 12. Display data
