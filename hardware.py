import atexit
from gpiozero import LED, PWMLED, MotionSensor

# --- Pines de hardware ---
PIN_LUZ = 22
PIN_MOTOR_1A = 13
PIN_MOTOR_2A = 18
PIN_PIR = 25
PIN_ENABLE = 4

# --- Variables de hardware (inicialmente None) ---
luz = None
motor_1a = None
motor_2a = None
pir = None
enable = None

# --- Audio ---
SONIDO_PATH = "/home/octinomo/Tokinomo-control-with-flet-and-fastapi/assets/ZWAN.mp3"

def init_hardware():
    """Inicializa los pines de hardware. Llamar solo una vez al iniciar FastAPI"""
    global luz, motor_1a, motor_2a, pir, enable

    luz = LED(PIN_LUZ)
    motor_1a = PWMLED(PIN_MOTOR_1A, frequency=1000)
    motor_2a = PWMLED(PIN_MOTOR_2A, frequency=1000)
    pir = MotionSensor(PIN_PIR)
    enable = LED(PIN_ENABLE)
    enable.on()

def cleanup_gpio():
    print("Turning off all pinout")
    if enable: enable.off()
    if luz: luz.off()
    if motor_1a: motor_1a.off()
    if motor_2a: motor_2a.off()

# Registrar cleanup al salir
atexit.register(cleanup_gpio)
