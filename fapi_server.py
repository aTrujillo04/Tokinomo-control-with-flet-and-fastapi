import time
import threading
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from hardware import luz, motor_1a, motor_2a, pir, SONIDO_PATH

#Global variable
active_routine = False

# FastApi server
app = FastAPI()

def wait_pir():
    global active_routine
    print("Rutina activa, esperando detección PIR...")
    while active_routine:
        if pir.motion_detected:
            print("PIR detectó movimiento, ejecutando rutina.")
            luz.on()
            motor_1a.value = 0.7
            motor_2a.value = 0.7
            subprocess.Popen(["mpg123", "-q", "--loop", "-1", SONIDO_PATH],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            break
        time.sleep(0.1)

@app.post("/control")
async def control(request: Request):
    global active_routine
    data = await request.json()
    gadget = data.get("gadget")
    action = data.get("action")

    if action not in ["on", "off"]:
        return JSONResponse({"status": "error", "message": "Invalid Action"}, status_code=400)

    # Iluminación
    if gadget == "ilumination":
        luz.on() if action == "on" else luz.off()
        return {"status": "ok", "gadget": gadget, "action": action}

    # Motor
    if gadget == "motor":
        value = 1 if action == "on" else 0
        motor_1a.value = value
        motor_2a.value = value
        return {"status": "ok", "gadget": gadget, "action": action}

    # Sonido
    if gadget == "sound":
        if action == "on":
            subprocess.Popen(["mpg123", "-q", "--loop", "-1", SONIDO_PATH],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(["pkill", "mpg123"])
        return {"status": "ok", "gadget": gadget, "action": action}

    # Rutina completa
    if gadget == "routine":
        if action == "on":
            if not active_routine:
                active_routine = True
                threading.Thread(target=wait_pir, daemon=True).start()
            return {"status": "ok", "gadget": gadget, "action": "on"}
        else:
            active_routine = False
            luz.off()
            motor_1a.value = 0
            motor_2a.value = 0
            subprocess.run(["pkill", "mpg123"])
            return {"status": "ok", "gadget": gadget, "action": "off"}

    return JSONResponse({"status": "error", "message": "Invalid gadget"}, status_code=400)

@app.post("/pwm")
async def pwm_control(request: Request):
    data = await request.json()
    value = data.get("value")
    try:
        v = int(value)
        if 0 <= v <= 100:
            duty = v / 100
            motor_1a.value = duty
            motor_2a.value = duty
            return {"status": "ok", "pwm": v}
        return JSONResponse({"status": "error", "message": "Out of range"}, status_code=400)
    except (TypeError, ValueError):
        return JSONResponse({"status": "error", "message": "Invalid value"}, status_code=400)

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)
