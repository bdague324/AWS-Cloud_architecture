# Amazon Rekognition API

## Objective: set up an environment on distant machines and use Amazon Rekognition API for object and scene detection.

![AWS](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Rekognition-API/Screenshots/AWS_rekognition.gif)

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Route table
- 1 Ubuntu instances (Back-end_server)
- 1 Security groups

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

### 5. Back End Server instance
#### Create the instance on AWS:
Create an instance: **Back-end_server** *(public)* with type Ubuntu Server 18.04 LTS (HVM) *(ami-04b9e92b5572fa0d1)*, type t2.micro, enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here) and configure storage to 10GiB (could be less or more depending on your needs).

Configure the associated security group as follows:
##### Inbound rules:
| Type            | Protocol   | Port Range  | Source             |
| --------------- | ---------- | ----------- | ------------------ |
| SSH             | TCP        | 22          | 0.0.0.0/0          |
| Custom TCP Rule | TCP        | 8888        | 0.0.0.0/0, ::/0    |

##### Outbound rules:
| Type            | Protocol   | Port Range  | Destination        |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | All         | 0.0.0.0/0          |

#### Connect to the instance with PuTTY:
See part 5 of [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#connection-to-jupyter-server) README file to get instructions.

#### Configure Back End Server
  ```
  sudo apt-get update -y
  sudo apt-get install python3-pip -y
  pip install boto3
  wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
  sudo bash Anaconda3-2019.07-Linux-x86_64.sh
  source ~/.bashrc
  conda update --all --yes
  jupyter notebook --ip=0.0.0.0 --no-browser #if you want to have access via Web browser
  ```

Or see [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#conda-installation) README file to get instructions.

#### Connect to Back End Server using browser
See [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#connect-to-jupyter-server-using-browser) README file to get instructions.

#### Create a virtual environment
- Go to your Jupyter Notebook in your Web browser and click on `New > Terminal`
- In the newly opened terminal create the new environment using conda
  ```
  conda create -n nameofyourenv python=3.6
  conda install nb_conda
  conda activate nameofyourenv
  conda install ipykernel
  ipython kernel install --user --name=nameyouwanttodisplay
  ```

#### OPTIONAL: clone a repository
Once you activated your new environment, you can clone a repository to get some useful files.

  ```
  sudo apt-get install git
  git clone https://github.com/lisakoppe/AWS-Cloud_architecture.git
  ```

#### Run the AWS Rekognition API on a picture
Make sure to save a photo to your current directory and to make the following changes in the python [reko.py](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Rekognition-API/reko.py) script:
- Change the picture's name
- Change the AWS credentials (access key id and secret access key)

Run the python [reko.py](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Rekognition-API/reko.py) script and then check the label recognized.

![Rekognition result](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Rekognition-API/Screenshots/result.PNG)
