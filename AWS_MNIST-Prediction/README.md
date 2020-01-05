# Handwritten digits recognition model training and deployment on distant servers using the MNIST database

## Objective: set up an environment on distant machines to train the handwritten digits recognition CNN model based on the MNIST database, deploy an API on a Web server and access the WebApp to make the prediction.

![MNIST](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/MNIST.PNG)

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Route table
- 3 Ubuntu instances (Training_server, Front-end_server, Back-end_server)
- 3 Security groups

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

### 5. Jupyter Server instance
#### Create the instance on AWS:
Create an instance: **Training_server** *(public)* with type Ubuntu Server 18.04 LTS (HVM) *(ami-04b9e92b5572fa0d1)*, type m5.xlarge, enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here) and configure storage to 20GiB (could be less or more depending on your needs).

![Training_Server_instance](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Training_Server_instance.PNG)

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

#### Configure Training Server
  ```
  sudo apt-get update -y
  wget https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
  sudo bash Anaconda3-2019.07-Linux-x86_64.sh
  source ~/.bashrc
  conda update --all --yes
  jupyter notebook --ip=0.0.0.0 --no-browser
  ```

Or see [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#conda-installation) README file to get instructions.

#### Connect to Training Server using browser
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

#### Install packages
- Install all the packages listed in the `requirements.txt` file
  ```
  pip install -r AWS-Cloud_architecture/AWS_MNIST-Prediction/requirements.txt
  ```

#### Train the model
The training is based on **60,000 images** and testing is performed on **10,000 images**.

- Go to your Jupyter Notebook in your Web browser and open the `MNIST_CNN.ipynb` file (previously cloned)
- Execute all the cells until cell 9 to train the model with 10 epochs (note that it may take approximately 10 minutes)
- Run cell 10 to save the model as `cnn-mnist`

#### The Jupyter Server instance can now be terminated as it won't be used anymore.

### 6. Front End Server instance
#### Create the instance on AWS:
Create an instance: **Front-end_server** *(public)* with type Ubuntu Server 18.04 LTS (HVM) *(ami-04b9e92b5572fa0d1)*, type t2.micro, enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here) and configure storage to 10GiB (could be less or more depending on your needs).

![Front-end_Server_instance](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Front-end_Server_instance.PNG)

Configure the associated security group as follows:
##### Inbound rules:
| Type            | Protocol   | Port Range  | Source             |
| --------------- | ---------- | ----------- | ------------------ |
| SSH             | TCP        | 22          | 0.0.0.0/0          |
| HTTP            | TCP        | 80          | 0.0.0.0/0, ::/0    |

##### Outbound rules:
| Type            | Protocol   | Port Range  | Destination        |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | All         | 0.0.0.0/0          |

#### Connect to the instance with PuTTY:
See part 5 of [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#connection-to-jupyter-server) README file to get instructions.

#### Configure Front End Server
- Update the package manager and install Apache2
  ```
  sudo apt-get update -y
  sudo apt install apache2 -y
  ```
- Copy the **Front End Server public IP address** and paste it to the Web browser. You should then have access to Apache 2 documentation.

![Apache2](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Apache2.PNG)

#### OPTIONAL: clone a repository
Clone a repository to get some useful files.
  ```
  sudo apt-get install git
  git clone https://github.com/lisakoppe/AWS-Cloud_architecture.git
  ```

#### Deploy the WebApp
The WebApp components will now be placed on the Front End Server to display the drawing digits interface.

- Move the index.html file and the static folder
  ```
  sudo mv AWS-Cloud_architecture/AWS_MNIST-Prediction/index.html /var/www/html/
  sudo mv AWS-Cloud_architecture/AWS_MNIST-Prediction/static/ /var/www/html/
  ```
- Refresh the Web page with the **Front End Server public IP address**.

#### The WebApp is now displayed on the screen but cannot yet make the prediction.

![WebApp](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/WebApp.PNG)

### 7. Back End Server instance
#### Create the instance on AWS:
Create an instance: **Back-end_server** *(public)* with type Ubuntu Server 18.04 LTS (HVM) *(ami-04b9e92b5572fa0d1)*, type t2.micro, enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here) and configure storage to 15GiB (could be less or more depending on your needs).

![Back-end_Server_instance](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Back-end_Server_instance.PNG)

Configure the associated security group as follows:
##### Inbound rules:
| Type            | Protocol   | Port Range  | Source             |
| --------------- | ---------- | ----------- | ------------------ |
| SSH             | TCP        | 22          | 0.0.0.0/0          |
| Custom TCP Rule | TCP        | 8888        | 0.0.0.0/0, ::/0    |
| Custom TCP Rule | TCP        | 5000        | 0.0.0.0/0, ::/0    |

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
- Go to your Back End Server Notebook in your Web browser and click on `New > Terminal`
- In the newly opened terminal create the new environment using conda
  ```
  conda create -n BackEndEnv python=3.6
  conda install nb_conda
  conda activate BackEndEnv
  conda install ipykernel
  ipython kernel install --user --name=BackEnd
  ```

#### Install packages
  ```
  conda install opencv
  pip install -U flask-cors
  pip install -r AWS-Cloud_architecture/AWS_MNIST-Prediction/requirements.txt
  ```

#### OPTIONAL: clone a repository
Clone a repository to get some useful files.
  ```
  sudo apt-get install git
  git clone https://github.com/lisakoppe/AWS-Cloud_architecture.git
  ```

#### Build the API and launch Flask to access the prediction
  ```
  sudo mv AWS-Cloud_architecture/AWS_MNIST-Prediction/cnn-mnist /home/ubuntu/
  sudo mv AWS-Cloud_architecture/AWS_MNIST-Prediction/keras_flask.py /home/ubuntu/
  python keras_flask.py
  ```

#### Update index.html file
- Connect to the Front End Server instance using PuTTY
- Update index.html file
  ```
  cd /var/www/html/
  sudo vi index.html
  ```
- Replace the Back End Public IPv4: http://`Back End Public IPv4`:5000/predict/
Tips: navigate with the arrows, type 'i' enter insert mode, press 'ctrl+c' and then ':wq' to save and exit insert mode, press 'enter' to exit.

#### Access the WebApp and make the prediction
Go to Web browser and enter `Front End Public IPv4`. Draw a digit and hit the *Predict* button. Predicted result based on the trained CNN model is displayed on screen as follows.

![Prediction](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Prediction.PNG)
