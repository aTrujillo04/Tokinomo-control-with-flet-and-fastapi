import flet as ft
from utils import control_gadget, set_motor_pwm

def main(page: ft.Page):
    page.title = "Octynomo Dashboard"
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_width = 1200
    page.window_height = 800
    page.padding = 10

    # Fondo difuminado pastel
    background_design = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#dfe6e9", "#ffffff", "#74b9ff"]
        ),
        expand=True,
    )

    gadget_states = {"ilumination": False, "sound": False, "routine": False, "motor": False}
    data_mapping = {"Ilumination": "ilumination", "Sound": "sound", "Routine": "routine", "Motor": "motor"}

    # Login
    txt_user = ft.TextField(
        hint_text="User", border_radius=12, bgcolor="#ffffff",
        height=55, content_padding=15, text_align=ft.TextAlign.LEFT, expand=True
    )
    txt_password = ft.TextField(
        hint_text="Password", password=True, can_reveal_password=True,
        border_radius=12, bgcolor="#ffffff", height=55, content_padding=15, text_align=ft.TextAlign.LEFT, expand=True
    )
    txt_error = ft.Text("⚠️ Incorrect user or password", color="red", visible=False)

    def login_click(e):
        if txt_user.value == "adm" and txt_password.value == "1":
            txt_error.visible = False
            page.go("/panel")
        else:
            txt_error.visible = True
            page.update()

    login_form = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Login", size=32, weight=ft.FontWeight.BOLD, color="#2d3436", text_align=ft.TextAlign.CENTER),
                ft.Image(
                    # URL de imagen de usuario actualizada
                    src="https://e7.pngegg.com/pngimages/146/551/png-clipart-user-login-mobile-phones-password-user-miscellaneous-blue.png",
                    width=120, height=120, fit=ft.ImageFit.CONTAIN
                ),
                txt_user,
                txt_password,
                txt_error,
                ft.ElevatedButton(
                    content=ft.Text("Enter", size=20, weight=ft.FontWeight.BOLD),
                    on_click=login_click,
                    bgcolor="#74b9ff", color="#ffffff", height=50, expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=25,
        width=400,
        height=500,
        border_radius=20,
        bgcolor="#f0f0f0",
        alignment=ft.alignment.center,
    )

    login_view = ft.View(
        "/",
        [
            ft.Stack(
                controls=[
                    background_design,
                    ft.Container(content=login_form, alignment=ft.alignment.center, expand=True),
                    ft.Container(
                        content=ft.Image(
                            # URL de logo actualizada
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png",
                            fit=ft.ImageFit.CONTAIN, opacity=0.9
                        ),
                        width=140, height=100,
                        alignment=ft.alignment.bottom_right, right=10, bottom=10
                    )
                ],
                expand=True
            )
        ]
    )

    # Dashboard
    def gadget_toggle(e):
        btn = e.control
        display_name = btn.data
        gadget_key = data_mapping.get(display_name)
        if not gadget_key:
            return
        gadget_states[gadget_key] = not gadget_states[gadget_key]
        started = gadget_states[gadget_key]
        
        # Change button style based on state
        btn.bgcolor = "#0984e3" if started else "#74b9ff"
        btn.text = f"{display_name}: {'On' if started else 'Off'}"
        
        page.update()
        control_gadget(gadget_key, "on" if started else "off")

    def change_slide(e):
        value = int(e.control.value)
        speed_value.value = f"Speed: {value}%"
        page.update()
        set_motor_pwm(value)

    # Slider
    speed_value = ft.Text("Speed: 0%", size=16, color="#2d3436")
    velocidad_slider = ft.Slider(
        min=0, max=100, divisions=100, value=0,
        on_change=change_slide,
        active_color="#74b9ff", thumb_color="#2d3436", expand=True
    )

    slider_container = ft.Container(
        content=ft.Column([velocidad_slider, speed_value],
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15, border_radius=15, bgcolor="rgba(255,255,255,0.3)", expand=True
    )

    # Botones
    buttons_row = ft.ResponsiveRow(
        spacing=30,  # separa más los botones
        run_spacing=30, # Agrega espaciado vertical para mejor ajuste en pantallas pequeñas
        controls=[
            ft.Container(
                content=ft.ElevatedButton(
                    text=f"{gadget}: Off", data=gadget, on_click=gadget_toggle,
                    bgcolor="#74b9ff",
                    color="#ffffff",
                    height=90,  # Altura aumentada
                    expand=True,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
                ),
                col={"xs":12, "sm":6, "md":3}, expand=True
            ) for gadget in ["Ilumination", "Sound", "Motor", "Routine"]
        ]
    )
    
    # Nuevo contenedor para agrupar títulos
    header_content = ft.Column(
        controls=[
            ft.Text("Octynomo controls", size=32, weight=ft.FontWeight.BOLD, color="#2d3436", text_align=ft.TextAlign.CENTER),
            ft.Text("Features", size=22, color="#0984e3", text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5 # Espacio mínimo entre títulos
    )

    # Panel content: Usa START y un contenedor expandible para empujar el slider hacia abajo
    panel_content = ft.Column(
        controls=[
            header_content, # 1. Títulos
            # Espacio fijo pequeño para la separación inicial de los botones con el título
            ft.Divider(height=40, color="transparent"), 
            
            buttons_row,    # 2. Botones
            
            # 3. Separador fijo para dar una distancia mínima del slider
            ft.Divider(height=80, color="transparent"),
            
            # 4. Contenedor que absorbe todo el espacio vertical extra y empuja el siguiente elemento (el slider) hacia abajo.
            ft.Container(expand=True),
            
            # 5. Slider - Se queda en la parte inferior del espacio disponible
            ft.Container(
                content=slider_container,
                width=800, # Establecemos un ancho máximo para que no se extienda demasiado horizontalmente
            )
        ],
        spacing=20, # Espacio entre los elementos
        alignment=ft.MainAxisAlignment.START, # Asegura que todo comience desde arriba
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )

    panel_view = ft.View(
        "/panel",
        [
            ft.Stack(
                controls=[
                    background_design,
                    ft.Container(
                        content=panel_content, 
                        expand=True, 
                        # Modificado a 60 para subir los títulos
                        alignment=ft.alignment.top_center, 
                        padding=ft.padding.only(top=60, bottom=50, left=20, right=20)
                    ),
                    ft.Container(
                        content=ft.Image(
                            # Logo actualizado
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png",
                            fit=ft.ImageFit.CONTAIN, opacity=0.9
                        ),
                        width=140, height=100,
                        alignment=ft.alignment.bottom_right, right=10, bottom=10
                    )
                ],
                expand=True
            )
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(login_view)
        if page.route == "/panel":
            page.views.append(panel_view)
        page.update()

    page.on_route_change = route_change
    page.go(page.route)

def run_flet():
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)