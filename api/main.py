import flet as ft
import flet_fastapi
import os
from datetime import datetime
import calendar

def main(page: ft.Page):
    page.title = "TITANFIT Mobile"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 750
    page.padding = 0
    page.bgcolor = "#0F0F0F"

    # Datos iniciales (igual que tu original)
    user_data = {"usuario": "", "genero": "", "nacimiento": "", "peso": "", "altura": ""}
    dias_entrenados = set()
    vasos_agua = [0] # Usamos lista para mutabilidad

    datos_rutinas = {
        "🔥 Abdomen": ["Plancha", "Crunches", "Elevación", "Bicicleta", "P. Lateral", "Escaladores", "V-Ups", "Talones", "G. Ruso", "Superman"],
        "⚖️ Bajar Peso": ["Burpees", "Saltos", "Sentadillas", "Zancadas", "Jumping Jacks", "Flexiones", "Escaladores", "Plancha", "Correr", "Skipping"],
        "🍑 Glúteos": ["Sentadilla", "Puente", "Patada", "Abductores", "Zancada Lateral", "Peso Muerto", "Subida Escalón", "Clamshell", "Fire Hydrant", "Zancada Atrás"],
        "💪 Tonificar": ["Flexión", "Dips", "Curl", "Press", "Sentadilla", "Remo", "Zancada", "Plancha", "Burpees", "V-Ups"],
        "📐 Espalda": ["Remo", "Superman", "Plancha", "Puente", "Gato-Camello", "Pájaro-Perro", "Y-W-T", "Remo Invertido", "Dorsales", "Encogimientos"],
        "🏃 Cardio": ["Skipping", "Burpees", "Jumping Jacks", "Mountain Climbers", "Sprints", "Boxeo", "Saltar Cuerda", "Talones Atrás", "Rodillas Arriba", "Zancadas Salto"]
    }

    # --- FUNCIONES DE NAVEGACIÓN ---
    def show_registro(e=None):
        page.clean()
        
        # Selectores (Cumpliendo tu regla de "Seleccionables")
        dd_dia = ft.Dropdown(label="Día", options=[ft.dropdown.Option(str(i).zfill(2)) for i in range(1,32)], width=80)
        dd_mes = ft.Dropdown(label="Mes", options=[ft.dropdown.Option(m) for m in ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]], width=100)
        dd_año = ft.Dropdown(label="Año", options=[ft.dropdown.Option(str(i)) for i in range(2026, 1950, -1)], width=100)
        
        dd_m = ft.Dropdown(label="M", options=[ft.dropdown.Option("1"), ft.dropdown.Option("2")], width=80)
        dd_cm = ft.Dropdown(label="Cm", options=[ft.dropdown.Option(f"{i:02d}") for i in range(100)], width=100)
        dd_peso = ft.Dropdown(label="Kg", options=[ft.dropdown.Option(str(i)) for i in range(40, 150)], width=100)

        nombre_user = ft.TextField(label="Nombre de Usuario", border_color="#FF2E63")
        genero_seg = ft.SegmentedButton(
            selected={"Masculino"},
            segments=[
                ft.Segment(value="Masculino", label=ft.Text("Masculino")),
                ft.Segment(value="Femenino", label=ft.Text("Femenino")),
            ],
        )

        def finalizar(e):
            if not nombre_user.value or not dd_dia.value:
                page.snack_bar = ft.SnackBar(ft.Text("⚠️ Completa todos los campos"))
                page.snack_bar.open = True
                page.update()
                return
            
            user_data.update({
                "usuario": nombre_user.value,
                "genero": list(genero_seg.selected)[0],
                "nacimiento": f"{dd_dia.value} {dd_mes.value} {dd_año.value}",
                "peso": f"{dd_peso.value} kg",
                "altura": f"{dd_m.value}.{dd_cm.value} m"
            })
            show_main_app()

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text("CREAR CUENTA", size=28, weight="bold", color="#FF2E63"),
                    nombre_user,
                    ft.Text("Género:"),
                    genero_seg,
                    ft.Text("Fecha de Nacimiento:"),
                    ft.Row([dd_dia, dd_mes, dd_año], alignment="center"),
                    ft.Text("Estatura y Peso:"),
                    ft.Row([dd_m, dd_cm, dd_peso], alignment="center"),
                    ft.ElevatedButton("FINALIZAR REGISTRO", bgcolor="#00ADB5", color="white", height=50, on_click=finalizar)
                ], horizontal_alignment="center", scroll="auto"),
                padding=20
            )
        )

    def show_main_app():
        page.clean()
        
        def nav_change(e):
            if e.control.selected_index == 0: show_rutinas()
            elif e.control.selected_index == 1: show_control()
            elif e.control.selected_index == 2: show_perfil()

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.icons.STARS, label="Control"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON, label="Perfil"),
            ],
            on_change=nav_change,
            bgcolor="#1A1A1A"
        )

        # Header con tus links
        page.add(
            ft.Row([
                ft.IconButton(ft.icons.RESTAURANT_MENU, icon_color="#FF2E63", on_click=lambda _: page.launch_url("https://instagram.com/chuyalmada")), # Placeholder Dieta
                ft.IconButton(ft.icons.PHONE, icon_color="#00ADB5", on_click=lambda _: page.launch_url(f"https://wa.me/584127761514")),
                ft.IconButton(ft.icons.CAMERA_ALT, icon_color="white", on_click=lambda _: page.launch_url("https://instagram.com/chuyalmada")),
            ], alignment="spaceEvenly", bgcolor="#1A1A1A")
        )
        
        # Contenedor para el contenido dinámico
        global content_area
        content_area = ft.Column(expand=True, scroll="auto")
        page.add(content_area)
        show_rutinas()

    def show_rutinas():
        content_area.controls.clear()
        grid = ft.ResponsiveRow()
        colores = ["#FF2E63", "#00ADB5", "#FF9F29", "#6A2C70", "#888888", "#555555"]
        
        for i, (nombre, lista) in enumerate(datos_rutinas.items()):
            grid.controls.append(
                ft.Container(
                    content=ft.Text(nombre, weight="bold"),
                    bgcolor=colores[i],
                    padding=20,
                    border_radius=15,
                    col={"xs": 6},
                    height=100,
                    alignment=ft.alignment.center,
                    on_click=lambda _, n=nombre: start_workout(n)
                )
            )
        content_area.controls.append(grid)
        page.update()

    def show_control():
        content_area.controls.clear()
        
        lbl_agua = ft.Text(f"{vasos_agua[0]} Vasos", size=30, weight="bold")
        
        def update_agua(v):
            vasos_agua[0] = max(0, vasos_agua[0] + v)
            lbl_agua.value = f"{vasos_agua[0]} Vasos"
            page.update()

        content_area.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text("💧 HIDRATACIÓN DIARIA", color="#00ADB5", weight="bold"),
                    lbl_agua,
                    ft.Row([
                        ft.IconButton(ft.icons.REMOVE, on_click=lambda _: update_agua(-1)),
                        ft.IconButton(ft.icons.ADD, on_click=lambda _: update_agua(1)),
                    ], alignment="center")
                ], horizontal_alignment="center"),
                bgcolor="#1A1A1A", padding=20, border_radius=15
            )
        )
        page.update()

    def show_perfil():
        content_area.controls.clear()
        content_area.controls.append(
            ft.Column([
                ft.Icon(ft.icons.PERSON, size=80, color="#00ADB5"),
                ft.Text(user_data["usuario"], size=24, weight="bold"),
                ft.Divider(),
                ft.ListTile(title=ft.Text("Género"), subtitle=ft.Text(user_data["genero"])),
                ft.ListTile(title=ft.Text("Nacimiento"), subtitle=ft.Text(user_data["nacimiento"])),
                ft.ListTile(title=ft.Text("Peso"), subtitle=ft.Text(user_data["peso"])),
                ft.ListTile(title=ft.Text("Estatura"), subtitle=ft.Text(user_data["altura"])),
            ], horizontal_alignment="center")
        )
        page.update()

    def start_workout(categoria):
        page.clean()
        ejercicios = datos_rutinas[categoria]
        
        def finalizar_rutina(e):
            page.clean()
            page.add(ft.Column([
                ft.Text("🏆", size=100),
                ft.Text("¡FELICIDADES!", size=35, weight="bold", color="#00ADB5"),
                ft.Text("Rutina completada")
            ], horizontal_alignment="center", alignment="center", expand=True))
            page.update()
            import time
            time.sleep(3)
            show_main_app()

        page.add(
            ft.Column([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: show_main_app()),
                ft.Text(categoria, size=22, weight="bold", color="#FF2E63"),
                ft.Container(
                    content=ft.Text("Imagen/GIF del ejercicio"), # Aquí irían tus imágenes
                    height=200, bgcolor="#1A1A1A", border_radius=15, alignment=ft.alignment.center
                ),
                ft.Text(ejercicios[0].upper(), size=25, weight="bold"),
                ft.Text("60 Segundos", size=40, weight="bold"),
                ft.ElevatedButton("SIGUIENTE EJERCICIO", on_click=finalizar_rutina)
            ], horizontal_alignment="center")
        )

app = flet_fastapi.app(main)
