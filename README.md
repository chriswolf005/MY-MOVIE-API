# 🎬 MY-MOVIE-API

¡Bienvenido a **MY-MOVIE-API**! 🎉 Este es un proyecto de API RESTful para gestionar películas, construido con FastAPI y SQLAlchemy. Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre una base de datos de películas. 🍿

## 🚀 Características

- **CRUD de Películas**: Agregar, obtener, actualizar y eliminar películas. 🎥
- **Autenticación**: Seguridad básica mediante tokens JWT. 🔐
- **Base de Datos**: Integración con SQLite a través de SQLAlchemy. 💾
- **Documentación Interactiva**: Generada automáticamente con Swagger UI. 📚

## 📦 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes requisitos:

- Python 3.7 o superior 🐍
- `pip` para la gestión de paquetes 📦

## 🛠 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/chriswolf005/MY-MOVIE-API.git
   cd MY-MOVIE-API
### Crea un entorno virtual:

```bash
python -m venv venv
Activa el entorno virtual:
```
-En Windows:
```bash
venv\Scripts\activate
```
-En MacOS/Linux:
```bash
source venv/bin/activate
```
### Instala las dependencias:

```bash

pip install -r requirements.txt
```
### ⚙️ Uso
Para ejecutar la API, utiliza el siguiente comando:

bash
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Una vez que el servidor esté en funcionamiento, visita http://localhost:8000/docs para ver la documentación interactiva de la API. 🖥️

## 🗂 Endpoints
Películas
- **GET /movies: Obtener todas las películas**.
- **GET /movies/{id}: Obtener una película específica por ID**.
- **POST /movies: Agregar una nueva película**.
- **PUT /movies/{id}: Actualizar una película existente por ID**.
- **DELETE /movies/{id}: Eliminar una película por ID**.
## 🧪 Pruebas
Para ejecutar las pruebas, puedes usar:

```bash

pytest
```
## 📄 Contribuciones
**Las contribuciones son bienvenidas. Siéntete libre de abrir un issue o enviar un pull request**. 😊

## 📧 Contacto
**Si tienes preguntas o sugerencias, no dudes en contactarme**:

- **GitHub: chriswolf005**.
- **Email: c.sanchezgarcia1999@gmail.com**.
  
**¡Gracias por tu interés en MY-MOVIE-API!** 🌟
