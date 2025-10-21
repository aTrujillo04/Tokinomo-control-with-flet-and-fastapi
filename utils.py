import requests

RASP_IP = "http://127.0.0.1:8000"

def control_gadget(gadget, state):
    try:
        r = requests.post(f"{RASP_IP}/control", json={"gadget": gadget, "action": state}, timeout=3)
        print(f"✅ Enviado: {gadget} -> {state} | Respuesta: {r.text}")
    except Exception as e:
        print(f"⚠️ Error al conectar: {e}")

def set_motor_pwm(value):
    try:
        r = requests.post(f"{RASP_IP}/pwm", json={"value": int(value)}, timeout=3)
        print(f"✅ PWM {value}% | Respuesta: {r.text}")
    except Exception as e:
        print(f"⚠️ Error al enviar PWM: {e}")
