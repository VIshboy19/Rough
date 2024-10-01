# Assignment 3

The purpose of this assignment is to discuss how to send data from an ESP32 to the internet via AWS services.

## Steps

The following steps will show how to set up the AWS server to send the data to the internet:

1. **Step 1**: Hardware and Arduino configuration
   - Connect DHT11 to the computer and to the ESP32 device as shown in the figure below
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/refs/heads/main/WhatsApp%20Image%202024-09-30%20at%208.48.06%20PM.jpeg  "Optional Title")
   - Load the required code(DHT11Default.ino) in Arduino IDE
   - In Library Manager install **SimpleDHT**
   - In Board manager install **esp32** by ExpressIf to version 2.0.11.

2. **Step 2**: AWS configuration
   - After that first setup AWS account

3. **Step 3**: Create EC2 in AWS
   - Amazon EC2 (Elastic Compute Cloud) is a core service provided by Amazon Web Services (AWS) that allows users to rent virtual servers, known as instances, to run applications in the cloud.
   - We will use EC2 to set up a virtual **Ubuntu** system to host the code.
   - First go to Modules in AWS
   - in Modules go to Sandbox envirnoment
   - Then click on **Start Lab**
   - After Start Lab we click on **AWS** button when the button turns green.
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/main/Screenshot%20(17).png  "Optional Title")
   - After starting we will Select EC2

4. **Step 4**: Instance setup
   - First we will setup the virtual machine to have Ubuntu Operating system and have a storage of miminum 28GB.
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/main/Screenshot%20(18).png  "Optional Title")
   - As for Key Pair(login) we will select **Proceed without a Key Pair**
   - Then we launch the instance

5. **Step 5**: Security Setup
   - As seen in the screenshot we setup the security Groups.
   - We launch launch-wizrd-1 and then Edit Inbound rules
   - In Inbound rules We Add rule
   - We set Custom TCP with Port Range to 8080 and save the rules.
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/main/Screenshot%20(20).png "Title")

6. **Step 6**: Instance initialzation
   - In the ubuntu OS we first run sudo apt-get update. It updates the available packages to the latest version 
   - Then we run **sudo apt-get install nodejs npm** It installs nodeJs so that we can run JavaScript codes
   - then we install http-server globally using **sudo npm install -g http-server**
   - http-server is a small server that acts as a server to run small web pages.
   - We then run the http-server
   - We note down the public IP address that appears at the bottom of the windows.

7. **Step 7**: Setup and Running
   - We add the public IP address in Step 7 in our Arduino code DHT11Default.ino
   - We add the IP address in the variable severname.
   - We then send data using sendData
   - The IP address is set up as http://the_ip_address_from_step_7/sendData
   - To check if the server is working we type our IP address followed by the node 8080 that we setup in Step 6
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/main/Screenshot%20(28).png "Title")
   - Then we run the code on the ESP 32
   - Currently we are sending "Error (404): Not Found"
   - We end up seeing "Error (404): Not Found" on our Ubuntu Windows
   - ![Sample Image](https://raw.githubusercontent.com/VIshboy19/Rough/main/Screenshot%20(22).png "Title")

**Conclusion** 

In this assignment, we explored the process of sending data from an ESP32 to the internet using AWS services. By following the outlined steps, one can successfully set up an AWS server to facilitate this communication.