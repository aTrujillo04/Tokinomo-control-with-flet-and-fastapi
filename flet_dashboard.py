import flet as ft
from utils import control_gadget, set_motor_pwm

# Flet dashboard design
def main(page: ft.Page):
    page.title = "Octynomo Dashboard"
    page.scroll = ft.ScrollMode.ALWAYS
    page.window_width = 1200
    page.window_height = 800
    
    page.scroll = ft.ScrollMode.ALWAYS #Page configurations, title, height, width and scroll mode.

    background_design = ft.Stack( #Stack for background design
        [
            ft.Container( #Container with linear gradient background
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=["#0288d1", "#81d4fa", "#b3e5fc"] #Gradient color for blurred effect
                ),
                expand=True,
            ),
            
        ],
        expand=True,
    )

    gadget_states = {"ilumination": False, "sound": False, "routine": False, "motor": False}
    data_mapping = {"Ilumination": "ilumination", "Sound": "sound", "Routine": "routine", "Motor": "motor"}

    
    # Login
    txt_user = ft.TextField(
        hint_text="User", border_radius=12, bgcolor="white",
        height=55, content_padding=15, text_align=ft.TextAlign.LEFT #Text input for username
    )
    txt_password = ft.TextField(
        hint_text="Password", password=True, can_reveal_password=True, 
        border_radius=12, bgcolor="white", height=55, content_padding=15, text_align=ft.TextAlign.LEFT #Text input for password
    )
    txt_error = ft.Text("⚠️ Incorrect user or password", color="red500", visible=False) #Error message for incorrect login

    def login_click(e): #Function to handle login logic
        if txt_user.value == "adm" and txt_password.value == "1": #defined credentials
            page.go("/panel") #If correct, navigate to panel view
        else:
            txt_error.visible = True #If incorrect, show error message
            page.update()

    login_form = ft.Container( #Container for login form
        content=ft.Column(
            controls=[
                ft.Container(expand=True),
                ft.Text(
                    "Login",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="blueGrey900",
                    text_align=ft.TextAlign.CENTER, #Login container design
                ),
                ft.Divider(height=15, color="transparent"),

                ft.Image(
                    src="https://images.icon-icons.com/3446/PNG/512/account_profile_user_avatar_icon_219236.png", 
                    width=120,
                    height=120,
                    fit=ft.ImageFit.CONTAIN, #Image for login container
                ),

                ft.Divider(height=25, color="transparent"), #divider for spacing
                txt_user,
                txt_password, #fields for user and password
                ft.Container(height=20),
                ft.ElevatedButton( #Enter button after entering credentials
                    content=ft.Text("Enter", size=20, weight=ft.FontWeight.BOLD),
                    on_click=login_click,
                    bgcolor="blue700",
                    color="white",
                    height=50 #Button design
                ),
                txt_error, #Error message container
                ft.Container(expand=True), 
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400, 
        height=600,
        padding=35,
        border_radius=20,
        bgcolor="white",
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color="black26"),
        alignment=ft.alignment.center, #ft Container design
    )

    login_view = ft.View( #View for login page
        "/",
        [
            ft.Stack( #Stack for background and login form
                controls=[
                    background_design, #Background design container
                    ft.Container(content=login_form, alignment=ft.alignment.center, expand=True),
                    ft.Container( #Container for logo at bottom right
                        content=ft.Image(
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png",
                            fit=ft.ImageFit.CONTAIN, opacity=0.7
                        ),
                        width=160, height=100, alignment=ft.alignment.bottom_right, right=10, bottom=10
                    )
                ],
                expand=True,
            )
        ]
    )
    

    # Dashboard
       # Panel
    def gadget_toggle(e): #Function to toggle gadget states
        btn = e.control
        display_name = btn.data
        gadget_key = data_mapping.get(display_name) #Get internal key from display name
        if not gadget_key: #Determine if gadget key is valid
            return

        gadget_states[gadget_key] = not gadget_states[gadget_key] #alternate gadget state
        started = gadget_states[gadget_key]
        btn.bgcolor = "green700" if started else "red700"
        btn.text = f"{display_name}: {'On' if started else 'Off'}" #Update button text and color
        page.update()
        control_gadget(gadget_key, "on" if started else "off") #Call service function to control gadget

    def change_slide(e): #Define function to handle slider changes
        value = int(e.control.value)
        speed_value.value = f"Speed: {value}%" #Update speed value text
        page.update()
        set_motor_pwm(value)

    # Slider for motor speed control
    speed_value = ft.Text("Speed: 0%", size=16, color="white")
    velocidad_slider = ft.Slider(
        min=0, max=100, divisions=100, value=0, #Define ranges and divisions
        on_change=change_slide,
        active_color="blue700", thumb_color="blue900", expand=True
    )
    slider_container = ft.Container( #Slider button container
        content=ft.Column(
            [velocidad_slider, speed_value],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=25,
        border_radius=15,
        bgcolor="rgba(255,255,255,0.15)",
        expand=True
    )

    # Buttons
    buttons_row = ft.ResponsiveRow( #Create a responsive row to contain de gadgets buttons
        spacing=25,
        controls=[
            ft.Container( #Each gadget is placed a container
                content=ft.ElevatedButton(
                    text=f"{gadget}: Off", data=gadget, #The button and the state
                    on_click=gadget_toggle, #Calling gadget_toggle
                    bgcolor="red700", color="white",
                    height=90, expand=True, #Buttons design
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)) #Rounded Border for the buttons
                ),
                col={"xs":12, "sm":6, "md":3},
                expand=True,
            ) for gadget in ["Ilumination", "Sound", "Motor", "Routine"]
        ]
    )

    # Dashboard panel content
    panel_content = ft.Container( #Main container inside the dashboard
        content=ft.Column(
            controls=[
                ft.Text("Octynomo controls", size=34, weight="bold", color="white"), #Title and design
                ft.Text("Features", size=22, color="white70"), #Subtitle and design
                buttons_row, #Inserting  buttons responsive row
                ft.Divider(height=40, color="transparent"), 
                slider_container #Insert slider_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25
        ),
        padding=ft.padding.only(left=40, right=40, top=30, bottom=80), #Padding for the container
        border_radius=20,
        bgcolor="rgba(255,255,255,0.1)",
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color="black26"),
        expand=True
    )

    panel_view = ft.View( #View for dashboard panel 
        "/panel",
        [
            ft.Stack( #Stack for background and panel content
                controls=[
                    background_design,
                    ft.Container(content=panel_content, expand=True, alignment=ft.alignment.center),
                    ft.Container(
                        content=ft.Image(
                            src="https://d31i9b8skgubvn.cloudfront.net/folder/logos/3678_logo_IJdTc4y2nxqKLZjf.png", #Insert logo at bottom right
                            fit=ft.ImageFit.CONTAIN, opacity=0.7
                        ),
                        width=130, height=100,
                        alignment=ft.alignment.bottom_right, right=10, bottom=10 #Positioning
                    )
                ],
                expand=True
            )
        ]
    )

    def route_change(route):
        page.views.clear()
        page.views.append(login_view) #Define views based on route
        if page.route == "/panel":
            page.views.append(panel_view)
        page.update() #Update page on route change

    page.on_route_change = route_change
    page.go(page.route)

def run_flet():
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)
