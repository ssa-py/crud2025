# 🛒 Sistema de Gestión de Inventario (CRUD - V3.0 - SSA)

Este es un sistema de gestión de inventario basado en consola, diseñado para facilitar la administración de productos (crear, leer, actualizar, eliminar) y la gestión de usuarios. La aplicación utiliza **SQLite** para la persistencia de los datos, proporcionando una solución robusta y fácil de usar para el control de stock.

---

## ✨ Características Principales

* **Gestión de Usuarios:**
    * Registro de nuevos usuarios con confirmación de contraseña.
    * Inicio de sesión seguro para acceder al sistema.
    * Opción de resetear todos los usuarios (ideal para entornos de prueba).
* **Gestión de Productos (CRUD Completo):**
    * **Crear:** Añade nuevos productos con **nombre**, **descripción**, **cantidad**, **precio** y **categoría**.
    * **Leer:** Visualiza todos los productos en un formato de tabla organizado.
    * **Buscar:** Encuentra productos específicos por **ID**, **nombre** (parcial) o **categoría** (parcial).
    * **Actualizar:** Modifica la información de productos existentes mediante su ID.
    * **Eliminar:** Quita productos del inventario.
* **Reportes de Stock Bajo:**
    * Genera un reporte que lista productos cuya cantidad es igual o inferior a un límite definido por el usuario.
* **Sistema de Logging:**
    * Registra las acciones clave del usuario (ej. agregar producto, iniciar sesión, salir) en un archivo `log.txt` con marca de tiempo.
* **Interfaz Amigable:**
    * Menús interactivos y mensajes claros en la consola, mejorados con colores gracias a la librería `colorama`.

---

## 🚀 Requisitos

Asegúrate de tener **Python 3.x** instalado en tu sistema.

Este proyecto requiere las siguientes librerías de Python:

* `colorama`: Para el manejo de colores en la consola.
* `getpass`: (Estándar de Python) Utilizado para la entrada segura de contraseñas.
* `sqlite3`: (Estándar de Python) Módulo para la gestión de la base de datos.

---

## 🛠️ Instalación

1.  **Descarga los archivos:**
    Asegúrate de tener todos los archivos Python (`main.py`, `productos.py`, `login.py`, `database.py`, y `ayuda.py`) en un mismo directorio.

2.  **Instala las dependencias:**
    Abre tu terminal o línea de comandos y ejecuta el siguiente comando para instalar `colorama`:

    ```bash
    pip install colorama
    ```

---

## 🖥️ Uso

1.  **Ejecuta la aplicación:**
    Navega hasta el directorio donde guardaste los archivos y ejecuta el archivo principal:

    ```bash
    python main.py
    ```

2.  **Menú de Inicio de Sesión:**
    Al iniciar la aplicación, se te presentará un menú de inicio de sesión:
    * **1. Alta de usuario:** Crea una nueva cuenta de usuario.
    * **2. Iniciar sesión:** Accede al sistema con tus credenciales.
    * **3. Resetear usuarios:** Borra todos los usuarios registrados (¡usar con precaución en entornos de producción!).
    * **4. Salir del Login:** Cierra la aplicación.

3.  **Menú Principal de Gestión de Inventario:**
    Una vez que inicies sesión con éxito, verás el menú principal con las siguientes opciones:
    * **1. Agregar nuevo producto:** Añade un nuevo artículo al inventario.
    * **2. Ver todos los productos:** Muestra una lista de todos los productos.
    * **3. Buscar producto:** Permite buscar productos por ID, nombre o categoría.
    * **4. Eliminar producto:** Borra un producto del inventario.
    * **5. Modificar producto:** Edita los detalles de un producto existente.
    * **6. Reporte de stock bajo:** Genera un informe de productos con baja cantidad.
    * **7. Salir de la aplicación:** Cierra el programa y el sistema de logging.
    * **8. Ayuda:** Accede a un menú interactivo para consultar la documentación de la aplicación, incluyendo una guía general y los `docstrings` de módulos y funciones específicas.

4.  **Uso del Menú de Ayuda (Opción 8):**
    Al seleccionar la opción "8. Ayuda" en el menú principal, se te presentará un submenú:
    * Podrás ver una **guía general de uso** de la aplicación.
    * Podrás consultar la **documentación a nivel de módulo** para `main.py`, `login.py`, `productos.py` y `database.py`.
    * Tendrás una opción **interactiva para ver la documentación de funciones específicas**: Se te pedirá que selecciones un módulo, y luego se te mostrará una lista de las funciones disponibles en ese módulo para que elijas cuál documentar. Esto facilita la exploración de la API interna del sistema.

---

## 📁 Estructura del Proyecto

* `main.py`: El punto de entrada principal de la aplicación. Orquesta los módulos y presenta el menú principal de operaciones CRUD.
* `login.py`: Maneja toda la lógica relacionada con el registro de usuarios, el inicio de sesión y el reseteo de cuentas.
* `productos.py`: Contiene las funciones para todas las operaciones de gestión de productos (agregar, ver, buscar, modificar, eliminar) y la generación de reportes de stock.
* `database.py`: Encargado de la interacción con la base de datos SQLite. Incluye funciones para conectar, crear tablas, y realizar operaciones CRUD seguras (con transacciones) tanto para usuarios como para productos.
* `ayuda.py`: Módulo que proporciona un menú interactivo para acceder a la documentación general de la aplicación, así como a los `docstrings` de módulos y funciones específicas.
* `inventario.db`: (Generado automáticamente) El archivo de la base de datos SQLite donde se almacenan todos los datos de usuarios y productos.
* `log.txt`: (Generado automáticamente) Archivo de texto que registra las acciones de los usuarios dentro de la aplicación.

---

## 📝 Notas Adicionales

* Las contraseñas de los usuarios no se encriptan; para un sistema de producción, se recomienda usar un hash seguro (ej., `hashlib`).
* La base de datos (`inventario.db`) se crea en el mismo directorio donde se ejecuta `main.py`.
* El archivo de log (`log.txt`) también se crea en el mismo directorio.
---
## 👤 Autor

Alegre Sebastian - Desarrollador principal de este sistema de gestión de inventario.
---
## 🙏 Agradecimientos

Al curso de Talento Tech BA - Argentina por despertar mas mi curiosidad por este mundo de la programacion

A la comunidad de Python por sus excelentes librerías y recursos.

A los usuarios por probar y proporcionar retroalimentación para mejorar este sistema.

Y a la profe del curso que con mucha paciencia llevo sus clases desde 0 hasta poder hacer una app funcional.

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` (si existe) para más detalles.

---


