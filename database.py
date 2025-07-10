"""
Este módulo es el encargado de la interacción con la base de datos SQLite.
Define las funciones para conectar a la base de datos, crear las tablas
necesarias (usuarios y productos), y realizar todas las operaciones CRUD
(Crear, Leer, Actualizar, Eliminar) de forma segura utilizando transacciones.
"""
import sqlite3
from colorama import Fore, Style, init

# Inicializar colorama para mensajes de consola
init(autoreset=True)

# Nombre del archivo de la base de datos
ARCHIVO_DB = 'inventario.db'

def conectar_db():
    """
    Establece una conexión con la base de datos SQLite.
    Crea el archivo de la base de datos si no existe.
    Retorna el objeto de conexión.
    """
    try:
        conn = sqlite3.connect(ARCHIVO_DB)
        # Permite acceder a las columnas por nombre (como si fueran diccionarios)
        conn.row_factory = sqlite3.Row
        # print(Fore.GREEN + f"✅ Conexión a la base de datos '{ARCHIVO_DB}' establecida." + Style.RESET_ALL) - se comento para evitar mensajes repetidos
        return conn
    except sqlite3.Error as e:
        print(Fore.RED + f"❌ Error al conectar a la base de datos: {e}" + Style.RESET_ALL)
        return None

def crear_tablas():
    """
    Crea las tablas necesarias en la base de datos si no existen.
    Esta función de configuración no usa BEGIN/COMMIT/ROLLBACK explícitos porque es una operación
    de inicialización y sqlite3 maneja la transacción implícitamente para CREATE TABLE.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()

            # Tabla de Usuarios 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL
                )
            ''')
            print(Fore.GREEN + "✅ Tabla 'usuarios' verificada/creada." + Style.RESET_ALL)

            # Tabla de Categorías
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL
                )
            ''')
            print(Fore.GREEN + "✅ Tabla 'categorias' verificada/creada." + Style.RESET_ALL)
             # Poblar categorías por defecto si está vacía
            cursor.execute("SELECT COUNT(*) as cuenta FROM categorias")
            if cursor.fetchone()['cuenta'] == 0:
                categorias_defecto = [
                    'Fruta', 'Verdura', 'Lácteo', 'Grano', 'Bebida', 'Alcohol',
                    'Papeleria', 'Golosinas', 'Perfumeria', 'Panaderia',
                    'Carnes', 'Congelados', 'Especias y condimentos', 'Limpieza', 'Otros'
                ]
                for cat in categorias_defecto:
                    cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (cat,))
                conn.commit()
                print(Fore.GREEN + "✅ Categorías por defecto insertadas." + Style.RESET_ALL)


            # Tabla de Productos - Esquema Actualizado
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    cantidad INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT NOT NULL
                )
            ''')
            print(Fore.GREEN + "✅ Tabla 'productos' verificada/creada con esquema actualizado." + Style.RESET_ALL)

            conn.commit() # Confirma los cambios de CREATE TABLE  
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al crear tablas: {e}" + Style.RESET_ALL)
        finally:
            conn.close()
            # print(Fore.CYAN + "⚙️ Conexión a DB cerrada después de crear tablas." + Style.RESET_ALL) # Se comento para evitar mensajes repetidos
    else:
        print(Fore.RED + "❌ No se pudo crear las tablas debido a un problema de conexión a la base de datos." + Style.RESET_ALL)
    

# --- Funciones para Usuarios ---

def agregar_usuario(nombre_usuario, contrasena): #parametros obligatorios
    """
    Agrega un nuevo usuario a la base de datos dentro de una transacción.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    conn = conectar_db()
    if conn:
        try:
            conn.execute("BEGIN TRANSACTION") # Inicia la transacción
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena) VALUES (?, ?)", (nombre_usuario, contrasena)) # Inserta el nuevo usuario
            conn.commit() # Confirma los cambios si todo fue bien  
            print(Fore.GREEN + f"✅ Usuario '{nombre_usuario}' agregado exitosamente (transacción confirmada)." + Style.RESET_ALL)
            return True
        except sqlite3.IntegrityError:
            conn.rollback() # Revierte los cambios si el usuario ya existe
            print(Fore.RED + f"❌ Error: El nombre de usuario '{nombre_usuario}' ya existe (transacción revertida)." + Style.RESET_ALL)
            return False
        except sqlite3.Error as e:
            conn.rollback() # Revierte los cambios si hay un error de DB
            print(Fore.RED + f"❌ Error al agregar usuario: {e} (transacción revertida)." + Style.RESET_ALL)
            return False
        finally:
            conn.close()
    return False

def obtener_usuario(nombre_usuario, contrasena): #parametros obligatorios   
    """
    Verifica las credenciales de un usuario.
    (Operación de lectura, no requiere transacción explícita).
    Retorna el nombre de usuario si las credenciales son correctas, None en caso contrario.
    """
    conn = conectar_db() # Conectar a la base de datos
    # Si la conexión es exitosa, se procede a buscar el usuario
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_usuario FROM usuarios WHERE nombre_usuario = ? AND contrasena = ?", (nombre_usuario, contrasena))
            usuario = cursor.fetchone()
            if usuario:
                return usuario['nombre_usuario']
            return None # Si no se encuentra el usuario, retorna None
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al obtener usuario: {e}" + Style.RESET_ALL)
            return None
        finally: # Cierra la conexión a la base de datos
            conn.close()
    return None

def obtener_todos_los_usuarios():
    """
    Obtiene todos los usuarios registrados en la base de datos.
    (Operación de lectura, no requiere transacción explícita).
    Retorna una lista de objetos (sqlite3.Row) para facilitar el acceso por nombre de columna.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_usuario, contrasena FROM usuarios")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al obtener todos los usuarios: {e}" + Style.RESET_ALL)
            return []
        finally:
            conn.close()
    return []

def eliminar_todos_los_usuarios():
    """
    Elimina todos los usuarios de la base de datos dentro de una transacción.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    conn = conectar_db()
    if conn:
        try:
            conn.execute("BEGIN TRANSACTION") # Inicia la transacción
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios")
            conn.commit() # Confirma los cambios
            print(Fore.YELLOW + "🗑️ Todos los usuarios eliminados exitosamente (transacción confirmada)." + Style.RESET_ALL)
            return True
        except sqlite3.Error as e:
            conn.rollback() # Revierte los cambios si hay un error de DB
            print(Fore.RED + f"❌ Error al eliminar todos los usuarios: {e} (transacción revertida)." + Style.RESET_ALL)
            return False
        finally:
            conn.close()
    return False

# --- Funciones para Productos ---

def agregar_producto(nombre, descripcion, cantidad, precio, categoria): #parametros obligatorios
    """
    Agrega un nuevo producto a la base de datos dentro de una transacción.
    Retorna el ID del nuevo producto si la operación fue exitosa, None en caso contrario.
    """
    conn = conectar_db()
    if conn:
        try:
            conn.execute("BEGIN TRANSACTION") # Inicia la transacción
            cursor = conn.cursor()
            cursor.execute("INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
                           (nombre, descripcion, cantidad, precio, categoria))
            conn.commit() # Confirma los cambios
            last_id = cursor.lastrowid # Obtiene el ID autoincremental del producto insertado
            print(Fore.GREEN + f"✅ Producto '{nombre}' agregado exitosamente con ID {last_id} (transacción confirmada)." + Style.RESET_ALL)
            return last_id
        except sqlite3.Error as e:
            conn.rollback() # Revierte los cambios si hay un error de DB
            print(Fore.RED + f"❌ Error al agregar producto: {e} (transacción revertida)." + Style.RESET_ALL)
            return None
        finally:
            conn.close()
    return None

def obtener_todos_los_productos():
    """
    Obtiene todos los productos registrados en la base de datos.
    (Operación de lectura, no requiere transacción explícita).
    Retorna una lista de objetos (sqlite3.Row) para facilitar el acceso por nombre de columna.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos ORDER BY nombre ASC")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al obtener todos los productos: {e}" + Style.RESET_ALL)
            return []
        finally:
            conn.close()
    return []

def obtener_producto_por_id_nombre_o_categoria(termino_busqueda):
    """
    Busca productos por ID exacto, nombre (parcial) o categoría (parcial).
    (Operación de lectura, no requiere transacción explícita).
    Retorna una lista de objetos (sqlite3.Row) de productos encontrados.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            resultados = []

            # 1. Intentar buscar por ID (si es numérico)
            if termino_busqueda.isdigit():
                id_busqueda = int(termino_busqueda)
                cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?", (id_busqueda,))
                producto = cursor.fetchone()
                if producto:
                    resultados.append(producto)
            
            # 2. Buscar por nombre (parcial, insensible a mayúsculas/minúsculas)
            # Esto se ejecuta incluso si se encontró por ID para permitir búsquedas múltiples.
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE LOWER(nombre) LIKE ?",
                           (f'%{termino_busqueda.lower()}%',))
            # Añadir resultados, evitando duplicados si ya se encontró por ID
            for row in cursor.fetchall():
                if row not in resultados:
                    resultados.append(row)

            # 3. Buscar por categoría (parcial, insensible a mayúsculas/minúsculas)
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE LOWER(categoria) LIKE ?",
                           (f'%{termino_busqueda.lower()}%',))
            # Añadir resultados, evitando duplicados
            for row in cursor.fetchall():
                if row not in resultados:
                    resultados.append(row)

            return resultados
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al buscar productos: {e}" + Style.RESET_ALL)
            return []
        finally:
            conn.close()
    return []

def actualizar_producto(id_producto, nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria):
    """
    Actualiza los datos de un producto existente por su ID dentro de una transacción.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    conn = conectar_db()
    if conn:
        try:
            conn.execute("BEGIN TRANSACTION") # Inicia la transacción
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE productos
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?
                WHERE id = ?
            ''', (nuevo_nombre, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_categoria, id_producto))
            conn.commit() # Confirma los cambios
            if cursor.rowcount > 0:
                print(Fore.GREEN + f"✅ Producto con ID {id_producto} actualizado exitosamente (transacción confirmada)." + Style.RESET_ALL)
                return True
            else:
                conn.rollback() # Revierte si no se encontró el producto (aunque no es un error, mantiene la consistencia)
                print(Fore.YELLOW + f"⚠ No se encontró ningún producto con el ID {id_producto} para actualizar (transacción revertida)." + Style.RESET_ALL)
                return False
        except sqlite3.Error as e:
            conn.rollback() # Revierte los cambios si hay un error de DB
            print(Fore.RED + f"❌ Error al actualizar producto con ID {id_producto}: {e} (transacción revertida)." + Style.RESET_ALL)
            return False
        finally:
            conn.close()
    return False


def eliminar_producto(id_producto):
    """
    Elimina un producto de la base de datos por su ID dentro de una transacción.
    Retorna True si la operación fue exitosa, False en caso contrario.
    """
    conn = conectar_db()
    if conn:
        try:
            conn.execute("BEGIN TRANSACTION") # Inicia la transacción
            cursor = conn.cursor()
            # Primero, obtenemos el nombre del producto para el mensaje de confirmación
            cursor.execute("SELECT nombre FROM productos WHERE id = ?", (id_producto,))
            nombre_producto_fila = cursor.fetchone()

            if nombre_producto_fila: # Si el producto existe
                nombre_producto = nombre_producto_fila['nombre']
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conn.commit() # Confirma los cambios
                if cursor.rowcount > 0: # Se eliminó al menos un producto
                    print(Fore.GREEN + f"✅ Producto '{nombre_producto}' (ID: {id_producto}) eliminado exitosamente (transacción confirmada)." + Style.RESET_ALL)
                    return True
                else:
                    # Este caso es poco probable si nombre_producto_fila ya encontró algo
                    conn.rollback() # Revierte
                    print(Fore.YELLOW + f"⚠ No se encontró ningún producto con el ID {id_producto} para eliminar (después de la primera verificación, transacción revertida)." + Style.RESET_ALL)
                    return False
            else:
                conn.rollback() # Revierte si el producto no existe
                print(Fore.YELLOW + f"⚠ No se encontró ningún producto con el ID {id_producto} para eliminar (transacción revertida)." + Style.RESET_ALL)
                return False
        except sqlite3.Error as e:
            conn.rollback() # Revierte los cambios si hay un error de DB
            print(Fore.RED + f"❌ Error al eliminar producto: {e} (transacción revertida)." + Style.RESET_ALL)
            return False
        finally:
            conn.close()
    return False

def obtener_productos_por_cantidad_limite(limite_cantidad):
    """
    Obtiene productos cuya cantidad es igual o inferior a un límite especificado.
    (Operación de lectura, no requiere transacción explícita).
    Retorna una lista de objetos (sqlite3.Row) de productos.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC, nombre ASC", (limite_cantidad,))
            return cursor.fetchall() # Retorna todos los productos que cumplen con la condición
        except sqlite3.Error as e: # Manejo de errores de la base de datos
            # Si ocurre un error, se imprime un mensaje y se retorna una lista vacía
            print(Fore.RED + f"❌ Error al obtener productos por cantidad límite: {e}" + Style.RESET_ALL)
            return []
        finally:
            conn.close()
    return []

def obtener_categorias():
    """
    Devuelve una lista de nombres de todas las categorías ordenadas alfabéticamente.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM categorias ORDER BY nombre ASC")
            return [row['nombre'] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al obtener categorías: {e}" + Style.RESET_ALL)
            return []
        finally:
            conn.close()
    return []

def agregar_categoria(nombre_categoria):
    """
    Agrega una nueva categoría si no existe. Retorna True si se agregó o ya existía, False si hubo error.
    """
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO categorias (nombre) VALUES (?)", (nombre_categoria,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(Fore.RED + f"❌ Error al agregar categoría: {e}" + Style.RESET_ALL)
            return False
        finally:
            conn.close()
    return False

# Bloque de prueba para el módulo database.py #utilizado para pruebas unitarias y de integración
# Este bloque se ejecuta solo si el script se ejecuta directamente, no si se importa
if __name__ == "__main__":
    print(Fore.CYAN + "--- Iniciando pruebas del módulo database.py ---" + Style.RESET_ALL)
    
    # Es recomendable eliminar el archivo de la DB para una prueba limpia si se modifica el esquema
    # import os
    # if os.path.exists(ARCHIVO_DB):
    #     os.remove(ARCHIVO_DB)
    #     print(Fore.YELLOW + f"Archivo '{ARCHIVO_DB}' eliminado para una prueba limpia." + Style.RESET_ALL)

    # Asegúrate de que las tablas se creen antes de cualquier operación
    crear_tablas()# Esto asegura que las tablas existan antes de realizar pruebas

    # --- Pruebas de Usuarios ---
    print(Fore.BLUE + "\n--- Pruebas de Usuarios ---" + Style.RESET_ALL)
    agregar_usuario("usuario_prueba", "clave_prueba")
    agregar_usuario("admin", "clave_admin")
    agregar_usuario("usuario_prueba", "otra_clave") # Intento de agregar duplicado (debería revertir)

    print("\nTodos los usuarios:")
    usuarios = obtener_todos_los_usuarios()
    for user in usuarios:
        print(f"  {user['nombre_usuario']}")

    print("\nIntento de inicio de sesión:")
    if obtener_usuario("usuario_prueba", "clave_prueba"):
        print(Fore.GREEN + "  Inicio de sesión de 'usuario_prueba' exitoso." + Style.RESET_ALL)
    else:
        print(Fore.RED + "  Login de 'usuario_prueba' fallido." + Style.RESET_ALL)

    if obtener_usuario("usuario_incorrecto", "clave_incorrecta"):
        print(Fore.GREEN + "  Inicio de sesión de 'usuario_incorrecto' exitoso." + Style.RESET_ALL)
    else:
        print(Fore.RED + "  Login de 'usuario_incorrecto' fallido." + Style.RESET_ALL)
    
    print("\n--- Eliminando todos los usuarios para probar la transacción de eliminación ---")
    eliminar_todos_los_usuarios()
    print("\nUsuarios después de eliminar todos:")
    usuarios = obtener_todos_los_usuarios()
    if not usuarios:
        print(Fore.YELLOW + "  No hay usuarios." + Style.RESET_ALL)
    else:
        for user in usuarios:
            print(f"  {user['nombre_usuario']}")

    # Volver a agregar un usuario para las pruebas de productos
    agregar_usuario("user_test", "user123")

    # --- Pruebas de Productos ---
    print(Fore.BLUE + "\n--- Pruebas de Productos ---" + Style.RESET_ALL)
    # agregar_producto(nombre, descripcion, cantidad, precio, categoria)
    id1 = agregar_producto("Manzana", "Manzanas rojas frescas", 100, 2.50, "Fruta")
    id2 = agregar_producto("Leche Entera", "Leche de vaca, 1 litro", 50, 1.80, "Lácteo")
    id3 = agregar_producto("Pan Integral", "Pan de molde integral 500g", 20, 3.20, "Panaderia")
    # Simular un error (ej. si una columna no existiera o el tipo de dato fuera incorrecto)
    # database.agregar_producto("Producto Fallido", "Una descripcion", "cantidad_invalida", 10.0, "Categoria") # Esto causaría un error y rollback

    print("\nTodos los productos:")
    productos = obtener_todos_los_productos()
    for prod in productos:
        print(f"  ID: {prod['id']}, Nombre: {prod['nombre']}, Cantidad: {prod['cantidad']}, Precio: {prod['precio']:.2f}, Categoría: {prod['categoria']}")

    print(Fore.BLUE + "\n--- Pruebas de Actualización de Productos (con transacción) ---" + Style.RESET_ALL)
    # Actualizar Leche Entera (ID 2)
    if id2: # Asegurarse de que el ID exista de la adición anterior
        actualizar_producto(id2, "Leche Desnatada", "Leche descremada, 1 litro", 60, 1.90, "Lácteo")
    else:
        print(Fore.RED + "Error: ID de leche no disponible para actualizar." + Style.RESET_ALL)

    # Actualizar un producto que no existe
    actualizar_producto(9999, "Producto Falso", "Descripción", 10, 10.0, "Categoría")

    print("\nTodos los productos después de actualizar:")
    productos = obtener_todos_los_productos()
    for prod in productos:
        print(f"  ID: {prod['id']}, Nombre: {prod['nombre']}, Cantidad: {prod['cantidad']}, Precio: {prod['precio']:.2f}, Categoría: {prod['categoria']}")

    print(Fore.BLUE + "\n--- Pruebas de Eliminación de Productos (con transacción) ---" + Style.RESET_ALL)
    eliminar_producto(id3) # Eliminar "Pan Integral"
    eliminar_producto(9999) # Eliminar un producto que no existe

    print("\nTodos los productos después de eliminar:")
    productos = obtener_todos_los_productos()
    for prod in productos:
        print(f"  ID: {prod['id']}, Nombre: {prod['nombre']}, Cantidad: {prod['cantidad']}, Precio: {prod['precio']:.2f}, Categoría: {prod['categoria']}")

    print(Fore.BLUE + "\n--- Pruebas de Reporte por Cantidad ---" + Style.RESET_ALL)
    limite = 25
    productos_bajo_limite = obtener_productos_por_cantidad_limite(limite)
    print(f"\nProductos con cantidad igual o inferior a {limite}:")
    if productos_bajo_limite:
        for prod in productos_bajo_limite:
            print(f"  ID: {prod['id']}, Nombre: {prod['nombre']}, Cantidad: {prod['cantidad']}, Categoría: {prod['categoria']}")
    else:
        print(Fore.YELLOW + "  No se encontraron productos bajo ese límite." + Style.RESET_ALL)

    print(Fore.CYAN + "\n--- Pruebas del módulo database.py finalizadas ---" + Style.RESET_ALL)
