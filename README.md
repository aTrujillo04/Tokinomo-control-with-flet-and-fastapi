# Tokinomo Control Dashboard with HTML and FastAPI

This project is a **Dashboard built with HTML** to control a Tokinomo and its features via a **Raspberry Pi 5**.

![](/assets/dashboard.gif)

## Features

- **Login Section:** License authentication to access the Dashboard.  
- **Feature Controls:** buttons to manage illumination, sound, and DC motor.  
- **Automatic Routine:** A button triggers the full routine in an automate way.  
- **Speed Control:** A slider adjusts the spin motor speed via PWM signals.

## Communication

The Dashboard communicates remotely with the Raspberry Pi using a **FastAPI server**:

1. The Dashboard sends **HTTP POST requests** with JSON data that contains button states (on/off or PWM values).  
2. The FastAPI server decodes the data and executes the programmed logic to:
   - Turn GPIOs on or off.  
   - Adjust PWM signals according to user input.

This setup enables full remote control of the Tokinomo through the Dashboard.

## Table of contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Operation](#Operation)
- [Specs](#Specs)
- [Project Structure](#Project-Structure)
- [Troubleshooting](#Troubleshooting)
- [Contributing](#Contributing)

## Requirements
**Hardware**
- Functional Laptop or PC
- Raspberry pi 5
- DC Motor
- PIR Movement Sensor
- Any sound output
- Any ilumination output
- Actuator to simulate Tokinomo arm.

**Software**
- Ubuntu **v22.04** 
- FastAPI **v0.120.0**
- Python 3.10

## Installation

The **server.py** script runs a FastAPI server that manages communication between the web interface and the Raspberry Pi hardware. It initializes GPIO components, defines endpoints (/control and /pwm) to operate illumination, motor speed, sound playback, and an automated PIR-based routine. The server also serves static files such as the dashboard and assets, and allows remote interaction through CORS. 

**Index.html** file defines the interactive web dashboard that controls the Raspberry Pi system. It includes a login interface and a dynamic control panel with buttons for illumination, motor, sound, and an automated routine, plus a slider to adjust PWM motor speed. Through JavaScript fetch requests and POST method, it communicates with the FastAPI backend. T

Finally **hardware.py** handles all GPIO-related configurations and interactions with the Raspberry Pi hardware. It defines pin assignments for LEDs, a motor (PWM), and a PIR motion sensor, and initializes them using the gpiozero library. It also provides cleanup functions to safely release GPIO resources when the server shuts down. Additionally, it stores the path to the audio file used in the system’s sound routine.

So now, let's first clone the repository by writing in your terminal:

```bash
git clone https://github.com/aTrujillo04/Tokinomo-control-with-html-and-fastapi.git
```

The server was created in order to **control** the Tokinomo from **any remote device** and keep the server launched in a **local and offline way**.
So first, let's create a virtual enviroment. This virtual enviroment should be created **inside this repository**, it will contain the tools and libraries required to work. 

```bash
cd /route/to/this/repository
python3 -m venv name
source name/bin/activate
```
The previous lines place you in the repository location inside your computer, create your virtual enviroment and activate it. When the virtual enviroment is activated you should see something like this:

```bash
(name) user@computer:~/route/to/repository$
```

Now let's download the requirements **inside the new virtual enviroment** and verify the installation by seeing the downloaded version:

```bash
pip install -r requirements.txt
pip show fastapi requests gpiozero lgpio rpi.gpio uvicorn
```
You should be able to see something like this: **FastAPI vX.X.X**
Then, you wil be able to **launch the server** by entering the following command in the terminal:

```bash
python3 app.py
```

If the server **runs optimally** and is waiting for HTTP requests you should see something like this:

```bash
 @app.on_event("startup")
INFO:     Started server process [2242]
INFO:     Waiting for application startup.
Hardware initialized
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```

Finally, let's create a pm2 process and make it a **startup** one so the FastAPI server will automatically run 15 seconds after the Raspberry is energyzed. In this way, it not neccesary to access graphically to the Raspberry pi 5 and launch the server.

First let's create a .sh file **in home**. The file will contain this:

```bash
#!/bin/bash
sleep 15
pm2 start /home/ubuntu_user/folder/Tokinomo.py --name desired_name --interpreter python3
```
Now, let's create the process. First let's install and verify the nodejs and npm installation:

```bash
sudo apt update
sudo apt upgrade -y

sudo apt install -y nodejs
npm -v

sudo npm install -g pm2
pm2 -v
```
After you see the versions, you can confirm the installation. So now, let's create the pm2 process, first making executable the script.sh you just created:

```bash
chmod +x /home/ubuntu_user/folder/tokinomo_server.sh
```
Now, let's test the pm2 process manually and verify its creation:

```bash
pm2 start /home/pi/Tokinomo/tokinomo_server.sh --desired_name_for_pm2
pm2 status
```
You should see something like this:

```bash
┌─────┬───────────────┬──────┬─────┬─────────┐
│ id  │ name          │ mode │ pid │ status  │
├─────┼───────────────┼──────┼─────┼─────────┤
│ 0   │ tokinomo      │ fork │ 1234│ online  │
└─────┴───────────────┴──────┴─────┴─────────┘
```

FInally, let's make it a **startup** process and save it:

```bash
pm2 startup
```
You will recieve an output such as this one:

```bash
sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u pi --hp /home/user
```
You must copy and enter it to the terminal, and finally make:

```bash
pm2 save
```
To finish, you must restart the raspberry and verify the pm2 creation:

```bash
sudo reboot
pm2 status
```
Again, you must see something like this, and finish the process:

```bash
┌─────┬───────────────┬──────┬─────┬─────────┐
│ id  │ name          │ mode │ pid │ status  │
├─────┼───────────────┼──────┼─────┼─────────┤
│ 0   │ tokinomo      │ fork │ 1234│ online  │
└─────┴───────────────┴──────┴─────┴─────────┘
```

## Operation

You will be able to open the dashboard entering in **any offline/online devide** the url for the site, for example:

```bash
http://**<IP_ADDRESS>**:9000/frontend/
```

First, you will see a login section, which you can bypass by entering the following credentials: **user: a** and **password: 1**. After logging in, the Tokinomo dashboard will be displayed.
Some **IMPORTANT** considerations you must have are than you must be connected to **the same wireless network** from the devide you enter the URL than your Raspberry pi 5. Then, you must enter the correct IP address in the url to complete de connection, you can know it doing in your terminal:

```bash
hostname -I
```

In order to make the communication efficient and easier for the user, a wireless network was created. So, the Raspberry pi 5 could be an available hotspot with **static ip**. In this way, 
a **efficient offline** server was developed. Follow the next steps to do it:

Click on the **WI-fi** icon in the upper right corner of your graphic interface. Then click the **advanced options** button and select the **Create wireless hotspot** option. Finally, enter a valid
wireless network name and password.

![](/assets/wlan.jpeg)

Now, you have created a wireless network that you Raspberry pi 5 can serve as a **hotspot**. So all the devices in which you must open de dashboard **must be connected to your recently created wireless connection** and due to the hotspot function, the Raspberry pi 5 **will always have the same static IP**.

## Specs 
For desired changes inside the dashboard:
- The page title can be modified in the following line (line 6):
  
```bash
 <title> Octinomo Controls </title>
```

- The password and user can be defined in the following lines, and also the message showed for incorrect users (line 246-255):

```bash
f(user==="a" && pass==="1"){
    document.getElementById("login").style.display="none";
    const dash = document.getElementById("dashboard");
    dash.style.display="flex";
    dash.classList.add("show");
    document.getElementById("speedSlider").value = 0;
    updateValue(0);
    error.innerText="";
  } else {
    error.innerText = "User or password incorrect.";
```
- The images can be changed in line 203 and 233:

  ```bash
   <img src="/assets/login.png" alt="Login" class="login-image">
  ``
- To change dashboard titles and its properties check from line 210 to 214:

  ```bash
 <div class="dashboard" id="dashboard">
  <div class="dashboard-header">
    <h1>Octinomo Control</h1>
    <h2>Features</h2>
  </div>
  ```

  ## Project Structure
  
```text
Remote-Dashboard-for-Tokinomo-in-Flet/
├── assets/
│   ├── ZWAN.MP3
│   ├── dashboard.gif
│   └── dashboard.webm
|   |__ login.png
|   |__ logo.png
|   |__wlan.jpeg
├── frontend/
│   ├── index.html
├── gitignore
├── README.md
├── hardware.py
├── requirements.py
├── server.py
```

## Troubleshooting
While trying to use **the dashboard buttons**,you may get this message error:

```bash
⚠️ Error while connecting to Raspberry (ilumination): HTTPConnectionPool(host='192.168.1.169', port=5000): Max retries exceeded with url: /control (Caused by ConnectTimeoutError(<urllib3.connection.HTTPConnection object at 0x72c2b3f513c0>, 'Connection to 192.168.1.169 timed out. (connect timeout=3)
```
This means that the HTTP request is sent, but no recived because of communication troubles with Flask server. So you must:
1. Confirm that your remote PC/Laptop is connected  to the same WI-fi network than your Raspberry.
2. Confirm that the dashboard has the same IP addres than your Raspberry.
3. Verify the Flask server operation.
4. Verify that port 5000 is not blocked.

Another common error you could have while running the **Flask server**:

```bash
Traceback (most recent call last):
  File "Tokinomo.py", line 54, in <module>
    GPIO.setup(4, GPIO.OUT)
  File "/usr/lib/python3/dist-packages/RPi/GPIO/__init__.py", line 164, in setup
    raise error("gpio not allocated")
RuntimeError: gpio not allocated
```
This means that the script cannot access to the GPIO Raspberry pinout, so each of these solutions could help:
1. Look for other proccess or scripts using the pinout and stop them:

```bash
ps aux | grep pigpiod
sudo systemctl stop pigpiod
```
It is optional to restart GPIO service:

```bash
sudo systemctl restart gpiochip
```
2. Execute your script with superuser permissions:

```bash
sudo python3 Tokinomo.py
```
3. It is suggested to clean the pin state at the end of all your scripts, so the pins can stay unocuppied while not running any script. So add at the end of all your scripts that use GPIO pinout:
```bash
GPIO.cleanup()
```

4. Another unlikely solution could be reinstall RPi.GPIO:
```bash
sudo apt purge python3-rpi.gpio -y
sudo apt autoremove -y
sudo apt install python3-rpi.gpio -y
```
**IMPORTANT: AFTER APPLYING ANY OF THESE SOLUTION YOU MUST RESTART THE RASPBERRY AND TEST THE COMMUNICATION AGAIN:**

```bash
sudo reboot
```

## Contributing
Contributions are appreciated. Please follow this steps to contribute:
1. Clon the repository.
2. Create a new branch.
3. Make your changes in the new branch.
4. Commit your changes.
5. Make a push inside your own branch.
6. Make a Pull Request.
