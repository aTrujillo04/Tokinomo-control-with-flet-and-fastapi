# Tokinomo Control Dashboard with HTML and Flask

This project is a **Dashboard built with HTML** to control a Tokinomo and its features via a **Raspberry Pi 5**.

![](.png)

## Features

- **Login Section:** License authentication to access the Dashboard.  
- **Feature Controls:** buttons to manage illumination, sound, and DC motor.  
- **Automatic Routine:** A button triggers the full routine in an automate way.  
- **Speed Control:** A slider adjusts the spin motor speed via PWM signals.

## Communication

The Dashboard communicates remotely with the Raspberry Pi using a **Flask server**:

1. The Dashboard sends **HTTP POST requests** with JSON data that contains button states (on/off or PWM values).  
2. The Flask server decodes the data and executes the programmed logic to:
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
- Flet **v0.28.3**
- Flask **v3.1.2**
- Python **v3**

## Installation


```bash
git clone https://github.com/aTrujillo04/Remote-Dashboard-for-Tokinomo-in-Flet
```
