# Jupyter Server setup on AWS Cloud

## Objective: install a Jupyter Server on AWS and access it on Web browser.

## Environment requirements:
- 1 VPC
- 1 public subnet in one Availability Zone
- 1 Internet Gateway associated with the public subnet
- 1 Ubuntu instance (Jupyter_server)
- 1 Route table
- 1 Security group

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

### 5. Ubuntu instance
Create an instance: **Jupyter_server** *(public)* with type Ubuntu Server 18.04 LTS (HVM) *(ami-04b9e92b5572fa0d1)*, enable Auto-assign Public IP to avoid EIP creation (no flexibility needed here) and configure storage to 15GiB (could be less or more depending on your needs).

![Jupyter_Server_instance](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/Jupyter_Server_instance.PNG)

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

## Connection to Jupyter Server
### Convert .pem key to .ppk key with PuTTYgen:
- Download PuTTYgen [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
- Open PuTTYgen and load an existing .pem private key file
- Save your newly created .ppk private key file
- Close PuTTY Key Generator
![PuTTYgen](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/PuTTYgen.PNG)

### Connect to Jupyter Server using PuTTY:
- Download PuTTY [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
- Go to AWS instance page, select Jupyter_server instance, click "Connect" and copy the host name of the instance and associate it to the public IP of the instance. Here: *ubuntu@54.197.70.222*
- Open PuTTY and paste instance host name and IP in the dedicated field and select SSH connection type
- In the left pane, go to `Connection > SSH > Auth` and load the .ppk private key file for authentification
- Go back to "Session" and click on "Save"
- Click on "Open" to connect to the Jupyter Server
![PuTTY](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/PuTTY.PNG)

### Configure Jupyter Server
- Update the package manager
  ```
  sudo apt-get update -y
  ```
- Install Python3.7
  ```
  sudo apt-get install python3.7 -y
  ```
- Check that Python is installed
  ```
  python3
  ```
  Python starts running when it shows ">>>".
  Quit Python with `exit()`
- Test Python by executing a small script in in Ubuntu console:
  - Open a notepad, write a small Python and save it with .py extension
  - Upload the Python script to the distant machine: open WinSCP, go to `Tools > Import sites > Jupyter_server` and press "Login". Then drag and drop the Python script file to your distant machine (in the right pane).
  ![WinSCP](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/WinSCP.PNG)
  - Go to Ubuntu console and execute the Python script: `python 3 myscript.py`. The script result appears on the console.
  - Quit Python3 coding console with `exit()`
- Install pip installer
  ```
  sudo apt-get install python3-pip -y
  ```
  Check the version of pip with `pip3 --version`
- Install Jupyter
  ```
  sudo pip3 install jupyter
  ```
- Bind to any ip
  ```
  jupyter notebook --ip=0.0.0.0
  ```

### Connect to Jupyter Server using browser
- Copy URL of the Jupyter Notebook in the Ubuntu console `http://ip-10-0-1-216:8888/?token=164f3a4db9a19af43bd65e4124ed1fd739bc182f0d6faab0`
- Replace the IP with the public IPv4 of the **Jupyter_server** instance and paste it to the browser page: `http://54.197.70.222:8888/?token=164f3a4db9a19af43bd65e4124ed1fd739bc182f0d6faab0`
Your are now connected to your Jupyter Server.

![Jupyter_Server](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/Jupyter_Server.PNG)

To avoid too many terminal windows, you can keep Jupyter Server running while shutting down terminal:
- Launch command line elsewhere and run it in the background `nohup jupyter notebook --ip=0.0.0.0 &`
If you refresh your browser's page, a *nohup.out* file should appear and Jupyter should keep running.

### Create a virtual environment
Here, we will detail two options to do so:
#### Conda installation
*Advantage of Conda: it allows the setup of virtual environments with different Python versions.*
- Go to your Jupyter Notebook in your Web browser and click on `New > Terminal`
- In the newly opened terminal create a tmp folder
  ```
  mkdir tmp
  ```
- Go to the tmp folder
  ```
  cd tmp/
  ```
- Download Anaconda
  ```
  curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
  bash Anaconda3-2019.10-Linux-x86_64.sh
  ```
  and follow the steps

#### Pew installation
- Go to your Jupyter Notebook in your Web browser and click on `New > Terminal`
- In the newly opened terminal download Pew
  ```
  pip3 install pew
  ```
- Create a new environment in Pew
  ```
  pew new MyPewEnv
  ```
- List all packages already installed
  ```
  pip3 freeze
  ```

### Link virtual environment to Jupyter
- Go to your Jupyter Notebook in your Web browser and click on `New > Terminal`
- In the newly opened terminal install ipykernel
  ```
  pip3 install ipykernel
  ```
- Create the new environment
  ```
  python3 -m ipykernel install --user --name=myEnv1
  ```
![my_env](https://github.com/lisakoppe/AWS-Cloud_architecture/blob/master/AWS_Jupyter-Server/Screenshots/my_env.PNG)

### Bonus: transfer Python packages name in a file and setup a specific environment with it
- Transfer the list of Python packages to a text file
  ```
  pip3 freeze > myEnv.txt
  ```
- Create a new environment with the text file created
  ```
  pew new MyPewEnv2
  pip3 install ipykernel
  pip3 install -r myEnv.txt
  python3 -m ipykernel install --user --name=myVEnv1
  ```

### General tips
- Shut down Jupyter Notebook from Terminal
  ```
  jupyter notebook stop
  ```
- Display the content of a file
  ```
  cat nohup.out
  ```
