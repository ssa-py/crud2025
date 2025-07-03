"""
Este es el módulo principal del Sistema de Gestión de Inventario.
Actúa como el punto de entrada de la aplicación, manejando el flujo
de inicio de sesión y el menú principal de operaciones CRUD sobre productos.
También gestiona el logging de las acciones del usuario.
"""

import datetime # Primero los módulos de la librería estándar

from colorama import Fore, Style, Back, init # Luego los módulos de terceros

import database # Finalmente tus módulos locales, en orden alfabético
import login
import productos
import ayuda # NUEVO: Importa el módulo de ayuda

# Es una buena práctica inicializar colorama en el punto de entrada principal
init(autoreset=True)

def generar_log(usuario, accion):
    """
    Genera un log de la sesión.
    """
    try:
        with open('log.txt', 'a', encoding='utf-8') as log_file:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"Usuario: {usuario}, Fecha: {fecha_hora}, Acción: {accion}\n")
        print(Fore.CYAN + f"✅ Log de acción '{accion}' generado exitosamente." + Style.RESET_ALL)
    except IOError as e:
        print(Fore.RED + f"❌ Error al escribir el log: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Ocurrió un error inesperado al generar el log: {e}" + Style.RESET_ALL)

def main():
    """
    Función principal que maneja el menú de la aplicación CRUD.
    Ahora con un menú más estético y saludo personalizado.
    """
    # 1. Asegurarse de que las tablas de la base de datos existan al inicio de la aplicación.
    database.crear_tablas()

    # 2. Manejar el inicio de sesión
    usuario = login.main()  # Captura el nombre del usuario o None si el login falla/se cancela

    if usuario is None:
        print(Fore.YELLOW + "🚪 Saliendo de la aplicación porque el inicio de sesión no fue exitoso o se canceló." + Style.RESET_ALL)
        return # Sale de la función main y termina el programa

    # Si el usuario es válido, continuar con el menú principal
    continuar = True  # Variable para controlar el bucle

    while continuar:  # Bucle para el menú del CRUD
        print(Style.BRIGHT + Fore.BLUE + "\n" + "═" * 60 + Style.RESET_ALL)
        print(Style.BRIGHT + Back.CYAN + Fore.CYAN + "                                                              " + Style.RESET_ALL)
        print(Style.BRIGHT + Back.WHITE + Fore.BLACK + "        ☀️       🛒 GESTIÓN DE INVENTARIO 🛒       ☀️           " + Style.RESET_ALL)
        print(Style.BRIGHT + Back.CYAN + Fore.CYAN + "                                                              " + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.BLUE + "═" * 60 + Style.RESET_ALL)
        print(Fore.CYAN + "           Bienvenid@ " + Style.BRIGHT + f"{usuario}" + Style.RESET_ALL + Fore.CYAN + "!. Al sistema CrUd - V3.0 - SSA" + Style.RESET_ALL)
        print(Fore.BLUE + "─" * 60 + Style.RESET_ALL)
        print(Fore.GREEN + "1. Agregar nuevo producto       ➕" + Style.RESET_ALL)
        print(Fore.GREEN + "2. Ver todos los productos      👀" + Style.RESET_ALL)
        print(Fore.GREEN + "3. Buscar producto              🔍" + Style.RESET_ALL)
        print(Fore.GREEN + "4. Eliminar producto            🚫" + Style.RESET_ALL)
        print(Fore.GREEN + "5. Modificar producto           ✏️" + Style.RESET_ALL)
        print(Fore.GREEN + "6. Reporte de stock bajo        📈" + Style.RESET_ALL)
        print(Fore.RED +   "7. Salir de la aplicación       🚪" + Style.RESET_ALL)
        print(Fore.BLUE + "─" * 60 + Style.RESET_ALL) # LÍNEA EXISTENTE, PERO AHORA SEPARADOR
        print(Fore.BLUE + "8. Ayuda                        ❓" + Style.RESET_ALL) # NUEVO: Opción de Ayuda
        print(Fore.BLUE + "─" * 60 + Style.RESET_ALL) # NUEVO: Separador final

        opcion_str = input(Fore.MAGENTA + "👉 Selecciona una opción (1-8): " + Style.RESET_ALL).strip() # MODIFICADO: Rango de opciones
        opcion = None

        try:
            opcion = int(opcion_str)
        except ValueError:
            print(Fore.RED + "❌ Error: La opción debe ser un número entero." + Style.RESET_ALL)
            input(Fore.YELLOW + "\nPresiona Enter para continuar...\n" + Style.RESET_ALL)
            continue

        match opcion:
            case 1:
                productos.agregar_producto(None)
                generar_log(usuario, "Producto agregado")
            case 2:
                productos.ver_productos(None)
                generar_log(usuario, "Productos vistos")
            case 3:
                productos.buscar_producto(None)
                generar_log(usuario, "Producto buscado")
            case 4:
                productos.eliminar_producto(None)
                generar_log(usuario, "Producto eliminado")
            case 5:
                productos.modificar_producto()
                generar_log(usuario, "Producto modificado")
            case 6:
                productos.reporte_productos_bajo_limite()
                generar_log(usuario, "Reporte de stock bajo generado")
            case 7:
                generar_log(usuario, "Salida del sistema")
                print(Style.BRIGHT + Fore.MAGENTA + "\n✨" + "═" * 58 + "✨" + Style.RESET_ALL)
                print(Style.BRIGHT + Back.WHITE + Fore.BLACK + f"         ¡Adiós, {usuario}!¡Vuelve pronto! 🙋‍♂️                   " + Style.RESET_ALL)
                print(Style.BRIGHT + Fore.MAGENTA + "✨" + "═" * 58 + "✨\n" + Style.RESET_ALL)
                continuar = False
            case 8: # NUEVO: Caso para la opción de Ayuda
                ayuda.menu_ayuda()
                generar_log(usuario, "Acceso a la ayuda")
            case _:
                print(Fore.RED + "❌ Opción Inválida. Por favor, selecciona un número del 1 al 8." + Style.RESET_ALL) # MODIFICADO: Rango de opciones

        if continuar:
            input(Fore.YELLOW + "\nPresiona Enter para continuar...\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
