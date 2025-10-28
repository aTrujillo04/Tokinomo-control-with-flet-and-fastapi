from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import threading
import time
import os
import uvicorn
import hardware
from hardware import init_hardware

# --- VARIABLES GLOBALES ---
active_routine = False
ASSETS_DIR = os.path.abspath("assets")

# --- SERVIDOR FASTAPI ---
app = FastAPI(title="Raspberry Controls")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes restringirlo si quieres
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    print("🔌 Inicializando hardware...")
    init_hardware()

# --- FUNCIÓN DE RUTINA PIR ---
def wait_pir():
    global active_routine
    print("Rutina activa, esperando detección PIR...")
    while active_routine:
        if hardware.pir.motion_detected:
            print("PIR detectó movimiento, ejecutando rutina.")
            hardware.luz.on()
            hardware.motor_1a.value = 0.7
            subprocess.Popen(
                ["mpg123", "-q", "--loop", "-1", hardwareSONIDO_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            break
        time.sleep(0.1)

# --- ENDPOINT /control ---
@app.post("/control")
async def control(request: Request):
    global active_routine
    data = await request.json()
    gadget = data.get("gadget")
    action = data.get("action")

    if action not in ["on", "off"]:
        return JSONResponse({"status": "error", "message": "Invalid Action"}, status_code=400)

    if gadget == "ilumination":
        hardware.luz.on() if action == "on" else hardware.luz.off()
        return {"status": "ok", "gadget": gadget, "action": action}

    if gadget == "motor":
        value = 0.01 if action == "on" else 0
        hardware.motor_1a.value = value
        return {"status": "ok", "gadget": gadget, "action": action}

    if gadget == "sound":
        if action == "on":
            subprocess.Popen(
                ["mpg123", "-q", "--loop", "-1", hardware.SONIDO_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            subprocess.run(["pkill", "mpg123"])
        return {"status": "ok", "gadget": gadget, "action": action}

    if gadget == "routine":
        if action == "on":
            if not active_routine:
                active_routine = True
                threading.Thread(target=wait_pir, daemon=True).start()
            return {"status": "ok", "gadget": gadget, "action": "on"}
        else:
            active_routine = False
            hardware.luz.off()
            hardware.motor_1a.value = 0
            subprocess.run(["pkill", "mpg123"])
            return {"status": "ok", "gadget": gadget, "action": "off"}

    return JSONResponse({"status": "error", "message": "Invalid gadget"}, status_code=400)

# --- ENDPOINT /pwm ---
@app.post("/pwm")
async def pwm_control(request: Request):
    data = await request.json()
    value = data.get("value")
    try:
        v = int(value)
        if 0 <= v <= 100:
            duty = v / 100
            hardware.motor_1a.value = duty
            return {"status": "ok", "pwm": v}
        return JSONResponse({"status": "error", "message": "Out of range"}, status_code=400)
    except (TypeError, ValueError):
        return JSONResponse({"status": "error", "message": "Invalid value"}, status_code=400)

# --- MONTAR DASHBOARD ---
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/frontend", StaticFiles(directory="frontend", html=True))

# --- MAIN ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000)



