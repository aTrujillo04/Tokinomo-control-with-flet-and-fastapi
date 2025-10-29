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

#Variable set to False
active_routine = False

#Assets path defined to use it resources.
ASSETS_DIR = os.path.abspath("assets")

#Instance created for Fastapi app
app = FastAPI(title="Raspberry Controls")


#Set the middleware parameters to change data with any device/source
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Set the hardware init to be registered with app init
@app.on_event("startup")
def startup_event():
    print("Hardware initialized")
    init_hardware()

#Function that defines the routine based in PIR detection
def wait_pir():
    global active_routine
    print("Routine active, waiting for PIR detection")
    while active_routine:
        if hardware.pir.motion_detected:
            print("Movement detected by PIR, initializing routine")
            hardware.luz.on()
            hardware.motor_1a.value = 0.7
            subprocess.Popen(
                ["mpg123", "-q", "--loop", "-1", hardware.SONIDO_PATH],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            break
        time.sleep(0.1)

#Endpoint  /control defined execute the action defined for the 4 buttons.
@app.post("/control")
#async func defined to wait a request while the thread execute other actions
async def control(request: Request):
    #active routine setted as globa routine type
    global active_routine
    #Convert the request (petition) to json without pausing the code.
    data = await request.json()
    gadget = data.get("gadget")
    action = data.get("action")

#If the action is different than on or off the server will log and error.
    if action not in ["on", "off"]:
        return JSONResponse({"status": "error", "message": "Invalid Action"}, status_code=400)
    
#If the gadget is ilumination/on and there's no error in communication the GPIO for the ilumination will turn on
    if gadget == "ilumination":
        hardware.luz.on() if action == "on" else hardware.luz.off()
        return {"status": "ok", "gadget": gadget, "action": action}

#If the gadget is motor/on and there's no error in communication the PWM pin for motor will turn on
    if gadget == "motor":
        value = 0.01 if action == "on" else 0
        hardware.motor_1a.value = value
        return {"status": "ok", "gadget": gadget, "action": action}

#If the gadget is sound/on and there's no error in communication the .mp3 file will replay from the path
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

#If the gadget is routine/on and active routine is not activated the complete routine will start.
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

#Endpoint assigned to control the PWM level in the pin
@app.post("/pwm")
#Async function defined 
async def pwm_control(request: Request):
    #Get te request and change it to json without pause the code.
    data = await request.json()
    value = data.get("value")
    try:
        #Module the PWM output in the pin
        v = int(value)
        if 0 <= v <= 100:
            duty = v / 100
            hardware.motor_1a.value = duty
            return {"status": "ok", "pwm": v}
        return JSONResponse({"status": "error", "message": "Out of range"}, status_code=400)
    except (TypeError, ValueError):
        return JSONResponse({"status": "error", "message": "Invalid value"}, status_code=400)

#Mount the assets folder to get static files (images)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
#Mount the dashboard programmed in HTML 
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

#Main to run the app inside the server with uvicorn. Available for all the sites and listening in port 9000
if __name__ == "__main__":  
    uvicorn.run("server:app", host="0.0.0.0", port=9000)



