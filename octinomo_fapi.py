import threading
from fapi_server import run_fastapi
from flet_dashboard import run_flet
from hardware import motor_1a, motor_2a, luz, enable, pir

# Ejecucion
if __name__ == "__main__":
    try:
        threading.Thread(target=run_fastapi, daemon=True).start()
        print("Servidor FastAPI corriendo en http://<RASP_IP>:8000")
        run_flet()
    finally:
        motor_1a.off()
        motor_2a.off()
        luz.off()
        enable.close()
        pir.close()
