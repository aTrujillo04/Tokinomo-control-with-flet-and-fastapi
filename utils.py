import httpx

RASP_IP = "http://10.42.0.1:8000"

async def control_gadget(gadget: str, action: str):
    """
    Envía comandos ON/OFF a la API de control de hardware de forma asíncrona.
    
    Usar httpx es CRÍTICO para no bloquear la interfaz de Flet.
    """
    try:
        # Usamos httpx.AsyncClient para manejar la petición de forma asíncrona
        async with httpx.AsyncClient(base_url=RASP_IP) as client:
            # El 'await' aquí es necesario porque la petición de red es una operación asíncrona
            response = await client.post(
                "/control",
                json={"gadget": gadget, "action": action},
                timeout=5.0
            )
        if response.status_code == 200:
            print(f"Control {gadget} OK: {action}")
        else:
            print(f"Error al controlar {gadget} (Código {response.status_code}): {response.text}")
    except Exception as e:
        print(f"Error de conexión al API /control: {e}")

async def set_motor_pwm(value: int):
    """
    Envía el valor PWM del motor a la API de forma asíncrona.
    """
    try:
        async with httpx.AsyncClient(base_url=RASP_IP) as client:
            # El 'await' aquí es necesario porque la petición de red es una operación asíncrona
            response = await client.post(
                "/pwm",
                json={"value": value},
                timeout=5.0
            )
        if response.status_code == 200:
            print(f"PWM OK: {value}%")
        else:
            print(f"Error al establecer PWM (Código {response.status_code}): {response.text}")
    except Exception as e:
        print(f"Error de conexión al API /pwm: {e}")