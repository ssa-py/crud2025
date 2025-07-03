"""
Este módulo contiene las funciones para la gestión de productos
(agregar, ver, buscar, modificar, eliminar) y la generación de reportes
de stock bajo en el sistema de inventario.
"""

from colorama import Fore, Style # Importar Style para poder usar Style.RESET_ALL
import database # Importar el módulo de base de datos

# Las funciones cargar_productos y guardar_productos de JSON ya no son necesarias aquí.
# Tampoco necesitamos 'random' para generar códigos de producto, ya que la base de datos
# maneja el ID autoincremental.

def mostrar_productos_en_tabla(productos):
    """
    Función auxiliar para imprimir productos en formato de tabla.
    Acepta una lista de objetos sqlite3.Row.
    """
    if not productos:
        print(Fore.RED + "❌ No hay productos para mostrar." + Style.RESET_ALL)
        return

    print("\n┌───────┬─────────────────┬─────────────────────┬──────────┬───────────┬──────────────────┐")
    print("│ {:<5} │ {:<15} │ {:<19} │ {:<8} │ {:<9} │ {:<16} │".format("ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"))
    print("├───────┼─────────────────┼─────────────────────┼──────────┼───────────┼──────────────────┤")

    for producto in productos:
        # Asegurarse de que las cadenas no excedan el ancho de la columna
        nombre_display = (producto['nombre'][:14] + '..') if len(producto['nombre']) > 16 else producto['nombre']
        descripcion_display = (producto['descripcion'][:17] + '..') if len(str(producto['descripcion'])) > 19 else str(producto['descripcion'])
        categoria_display = (producto['categoria'][:15] + '..') if len(producto['categoria']) > 17 else producto['categoria']

        print(f"│ {producto['id']:<5} │ {nombre_display:<15} │ {descripcion_display:<19} │ {producto['cantidad']:<8} │ ${producto['precio']:<8.2f} │ {categoria_display:<16} │")
    print("└───────┴─────────────────┴─────────────────────┴──────────┴───────────┴──────────────────┘")


def agregar_producto(productos_en_memoria): # El parámetro ya no es necesario, pero se mantiene por compatibilidad con main.py
    """
    Función para agregar un producto a la base de datos con nuevos campos.
    """
    categorias_disponibles = ['Fruta', 'Verdura', 'Lácteo', 'Grano', 'Bebida', 'Alcohol',
                              'Papeleria', 'Golosinas', 'Perfumeria', 'Panaderia',
                              'Carnes', 'Congelados', 'Especias y condimentos', 'Limpieza', 'Otros']
    
    categorias_disponibles = sorted(categorias_disponibles)
    salir_otro_producto = True
    while salir_otro_producto:
        print("\n➖➖➖➖ Registro de producto ➖➖➖➖")

        try:
            nombre = input(" ✍️  Ingrese el nombre del producto (o escriba 'salir' para cancelar): ").strip()
            if nombre.lower() == "salir":
                print(Fore.YELLOW + "🔙 Registro de producto cancelado." + Style.RESET_ALL)
                salir_otro_producto = False
                continue
            if not nombre:
                print(Fore.RED + "❌ Error: El nombre no puede estar vacío." + Style.RESET_ALL)
                continue

            descripcion = input(" 📝 Ingrese una breve descripción del producto (opcional): ").strip()
            # Si la descripción está vacía, se almacena como None o cadena vacía, SQLite lo permite.
            if not descripcion:
                descripcion = "Sin descripción"

            cantidad = None
            while cantidad is None:
                cantidad_str = input(" 📦 Ingrese la cantidad disponible (entero): ").strip()
                try:
                    cantidad = int(cantidad_str)
                    if cantidad < 0:
                        print(Fore.RED + "❌ Error: La cantidad no puede ser negativa." + Style.RESET_ALL)
                        cantidad = None # Reinicia para pedir de nuevo
                except ValueError:
                    print(Fore.RED + "❌ Error: La cantidad debe ser un número entero válido." + Style.RESET_ALL)

            precio = None
            while precio is None:
                precio_str = input(" 💰 Ingrese el precio del producto (ej. 12.99): ").strip()
                try:
                    # Usamos float para permitir decimales en el precio
                    precio = float(precio_str)
                    if precio < 0:
                        print(Fore.RED + "❌ Error: El precio no puede ser negativo." + Style.RESET_ALL)
                        precio = None
                except ValueError:
                    print(Fore.RED + "❌ Error: El precio debe ser un número válido (ej. 10, 15.50)." + Style.RESET_ALL)

            # Mostrar categorías ordenadas y opción de nueva categoría
            print("\nSelecciona la categoría del producto:")
            for i, categoria_nombre in enumerate(categorias_disponibles, start=1):
                print(f"{i}. {categoria_nombre}")
            print(f"{len(categorias_disponibles)+1}. Nueva categoría")

            categoria = None
            cat_ok = False
            while not cat_ok:
                opcion_categoria_str = input("Número de categoría (o escriba 'nueva'): ").strip().lower()
                if opcion_categoria_str == "nueva" or opcion_categoria_str == str(len(categorias_disponibles)+1):
                    nueva_categoria = input("Ingrese el nombre de la nueva categoría: ").strip()
                    if nueva_categoria:
                        categoria = nueva_categoria
                        print(f"Categoría agregada: {categoria}")
                        cat_ok = True
                    else:
                        print(Fore.RED + "❌ El nombre de la nueva categoría no puede estar vacío." + Style.RESET_ALL)
                else:
                    try:
                        opcion_categoria = int(opcion_categoria_str)
                        if 1 <= opcion_categoria <= len(categorias_disponibles):
                            categoria = categorias_disponibles[opcion_categoria - 1]
                            print(f"Categoría elegida: {categoria}")
                            cat_ok = True
                        else:
                            print(Fore.RED + "❌ Opción de categoría inválida. Por favor, ingrese un número dentro del rango." + Style.RESET_ALL)
                    except ValueError:
                        print(Fore.RED + "❌ Error: Debe ingresar un número para la categoría o 'nueva'." + Style.RESET_ALL)

            id_nuevo_producto = database.agregar_producto(nombre, descripcion, cantidad, precio, categoria)
            if id_nuevo_producto:
                print(f"🔖 Producto agregado con ID: {id_nuevo_producto}")
            else:
                pass
                print(Fore.RED + "❌ No se pudo agregar el producto. Verifique los datos e intente nuevamente." + Style.RESET_ALL)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n⚠️ Operación cancelada por el usuario." + Style.RESET_ALL)
            salir_otro_producto = False
            continue
        except Exception as e:
            print(Fore.RED + f"❌ Se produjo un error inesperado al agregar producto: {e}" + Style.RESET_ALL)

        if salir_otro_producto:
            otro = input("❗¿Desea agregar otro producto? (si/no): ").strip().lower()
            if otro != "si":
                salir_otro_producto = False

def ver_productos(productos_en_memoria): # El parámetro ya no es necesario
    """Función para ver los productos registrados, obteniéndolos de la base de datos."""
    print(Fore.CYAN + "\n--- Visualizar Productos ---" + Style.RESET_ALL)
    try:
        productos = database.obtener_todos_los_productos() # Obtener productos directamente de la DB
        mostrar_productos_en_tabla(productos) # Usar la función auxiliar para mostrar
    except Exception as e:
        print(Fore.RED + f"❌ Se produjo un error al intentar mostrar los productos: {e}" + Style.RESET_ALL)

def buscar_producto(productos_en_memoria): # El parámetro ya no es necesario
    """Función para buscar un producto en la base de datos por ID, nombre o categoría."""
    print(Fore.CYAN + "\n--- Búsqueda de Productos ---" + Style.RESET_ALL)
    nom_bus_ok = True
    while nom_bus_ok:
        busqueda = input("🔍 Ingrese el ID, nombre o categoría del producto a buscar o escriba 'salir' para cancelar: ").strip()

        if busqueda.lower() == "salir":
            print(Fore.YELLOW + "🔙 Cancelando búsqueda..." + Style.RESET_ALL)
            nom_bus_ok = False
            continue

        if not busqueda:
            print(Fore.RED + "❌ Error: La búsqueda no puede estar vacía, reintente." + Style.RESET_ALL)
            continue

        try:
            # Usar la función obtener_producto_por_id_nombre_o_categoria del módulo database
            resultados = database.obtener_producto_por_id_nombre_o_categoria(busqueda)

            if resultados:
                print("\n➖➖➖➖ Resultados de la Búsqueda ➖➖➖➖")
                mostrar_productos_en_tabla(resultados)
                print(Fore.GREEN + "✅ Producto(s) encontrado(s) exitosamente!" + Style.RESET_ALL)
                nom_bus_ok = False
            else:
                print(Fore.RED + "❌ No se encontraron productos con ese ID, nombre o categoría. Vuelva a intentar." + Style.RESET_ALL)

        except Exception as e:
            print(Fore.RED + f"❌ Se produjo un error durante la búsqueda: {e}" + Style.RESET_ALL)

def modificar_producto():
    """
    Actualiza los datos de un producto existente en la base de datos mediante su ID.
    """
    print(Fore.CYAN + "\n--- Modificar Producto ---" + Style.RESET_ALL)
    productos_actuales = database.obtener_todos_los_productos()
    if not productos_actuales:
        print(Fore.RED + "❌ No hay productos registrados para modificar." + Style.RESET_ALL)
        return

    mostrar_productos_en_tabla(productos_actuales)

    while True:
        id_str = input("✏️ Ingrese el ID del producto a modificar (o 'salir' para cancelar): ").strip()
        if id_str.lower() == 'salir':
            print(Fore.YELLOW + "🔙 Modificación cancelada." + Style.RESET_ALL)
            return

        try:
            id_producto = int(id_str)
            # Buscar el producto por ID para mostrar sus datos actuales
            producto_existente_lista = database.obtener_producto_por_id_nombre_o_categoria(str(id_producto))
            if not producto_existente_lista:
                print(Fore.RED + f"❌ No se encontró ningún producto con ID {id_producto}. Intente de nuevo." + Style.RESET_ALL)
                continue # Pide el ID de nuevo

            producto_actual = producto_existente_lista[0] # Siempre será el primero si se busca por ID exacto

            print(Fore.GREEN + f"\nProducto encontrado (ID: {producto_actual['id']}):" + Style.RESET_ALL)
            print(f"  Nombre actual: {producto_actual['nombre']}")
            print(f"  Descripción actual: {producto_actual['descripcion']}")
            print(f"  Cantidad actual: {producto_actual['cantidad']}")
            print(f"  Precio actual: {producto_actual['precio']:.2f}")
            print(f"  Categoría actual: {producto_actual['categoria']}")
            print(Fore.YELLOW + "Deje en blanco si no desea modificar un campo." + Style.RESET_ALL)

            # Recolectar nuevos datos, permitiendo que queden en blanco
            nuevo_nombre = input(f" Nuevo nombre ({producto_actual['nombre']}): ").strip() or producto_actual['nombre']
            nueva_descripcion = input(f" Nueva descripción ({producto_actual['descripcion']}): ").strip()
            if not nueva_descripcion and producto_actual['descripcion']: # Si el usuario deja en blanco y había una descripción previa
                nueva_descripcion = producto_actual['descripcion']
            elif not nueva_descripcion: # Si el usuario deja en blanco y no había descripción previa
                nueva_descripcion = "Sin descripción"


            nueva_cantidad = None
            while nueva_cantidad is None:
                cantidad_str = input(f" Nueva cantidad ({producto_actual['cantidad']}): ").strip()
                if not cantidad_str: # Si se deja en blanco, usar la cantidad actual
                    nueva_cantidad = producto_actual['cantidad']
                    break
                try:
                    nueva_cantidad = int(cantidad_str)
                    if nueva_cantidad < 0:
                        print(Fore.RED + "❌ Error: La cantidad no puede ser negativa." + Style.RESET_ALL)
                        nueva_cantidad = None
                except ValueError:
                    print(Fore.RED + "❌ Error: La cantidad debe ser un número entero válido." + Style.RESET_ALL)

            nuevo_precio = None
            while nuevo_precio is None:
                precio_str = input(f" Nuevo precio ({producto_actual['precio']:.2f}): ").strip()
                if not precio_str: # Si se deja en blanco, usar el precio actual
                    nuevo_precio = producto_actual['precio']
                    break
                try:
                    nuevo_precio = float(precio_str)
                    if nuevo_precio < 0:
                        print(Fore.RED + "❌ Error: El precio no puede ser negativo." + Style.RESET_ALL)
                        nuevo_precio = None
                except ValueError:
                    print(Fore.RED + "❌ Error: El precio debe ser un número válido (ej. 10, 15.50)." + Style.RESET_ALL)

            # Categoría: similar a agregar, pero preseleccionar la actual
            categorias_disponibles = ['Fruta', 'Verdura', 'Lácteo', 'Grano', 'Bebida', 'Alcohol',
                                      'Papeleria', 'Golosinas', 'Perfumeria', 'Panaderia',
                                      'Carnes', 'Congelados', 'Especias y condimentos', 'Limpieza', 'Otros']
            print("\nSelecciona la nueva categoría del producto (o deja en blanco para mantener la actual):")
            for i, cat_name in enumerate(categorias_disponibles, start=1):
                print(f"{i}. {cat_name}")
            print(f"(Categoría actual: {producto_actual['categoria']})")

            nueva_categoria = producto_actual['categoria'] # Valor por defecto
            opcion_categoria_str = input("Número de categoría: ").strip()
            if opcion_categoria_str: # Solo si el usuario ingresa algo
                try:
                    opcion_categoria = int(opcion_categoria_str)
                    if 1 <= opcion_categoria <= len(categorias_disponibles):
                        nueva_categoria = categorias_disponibles[opcion_categoria - 1]
                    else:
                        print(Fore.RED + "❌ Opción de categoría inválida. Se mantendrá la categoría actual." + Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + "❌ Error: Debe ingresar un número para la categoría. Se mantendrá la categoría actual." + Style.RESET_ALL)

            # Llamar a la función actualizar_producto del módulo database
            if database.actualizar_producto(id_producto, nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria):
                print(Fore.GREEN + "✅ Producto modificado exitosamente!" + Style.RESET_ALL)
            else:
                print(Fore.RED + "❌ No se pudo modificar el producto." + Style.RESET_ALL)
            break # Sale del bucle after attempt to update

        except ValueError:
            print(Fore.RED + "❌ Error: El ID debe ser un número entero válido." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n⚠️ Modificación de producto cancelada por el usuario." + Style.RESET_ALL)
            return
        except Exception as e:
            print(Fore.RED + f"❌ Se produjo un error inesperado durante la modificación: {e}" + Style.RESET_ALL)


def eliminar_producto(productos_en_memoria): # El parámetro ya no es necesario
    """Función para eliminar un producto de la base de datos por su ID."""
    print(Fore.CYAN + "\n--- Eliminar Producto ---" + Style.RESET_ALL)
    productos_actuales = database.obtener_todos_los_productos() # Obtener la lista actual de la DB
    if not productos_actuales:
        print(Fore.RED + "❌ No hay productos registrados para eliminar." + Style.RESET_ALL)
        return

    mostrar_productos_en_tabla(productos_actuales)

    while True:
        id_str = input("🚫 Ingrese el ID del producto a eliminar (o 'salir' para cancelar): ").strip()
        if id_str.lower() == 'salir':
            print(Fore.YELLOW + "🔙 Eliminación cancelada." + Style.RESET_ALL)
            return

        try:
            id_a_eliminar = int(id_str)
            # Llamar a la función eliminar_producto del módulo database
            if database.eliminar_producto(id_a_eliminar):
                # El mensaje de éxito/error ya es impreso por database.eliminar_producto
                pass
            else:
                print(Fore.RED + "❌ No se pudo eliminar el producto." + Style.RESET_ALL)
            break # Sale del bucle after attempt to delete

        except ValueError:
            print(Fore.RED + "❌ Error: El ID debe ser un número entero válido." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n⚠️ Eliminación de producto cancelada por el usuario." + Style.RESET_ALL)
            return
        except Exception as e:
            print(Fore.RED + f"❌ Se produjo un error inesperado al procesar la eliminación: {e}" + Style.RESET_ALL)

def reporte_productos_bajo_limite():
    """
    Genera un reporte de productos cuya cantidad es igual o inferior a un límite especificado por el usuario.
    """
    print(Fore.CYAN + "\n--- Reporte de Productos con Cantidad Baja ---" + Style.RESET_ALL)
    while True:
        limite_str = input("📈 Ingrese el límite de cantidad (mostrar productos con cantidad igual o inferior a este valor, o 'salir' para cancelar): ").strip()
        if limite_str.lower() == 'salir':
            print(Fore.YELLOW + "🔙 Reporte cancelado." + Style.RESET_ALL)
            return

        try:
            limite_cantidad = int(limite_str)
            if limite_cantidad < 0:
                print(Fore.RED + "❌ Error: El límite de cantidad no puede ser negativo." + Style.RESET_ALL)
                continue
            break # Sale del bucle si el límite es válido
        except ValueError:
            print(Fore.RED + "❌ Error: El límite de cantidad debe ser un número entero válido." + Style.RESET_ALL)

    productos_bajo_limite = database.obtener_productos_por_cantidad_limite(limite_cantidad)

    if productos_bajo_limite:
        print(Fore.GREEN + f"\nProductos con cantidad igual o inferior a {limite_cantidad}:" + Style.RESET_ALL)
        mostrar_productos_en_tabla(productos_bajo_limite)
    else:
        print(Fore.YELLOW + f"⚠ No se encontraron productos con cantidad igual o inferior a {limite_cantidad}." + Style.RESET_ALL)




