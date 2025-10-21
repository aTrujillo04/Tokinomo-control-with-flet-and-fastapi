import os
from gpiozero import LED, PWMLED, MotionSensor

#Hardware configuration
PIN_LUZ = 22
PIN_MOTOR_1A = 12
PIN_MOTOR_2A = 18
PIN_PIR = 25

enable = LED(4)
enable.on()

luz = LED(PIN_LUZ)
motor_1a = PWMLED(PIN_MOTOR_1A, frequency=1000)
motor_2a = PWMLED(PIN_MOTOR_2A, frequency=1000)
pir = MotionSensor(PIN_PIR)

#Audio route
SONIDO_PATH = os.path.join(os.path.dirname(__file__), "ZWAN.mp3")