"""
Este módulo maneja toda la lógica relacionada con la autenticación
de usuarios, incluyendo el registro de nuevas cuentas, el inicio de sesión,
y la funcionalidad de resetear todos los usuarios del sistema.
"""

# Sección alta y login de usuarios
import getpass
from colorama import Fore, Style, init
import database # Importar el nuevo módulo de base de datos

# Inicializar colorama para que los estilos se reseteen automáticamente
init(autoreset=True)

def alta_usuario():
    """
    Registra un nuevo usuario en la base de datos.
    Ahora pide repetir la contraseña para confirmación.
    """
    try:
        print(Fore.CYAN + "\n--- Alta de Nuevo Usuario ---" + Style.RESET_ALL)
        nombre_usuario = input("Ingrese un nombre de usuario: ").strip()

        if not nombre_usuario:
            print(Fore.RED + "❌ Error: El nombre de usuario no puede estar vacío." + Style.RESET_ALL)
            return

        # Bucle para pedir y confirmar la contraseña
        while True:
            # getpass.getpass() no muestra los caracteres escritos (por seguridad)
            contrasena = getpass.getpass("Ingrese contraseña (por su seguridad no se mostrara en pantalla): ").strip()
            confirmar_contrasena = getpass.getpass("Repita la contraseña para confirmar: ").strip()

            if not contrasena:
                print(Fore.RED + "❌ Error: La contraseña no puede estar vacía. Intente de nuevo." + Style.RESET_ALL)
                continue # Vuelve a pedir las contraseñas
            
            if contrasena == confirmar_contrasena:
                break # Las contraseñas coinciden, sale del bucle
            else:
                print(Fore.RED + "❌ Error: Las contraseñas no coinciden. Intente de nuevo." + Style.RESET_ALL)
                # El bucle continuará pidiendo las contraseñas nuevamente

        # Usar la función agregar_usuario del módulo database
        if database.agregar_usuario(nombre_usuario, contrasena):
            print(Fore.GREEN + "✅ Usuario registrado con éxito!" + Style.RESET_ALL)
        else:
            # El mensaje de error de usuario ya existente lo maneja database.agregar_usuario
            pass # No necesitamos imprimir nada aquí porque la función de la base de datos ya lo hace

    except EOFError:
        print(Fore.RED + "❌ Entrada terminada inesperadamente. No se pudo leer el usuario o la contraseña." + Style.RESET_ALL)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️ Operación de alta de usuario cancelada por el usuario." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"❌ Se produjo un error inesperado durante el alta de usuario: {e}" + Style.RESET_ALL)

def iniciar_sesion():
    """
    Permite a un usuario iniciar sesión usando la base de datos y retorna el nombre del usuario si es exitoso.
    """
    try:
        print(Fore.CYAN + "\n--- Inicio de Sesión ---" + Style.RESET_ALL)
        nombre_usuario = input("Ingrese su usuario: ").strip()
        contrasena = getpass.getpass("Contraseña: ").strip()

        if not nombre_usuario or not contrasena:
            print(Fore.RED + "❌ Usuario y/o contraseña no pueden estar vacíos." + Style.RESET_ALL)
            return None

        # Usar la función obtener_usuario del módulo database
        usuario_logueado = database.obtener_usuario(nombre_usuario, contrasena)

        if usuario_logueado:
            print(Fore.GREEN + f"👌 Bienvenid@ {usuario_logueado} 🔓" + Style.RESET_ALL)
            return usuario_logueado  # Retorna el nombre del usuario
        else:
            print(Fore.RED + "❌ Usuario o contraseña incorrecta, intente nuevamente." + Style.RESET_ALL)
            return None  # Retorna None si el inicio de sesión falla
    except EOFError:
        print(Fore.RED + "❌ Entrada terminada inesperadamente. No se pudo leer el usuario o la contraseña." + Style.RESET_ALL)
        return None
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️ Operación de inicio de sesión cancelada por el usuario." + Style.RESET_ALL)
        return None
    except Exception as e:
        print(Fore.RED + f"❌ Se produjo un error inesperado durante el inicio de sesión: {e}" + Style.RESET_ALL)
        return None

def resetear_usuarios():
    """
    Resetea la lista de usuarios vaciando la tabla de usuarios en la base de datos.
    """
    print(Fore.CYAN + "\n--- Resetear Usuarios ---" + Style.RESET_ALL)
    # Usar la función eliminar_todos_los_usuarios del módulo database
    if database.eliminar_todos_los_usuarios():
        print(Fore.GREEN + "✅ Usuarios reseteados con éxito." + Style.RESET_ALL)
    else:
        print(Fore.RED + "❌ No se pudieron resetear los usuarios." + Style.RESET_ALL)

def main():
    """
    Función principal que maneja el menú de login y alta de usuarios.
    """
    # Asegúrate de que las tablas de la base de datos existan al inicio.
    # Es crucial que esta llamada se haga antes de cualquier operación de DB.
    database.crear_tablas()

    while True:
        print("➖" * 30)
        print("  ✳️    Bienvenido al sistema de carga de productos    ✳️")
        print("1. 🕴️    Alta de usuario")
        print("2. ▶️    Iniciar sesión")
        print("3. 🗑️    Resetear usuarios")
        print("4. 🚪    Salir del Login")
        print("➖" * 30)

        opcion_str = input("Selecciona opción: ").strip()
        opcion = None

        try:
            opcion = int(opcion_str)
        except ValueError:
            print(Fore.RED + "❌ Error: Debe ingresar un número para la opción." + Style.RESET_ALL)
            input("\nPresione Enter para continuar...")
            continue

        try:
            if opcion == 1:
                alta_usuario()
            elif opcion == 2:
                usuario = iniciar_sesion()
                if usuario:  # Si el inicio de sesión fue exitoso
                    return usuario  # Retorna el nombre del usuario para el módulo principal
            elif opcion == 3:
                resetear_usuarios()
            elif opcion == 4:
                print(Fore.YELLOW + "🚪 Saliendo del módulo de Login." + Style.RESET_ALL)
                return None
            else:
                print(Fore.RED + "❌ Opción inválida. Por favor, seleccione un número entre 1 y 4." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Se produjo un error inesperado en el menú principal del login: {e}" + Style.RESET_ALL)

        input("\nPresione Enter para continuar...")

# El bloque __name__ == "__main__" es útil para probar el módulo login
# de forma independiente.
if __name__ == "__main__":
    main()
