import atexit
from gpiozero import LED, PWMLED, MotionSensor

#Established pinout
PIN_LUZ = 22
PIN_MOTOR_1A = 12
PIN_PIR = 25
PIN_ENABLE = 4

#Initialized variables to avoid GPIO bussy error
luz = None
motor_1a = None
pir = None
enable = None

#Audio path
SONIDO_PATH = "/home/octinomo/Tokinomo-control-with-flet-and-fastapi/assets/ZWAN.mp3"

#Function to initialize the variables by the defined pinout.
def init_hardware():
    global luz, motor_1a, pir, enable

    luz = LED(PIN_LUZ)
    motor_1a = PWMLED(PIN_MOTOR_1A, frequency=1000)
    pir = MotionSensor(PIN_PIR)
    enable = LED(PIN_ENABLE)
    enable.on()

#Funcion to close and clear all the pinout when the server is closed.
def close_pinout():
    print("Turning off all pinout")
    if enable: enable.close()
    if luz: luz.close()
    if motor_1a: motor_1a.close()


atexit.register(close_pinout)
