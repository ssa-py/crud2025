import sys
import inspect # Importar inspect para obtener miembros de un módulo

# Añade el directorio actual al path para importar módulos locales si ayuda.py se ejecuta solo
sys.path.append('.')

# Importa los módulos de tu aplicación.
# Asegúrate de que estos módulos existen en el mismo directorio
# para que las importaciones funcionen correctamente.
try:
    import main
    import login
    import productos
    import database
except ImportError as e:
    print(f"❌ Error al importar un módulo dependiente en ayuda.py: {e}")
    print("Asegúrate de que 'main.py', 'login.py', 'productos.py' y 'database.py' estén en el mismo directorio.")
    # Exit o manejar el error de forma apropiada si no se pueden importar
    sys.exit(1)


from colorama import Fore, Style, init

# Inicializar colorama para que los estilos se reseteen automáticamente
init(autoreset=True)

# Diccionario para mapear nombres de módulos a sus objetos de módulo
MODULOS_APP = {
    'main': main,
    'login': login,
    'productos': productos,
    'database': database
}

def mostrar_ayuda_general(): # Esta función muestra una guía general del uso de la aplicación
    """
    Muestra una guía general del uso de la aplicación.
    Explica el flujo básico y las funcionalidades principales.
    """
    print(Fore.CYAN + "\n--- Guía de Uso del Sistema de Inventario ---" + Style.RESET_ALL)
    print("Este sistema te permite gestionar productos y usuarios en una base de datos local.")
    print("\n")
    print(Style.BRIGHT + Fore.GREEN + "1.  Inicio de Sesión:" + Style.RESET_ALL)
    print("    Al ejecutar 'main.py', primero accederás al módulo de login.")
    print("    Puedes elegir entre dar de alta un nuevo usuario, iniciar sesión con uno existente,")
    print("    o resetear todos los usuarios para empezar de cero (¡usa esto con precaución!).")
    print("    Las contraseñas no se muestran mientras las escribes por seguridad.")
    print("\n")
    print(Style.BRIGHT + Fore.GREEN + "2.  Menú Principal (Gestión de Productos):" + Style.RESET_ALL)
    print("    Una vez que hayas iniciado sesión exitosamente, se te presentará el menú principal.")
    print("    Aquí podrás realizar todas las operaciones relacionadas con los productos:")
    print("    - ➕ Agregar Producto: Ingresa los detalles de un nuevo producto (nombre, descripción, cantidad, precio, categoría).")
    print("    - 👀 Ver Productos: Muestra una tabla con todos los productos registrados en tu inventario.")
    print("    - 🔍 Buscar Producto: Busca productos por su ID, nombre (parcial) o categoría (parcial).")
    print("    - ✏️ Modificar Producto: Actualiza la información de un producto existente, identificándolo por su ID.")
    print("    - 🚫 Eliminar Producto: Borra un producto específico del inventario usando su ID.")
    print("    - 📈 Reporte de Stock Bajo: Genera una lista de productos cuya cantidad en stock es baja (definirás el límite).")
    print("    - 🚪 Salir: Cierra la aplicación de forma segura.")
    print("\n")
    print(Style.BRIGHT + Fore.GREEN + "3.  Registro de Actividad (log.txt):" + Style.RESET_ALL)
    print("    Todas las acciones importantes que realices (agregar, modificar, eliminar productos, etc.)")
    print("    quedarán registradas automáticamente en el archivo `log.txt` para auditoría.")
    print("\n")
    print(Style.BRIGHT + Fore.GREEN + "4.  Base de Datos (inventario.db):" + Style.RESET_ALL)
    print("    La aplicación utiliza una base de datos SQLite ('inventario.db') para almacenar de forma")
    print("    persistente tanto los usuarios como los productos, asegurando que tus datos no se pierdan.")
    print(Fore.GREEN + "\n¡Esperamos que esta guía te sea de gran utilidad para gestionar tu inventario eficientemente! - Gracias por utilizar crud2025 - ssa" + Style.RESET_ALL)

def mostrar_docstring(modulo_o_funcion):
    """
    Función auxiliar para mostrar la docstring (documentación) de un objeto.
    Acepta un módulo o una función como argumento.
    """
    nombre_objeto = getattr(modulo_o_funcion, '__name__', 'Objeto Desconocido')
    doc = getattr(modulo_o_funcion, '__doc__', None)

    if doc:
        print(Fore.YELLOW + f"\n--- Documentación de {nombre_objeto} ---" + Style.RESET_ALL)
        print(Style.DIM + doc.strip() + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ No se encontró documentación para '{nombre_objeto}'. Asegúrate de que tenga una docstring." + Style.RESET_ALL)

def obtener_funciones_de_modulo(modulo):
    """
    Obtiene una lista de funciones definidas en un módulo dado,
    excluyendo las importaciones y funciones internas/privadas.
    """
    funciones = []
    for nombre, obj in inspect.getmembers(modulo):
        if inspect.isfunction(obj) and obj.__module__ == modulo.__name__:
            # Excluir funciones que no son parte "pública" del módulo
            if not nombre.startswith('_') and nombre != 'main': # 'main' es la función principal del módulo, no una utilidad.
                funciones.append(obj) # Añadir la función a la lista si es pública y no es 'main'
    return sorted(funciones, key=lambda f: f.__name__) # Ordenar alfabéticamente

def menu_ayuda():
    """
    Presenta un menú de ayuda que permite al usuario seleccionar
    qué sección de la documentación desea consultar.
    """
    while True:
        print(Fore.BLUE + "\n--- Menú de Ayuda ---" + Style.RESET_ALL)
        print("1. Guía general de uso de la aplicación")
        print("2. Documentación del módulo `main.py`")
        print("3. Documentación del módulo `login.py`")
        print("4. Documentación del módulo `productos.py`")
        print("5. Documentación del módulo `database.py`")
        print("6. Ver documentación de una función específica (interactivo)") 
        print("7. Volver al menú principal")
        print(Fore.BLUE + "---------------------" + Style.RESET_ALL)

        opcion_str = input("👉 Selecciona una opción (1-7): ").strip()
        opcion = None

        try:
            opcion = int(opcion_str)
        except ValueError:
            print(Fore.RED + "❌ Error: La opción debe ser un número entero." + Style.RESET_ALL)
            input(Fore.YELLOW + "\nPresiona Enter para continuar..." + Style.RESET_ALL)
            continue

        if opcion == 1:
            mostrar_ayuda_general()
        elif opcion == 2:
            mostrar_docstring(main)# Mostrar la documentación del módulo main
        elif opcion == 3:
            mostrar_docstring(login)# Mostrar la documentación del módulo login
        elif opcion == 4:
            mostrar_docstring(productos)# Mostrar la documentación del módulo productos
        elif opcion == 5:
            mostrar_docstring(database)# Mostrar la documentación del módulo database
        elif opcion == 6: # Lógica para la selección interactiva de funciones
            while True:
                print(Fore.CYAN + "\n--- Selecciona un Módulo para ver sus funciones ---" + Style.RESET_ALL)
                modulos_ordenados = sorted(MODULOS_APP.keys())
                for i, mod_nombre in enumerate(modulos_ordenados, start=1):
                    print(f"{i}. {mod_nombre}.py")
                print(f"{len(modulos_ordenados) + 1}. Volver al menú de Ayuda")

                opcion_modulo_str = input("👉 Selecciona un módulo (número): ").strip()
                try:
                    opcion_modulo = int(opcion_modulo_str)
                    if opcion_modulo == len(modulos_ordenados) + 1:
                        break # Salir del bucle de selección de módulo
                    
                    if 1 <= opcion_modulo <= len(modulos_ordenados):
                        modulo_seleccionado_nombre = modulos_ordenados[opcion_modulo - 1]
                        modulo_obj = MODULOS_APP[modulo_seleccionado_nombre]
                        
                        funciones_disponibles = obtener_funciones_de_modulo(modulo_obj)
                        
                        if not funciones_disponibles:
                            print(Fore.YELLOW + f"⚠ No se encontraron funciones documentables en '{modulo_seleccionado_nombre}.py'." + Style.RESET_ALL)
                            input(Fore.YELLOW + "\nPresiona Enter para continuar..." + Style.RESET_ALL)
                            continue

                        while True:
                            print(Fore.GREEN + f"\n--- Funciones en {modulo_seleccionado_nombre}.py ---" + Style.RESET_ALL)
                            for i, func in enumerate(funciones_disponibles, start=1):
                                print(f"{i}. {func.__name__}")
                            print(f"{len(funciones_disponibles) + 1}. Volver a la selección de módulo")

                            opcion_funcion_str = input("👉 Selecciona una función (número): ").strip()
                            try:
                                opcion_funcion = int(opcion_funcion_str)
                                if opcion_funcion == len(funciones_disponibles) + 1:
                                    break # Salir del bucle de selección de función
                                
                                if 1 <= opcion_funcion <= len(funciones_disponibles):
                                    funcion_seleccionada = funciones_disponibles[opcion_funcion - 1]
                                    mostrar_docstring(funcion_seleccionada)
                                else:
                                    print(Fore.RED + "❌ Opción de función inválida." + Style.RESET_ALL)
                            except ValueError:
                                print(Fore.RED + "❌ Error: La opción debe ser un número entero." + Style.RESET_ALL)
                            input(Fore.YELLOW + "\nPresiona Enter para continuar..." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "❌ Opción de módulo inválida." + Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + "❌ Error: La opción debe ser un número entero." + Style.RESET_ALL)
                input(Fore.YELLOW + "\nPresiona Enter para continuar..." + Style.RESET_ALL)


        elif opcion == 7:
            print(Fore.YELLOW + "🔙 Volviendo al menú principal..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "❌ Opción inválida. Por favor, selecciona un número del 1 al 7." + Style.RESET_ALL)

        if opcion != 7: # Evita pedir Enter si ya está saliendo
            input(Fore.YELLOW + "\nPresiona Enter para continuar..." + Style.RESET_ALL)

if __name__ == "__main__":
    menu_ayuda()

