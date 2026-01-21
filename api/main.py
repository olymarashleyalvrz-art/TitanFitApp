import flet as ft
import flet_fastapi

def main(page: ft.Page):
    page.title = "TitanFit"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # --- DISEÑO DEL LOGO Y TÍTULO ---
    logo_rayo = ft.Icon(name=ft.icons.BOLT, color="#00BFFF", size=100)
    titulo = ft.Text("TITANFIT", size=45, weight="bold", color="white", italic=True)

    # --- CAMPOS SELECCIONABLES (Como pediste) ---
    # Edad: de 10 a 90 años
    edad_drop = ft.Dropdown(
        label="Selecciona tu Edad",
        width=280,
        border_color="#00BFFF",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 91)]
    )

    # Estatura: de 130 a 220 cm
    estatura_drop = ft.Dropdown(
        label="Estatura (cm)",
        width=280,
        border_color="#00BFFF",
        options=[ft.dropdown.Option(str(i)) for i in range(130, 221)]
    )

    # Peso: de 30 a 200 kg
    peso_drop = ft.Dropdown(
        label="Peso (kg)",
        width=280,
        border_color="#00BFFF",
        options=[ft.dropdown.Option(str(i)) for i in range(30, 201)]
    )

    # --- BOTÓN DE ENTRADA ---
    btn_entrar = ft.Container(
        content=ft.Text("ENTRAR", color="white", weight="bold", size=18),
        alignment=ft.alignment.center,
        width=280,
        height=55,
        bgcolor="#00BFFF",
        border_radius=12,
        on_click=lambda _: print("Entrando...")
    )

    # --- AGREGAR TODO AL CONTENEDOR PRINCIPAL ---
    page.add(
        ft.Column(
            [
                logo_rayo,
                titulo,
                ft.Container(height=30),
                edad_drop,
                ft.Container(height=5),
                estatura_drop,
                ft.Container(height=5),
                peso_drop,
                ft.Container(height=25),
                btn_entrar
            ],
            horizontal_alignment="center",
        )
    )

# CONEXIÓN PARA VERCEL
app = flet_fastapi.app(main)
