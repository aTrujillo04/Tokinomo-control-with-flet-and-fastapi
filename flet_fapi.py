import time
import threading
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from hardware import luz, motor_1a, motor_2a, pir, SONIDO_PATH
import flet as ft
from flet.fastapi import app as flet_app
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from utils import control_gadget, set_motor_pwm

# --- GLOBAL VARIABLES ---
active_routine = False
ASSETS_DIR = os.path.abspath("assets")

# --- FASTAPI SERVERS ---
control_app = FastAPI()
control_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@control_app.post("/control")
async def control(request: Request):
    global active_routine
    data = await request.json()
    gadget = data.get("gadget")
    action = data.get("action")

    if action not in ["on", "off"]:
        return JSONResponse({"status": "error", "message": "Invalid Action"}, status_code=400)

    if gadget == "ilumination":
        luz.on() if action == "on" else luz.off()
        return {"status": "ok", "gadget": gadget, "action": action}

    if gadget == "motor":
        value = 1 if action == "on" else 0
        motor_1a.value = value
        motor_2a.value = value
        return {"status": "ok", "gadget": gadget, "action": action}

    if gadget == "sound":
        if action == "on":
            subprocess.Popen(["mpg123", "-q", "--loop", "-1", SONIDO_PATH],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
            luz.off()
            motor_1a.value = 0
            motor_2a.value = 0
            subprocess.run(["pkill", "mpg123"])
            return {"status": "ok", "gadget": gadget, "action": "off"}

    return JSONResponse({"status": "error", "message": "Invalid gadget"}, status_code=400)

@control_app.post("/pwm")
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

# --- 2️⃣ Servidor FLET ---
flet_app_instance = FastAPI()
flet_app_instance.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@flet_app_instance.get("/")
async def root():
    return RedirectResponse(url="/flet")

async def main(page: ft.Page):
    page.title = "Octynomo Login"
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800

    def gradient_background():
        return ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=["#dfe6e9", "#ffffff", "#74b9ff"],
            ),
            expand=True,
        )

    # --- LOGIN ---
    txt_user = ft.TextField(label="User", border_radius=12, bgcolor="#ffffff", width=300)
    txt_password = ft.TextField(label="Password", password=True, can_reveal_password=True,
                                border_radius=12, bgcolor="#ffffff", width=300)
    txt_error = ft.Text("⚠️ Incorrect user or password", color="red", visible=False)

    def login_click(e):
        if txt_user.value == "adm" and txt_password.value == "1":
            txt_error.visible = False
            show_panel()
        else:
            txt_error.visible = True
        page.update()

    def hide_error(e):
        if txt_error.visible:
            txt_error.visible = False
            page.update()

    txt_user.on_change = hide_error
    txt_password.on_change = hide_error

    login_box = ft.Container(
        width=450,
        height=550,
        bgcolor="rgba(255,255,255,0.95)",
        border_radius=25,
        padding=40,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Text("Login", size=42, weight=ft.FontWeight.BOLD, color="#2d3436"),
                ft.Image(src="logi.png", width=180, height=180, fit=ft.ImageFit.CONTAIN,  tooltip="Image"),
                txt_user,
                txt_password,
                ft.ElevatedButton(
                    text="Enter",
                    width=220,
                    height=50,
                    bgcolor="#0984e3",
                    color="#ffffff",
                    on_click=login_click,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                txt_error
            ],
        ),
    )

    # --- PANEL ---
    def show_panel():
        page.clean()
        background = gradient_background()

        title = ft.Text(
            "Octynomo Control Panel",
            size=50,
            weight=ft.FontWeight.BOLD,
            color="#2d3436",
            text_align=ft.TextAlign.CENTER,
        )

        gadget_states = {"Illumination": False, "Sound": False, "Motor": False, "Routine": False}

        # --- Toggle Buttons async ---
        async def toggle_button(e):
            btn = e.control
            name = btn.data
            state = not gadget_states[name]
            gadget_states[name] = state
            btn.content.value = f"{name}: {'On' if state else 'Off'}"
            btn.bgcolor = "#0984e3" if state else "#74b9ff"
            btn.update()

            gadget_map = {
                "Illumination": "ilumination",
                "Sound": "sound",
                "Motor": "motor",
                "Routine": "routine"
            }

            await control_gadget(gadget_map[name], "on" if state else "off")

        # --- Botones ---
        buttons_row = ft.Row(
            controls=[
                ft.ElevatedButton(
                    content=ft.Text(name + ": Off", size=24, weight=ft.FontWeight.BOLD),
                    data=name,
                    bgcolor="#74b9ff",
                    color="#ffffff",
                    width=280,
                    height=110,
                    on_click=toggle_button,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25))
                )
                for name in ["Illumination", "Sound", "Motor", "Routine"]
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # --- Slider ---
        slider_value = ft.Text("Speed: 0%", size=20, color="#2d3436")

        async def change_slide(e):
            value = int(e.control.value)
            slider_value.value = f"Speed: {value}%"
            slider_value.update()
            await set_motor_pwm(value)

        slider = ft.Slider(
            min=0, max=100, divisions=100, value=0,
            on_change=change_slide,
            active_color="#74b9ff",
            thumb_color="#2d3436",
            width=600
        )

        panel_layout = ft.Column(
            controls=[
                title,
                ft.Container(height=130),
                buttons_row,
                ft.Container(height=200),
                ft.Column([slider, slider_value], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

        page.add(ft.Stack([background, ft.Container(content=panel_layout, alignment=ft.alignment.center, expand=True)], expand=True))

    page.add(ft.Stack([gradient_background(), ft.Container(content=login_box, alignment=ft.alignment.center, expand=True)], expand=True))

# --- Montar Flet ---
flet_app_instance.mount("/flet", flet_app(main, assets_dir=ASSETS_DIR))

# --- Ejecutar todo ---
if __name__ == "__main__":
    # FastAPI backend en hilo
    threading.Thread(target=lambda: uvicorn.run(control_app, host="0.0.0.0", port=8000), daemon=True).start()
    print("🌐 Dashboard corriendo en http://0.0.0.0:9000/flet")
    uvicorn.run(flet_app_instance, host="0.0.0.0", port=9000)