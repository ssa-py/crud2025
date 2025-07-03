# 🛒 Sistema de Gestión de Inventario (CrUd - V3.0 - SSA)

Este es un sistema de gestión de inventario basado en consola, desarrollado en Python, que permite a los usuarios administrar productos, realizar un seguimiento de stock, generar reportes y dashboards, y gestionar usuarios. Utiliza SQLite como base de datos para la persistencia de los datos y ofrece una interfaz de usuario interactiva y colorida.

## ✨ Características Principales

* **Gestión de Usuarios Segura**:
  * Registro de nuevos usuarios.
  * Inicio de sesión con credenciales.
  * Contraseñas ocultas durante la entrada (`getpass`).
  * Opción para resetear todos los usuarios (útil para pruebas).
* **Gestión Completa de Productos (CRUD)**:
  * **Agregar Productos**: Ingreso de nombre, descripción, cantidad, precio y categoría. Permite añadir nuevas categorías dinámicamente.
  * **Ver Productos**: Muestra un listado completo de todos los productos en una tabla formateada.
  * **Buscar Productos**: Permite buscar por ID, nombre o categoría (búsqueda parcial e insensible a mayúsculas/minúsculas).
  * **Modificar Productos**: Actualiza cualquier detalle de un producto existente por su ID.
  * **Eliminar Productos**: Elimina productos del inventario por su ID.
* **Reportes y Análisis**:
  * **Reporte de Stock Bajo**: Identifica productos cuya cantidad está por debajo de un límite especificado.
  * **Exportación a PDF**:
    * Exporta el inventario completo a un archivo PDF (`reportlab`).
    * Genera un dashboard visual con métricas clave y gráficos (cantidad por categoría, distribución de precios, top productos por stock) y lo exporta a PDF (`matplotlib`, `reportlab`).
  * **Dashboard en Consola**: Visualiza un resumen de métricas y gráficos ASCII directamente en la terminal.
* **Integración con WhatsApp**: Envía reportes de stock bajo directamente a través de WhatsApp (requiere un navegador web configurado).
* **Sistema de Logging**: Registra las acciones importantes de los usuarios en un archivo `log.txt`.
* **Módulo de Ayuda Interactivo**:
  * Proporciona ayuda general sobre el uso de la aplicación.
  * Permite ver los docstrings (documentación interna) de cada módulo y sus funciones principales, facilitando la comprensión del código.
* **Interfaz Amigable**: Utiliza `colorama` para una salida de consola colorida y fácil de leer, con menús interactivos y mensajes claros.

## 📦 Estructura del Proyecto

El proyecto está organizado en los siguientes módulos:

* `main.py`: El punto de entrada principal de la aplicación. Orquesta el flujo de inicio de sesión y el menú principal de gestión de inventario, interactuando con los demás módulos.
* `database.py`: Maneja todas las operaciones de la base de datos SQLite (`inventario.db`). Incluye funciones para conectar, crear tablas, y realizar operaciones CRUD sobre usuarios y productos, con manejo de transacciones para asegurar la integridad de los datos.
* `login.py`: Gestiona la lógica de autenticación de usuarios (registro e inicio de sesión). Interactúa con `database.py` para la persistencia de usuarios y utiliza `getpass` para la entrada segura de contraseñas.
* `productos.py`: Contiene la lógica de negocio para la gestión de productos. Implementa las funcionalidades CRUD para productos, generación de reportes, integración con WhatsApp, y la creación de dashboards en consola y PDF.
* `help_module.py`: Proporciona ayuda general sobre la aplicación y permite a los usuarios explorar la documentación interna (docstrings) de los módulos y sus funciones.

## ⚙️ Requisitos

* Python 3.6 o superior
* Las siguientes librerías de Python:
  * `colorama`
  * `matplotlib`
  * `reportlab`

## 🚀 Instalación

Sigue estos pasos para configurar y ejecutar la aplicación:

1. **Clonar el repositorio** (si está en GitHub):
   ```bash
   git clone [https://github.com/tu_usuario/nombre_del_repositorio.git](https://github.com/tu_usuario/nombre_del_repositorio.git)
   cd nombre_del_repositorio
   ```
   (Si no está en GitHub, simplemente descarga los archivos y navega al directorio del proyecto.)

2. **Crear un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**:
   * En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   * En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**:
   ```bash
   pip install colorama matplotlib reportlab
   ```

## ▶️ Uso

Para iniciar la aplicación, ejecuta el archivo `main.py` desde la terminal con el entorno virtual activado:

```bash
python main.py
```

Al iniciar, se te presentará un menú para:

1. **Alta de usuario**: Registra un nuevo usuario.
2. **Iniciar sesión**: Accede al sistema con tus credenciales.
3. **Resetear usuarios**: Elimina todos los usuarios registrados (¡usar con precaución!).
4. **Salir del Login**: Cierra la aplicación antes de iniciar sesión.

Una vez que inicies sesión exitosamente, accederás al menú principal de gestión de inventario, donde podrás realizar todas las operaciones CRUD, generar reportes y acceder a la ayuda.

**Sugerencia**: En cualquier momento, si deseas cancelar una operación de entrada de datos y volver al menú anterior, simplemente escribe `salir` y presiona Enter.

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor:

1. Haz un "fork" del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y asegúrate de que el código pase las pruebas.
4. Haz un "commit" de tus cambios (`git commit -m 'feat: Añadir nueva funcionalidad X'`).
5. Sube tus cambios a tu "fork" (`git push origin feature/nueva-funcionalidad`).
6. Abre un "Pull Request" describiendo tus cambios.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## ✍️ Autor

* **Alegre Sebastian** - 

## 🙏 Agradecimientos

* A la comunidad de Python por sus excelentes librerías y recursos.
* A los desarrolladores de `colorama`, `matplotlib` y `reportlab` por sus valiosas herramientas.
* Al curso de Talento Tech BA Argentina por permitirme acceder a estos conocimientos y a la Profe por la paciencia e incentivar a la mejora continua, esta version de CRUD es señal de no quedarse con lo basico!!!


