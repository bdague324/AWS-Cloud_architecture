# Handwritten digits recognition model training and deployment on distant servers using the MNIST database

## Objective: set up an environment on distant machines to train the handwritten digits recognition CNN model based on the MNIST database, deploy an API on a Web server and access the WebApp to make the prediction.

![MNIST](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/MNIST.PNG)

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Route table
- 3 Ubuntu instances
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
- Update the package manager
  ```
  sudo apt-get update -y
  ```
- Install Anaconda for Linux (Python 3.7 version)
  ```
  wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
  sudo bash Anaconda3-2019.10-Linux-x86_64.sh -u #answer yes to all questions
  ```
- Bind to any ip
  ```
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
  ```
- Activate the environment
  ```
  conda activate nameofyourenv
  ```
- Install ipykernel
  ```
  conda install ipykernel
  ipython kernel install --user --name=nameyouwanttodisplay
  ```

#### OPTIONAL: clone a repository
Once you activated your new environment, you can clone a repository to get some useful files.

- Install git
  ```
  sudo apt-get install git
  ```
- Clone a repository from GitHub
  ```
  git clone https://github.com/leodsti/AWS_Tutorials.git
  ```

#### Install packages
- Install all the packages listed in the `requirements.txt` file
  ```
  pip install -r AWS_Tutorials/MNIST/requirements.txt
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
- Update the package manager
  ```
  sudo apt-get update -y
  ```
- Install Apache 2 on Ubuntu 18.04
  ```
  sudo apt install apache2 -y
  ```
- Copy the **Front End Server public IP address** and paste it to the Web browser. You should then have access to Apache 2 documentation.

![Apache2](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_MNIST-Prediction/Screenshots/Apache2.PNG)

#### OPTIONAL: clone a repository
Clone a repository to get some useful files.

- Install git
  ```
  sudo apt-get install git
  ```
- Clone a repository from GitHub
  ```
  git clone https://github.com/leodsti/AWS_Tutorials.git
  ```

#### Deploy the WebApp
The WebApp components will now be placed on the Front End Server to display the drawing digits interface.

- Move the index.html file
  ```
  sudo mv AWS_Tutorials/MNIST/index.html /var/www/html/
  ```
- Move the static folder
  ```
  sudo mv AWS_Tutorials/MNIST/static/ /var/www/html/
  ```
- Refresh the Web page with the **Front End Server public IP address**.

#### The WebApp is now displayed on the screen.

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
| Custom TCP Rule | TCP        | 5000        | 0.0.0.0/0, ::/0    |

##### Outbound rules:
| Type            | Protocol   | Port Range  | Destination        |
| --------------- | ---------- | ----------- | ------------------ |
| All traffic     | All        | All         | 0.0.0.0/0          |

#### Connect to the instance with PuTTY:
See part 5 of [AWS_Jupyter-Server](https://github.com/lisakoppe/AWS-Cloud_architecture/tree/master/AWS_Jupyter-Server#connection-to-jupyter-server) README file to get instructions.

#### Configure Back End Server
- Update the package manager
  ```
  sudo apt-get update -y
  ```
- Check if Python 3 is installed
- Install pip installer
  ```
  sudo apt-get install python3-pip -y
  ```
- Install Anaconda for Linux (Python 3.7 version)
  ```
  wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
  sudo bash Anaconda3-2019.10-Linux-x86_64.sh -u #answer yes to all questions
  export PATH=~/anaconda3/bin:$PATH #try conda command. To be used if conda command is not found after installation
  ```
- Bind to any ip
  ```
  jupyter notebook --ip=0.0.0.0 --no-browser
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
  ```
- Activate the environment
  ```
  conda activate BackEndEnv
  ```
- Install ipykernel
  ```
  conda install ipykernel
  ipython kernel install --user --name=BackEnd
  ```

#### Install packages
- Install OpenCV Computer Vision Library
  ```
  conda install opencv
  (pip install python3-opencv) to check
  ```
- Install Flask CORS
  ```
  pip install -U flask-cors
  ```
- Install all the packages listed in the `requirements.txt` file
  ```
  pip install -r AWS_Tutorials/MNIST/requirements.txt
  ```

#### OPTIONAL: clone a repository
Clone a repository to get some useful files.

- Install git
  ```
  sudo apt-get install git
  ```
- Clone a repository from GitHub
  ```
  git clone https://github.com/leodsti/AWS_Tutorials.git
  ```

#### Build the API and launch Flask to access the prediction
- Launch the keras_flask.py file
  ```
  cd AWS_Tutorials/MNIST/
  python3 ./keras_flask.py
  ```

#### Update index.html file
- Connect to the Front End Server instance using PuTTY
- Update index.html file
  ```
  cd /var/www/html/
  sudo vi index.html
  ```
- Replace the Front End Public IPv4: http://`Front End Public IPv4`:5000/predict/
Tips: navigate with the arrows, type 'i' enter insert mode, press 'ctrl+c' and then ':wq' to save and exit insert mode, press 'enter' to exit.

#### Update keras_flask.py file
- Connect to the Front End Server instance using PuTTY
- Update keras_flask.py file
  ```
  cd /var/www/html/
  sudo vi keras_flask.py
  ```
- Insert code
  ```
  from flask_cors import CORS
  app = Flask(__name__)
  cors = CORS(app, resources={r"*": {"origins": "*"}})
  ```




#### Access the WebApp and make the prediction
Go to the Web browser and type http://`Front End Public IPv4`:5000/predict/
