# 🏕️ Campamento Management API

![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask 3.0](https://img.shields.io/badge/Flask-3.0-green.svg)
![PostgreSQL 15](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker Ready](https://img.shields.io/badge/Docker-Containerized-2496ED.svg)

API RESTful modular para la gestión integral de un campamento (usuarios, actividades y reservas), construida con **Flask**, **PostgreSQL** y **Docker Compose**, utilizando autenticación sin estado mediante **JWT**.

---

## 🏗️ Arquitectura y Patrones

* **Application Factory Pattern:** Separación limpia de configuraciones, extensiones y registros de rutas.
* **Modular Blueprints:** Rutas divididas en módulos independientes (`auth`, `activities`, `bookings`).
* **JWT & RBAC:** Control de acceso basado en roles (`admin` / `user`) con `Flask-JWT-Extended`.
* **Containerized Environment:** Entorno de desarrollo multi-contenedor aislado con Docker Compose.
* **OpenAPI Documentation:** Documentación interactiva de endpoints integrada vía Swagger (`Flasgger`).

---

## 🚀 Endpoints de la API

| Método | Endpoint | Protección | Descripción |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/v1/auth/register` | Pública | Registro de nuevos usuarios y administradores |
| **POST** | `/api/v1/auth/login` | Pública | Autenticación y generación de token JWT |
| **GET** | `/api/v1/activities` | Pública | Listado de actividades disponibles |
| **POST** | `/api/v1/activities` | Bearer JWT (Admin) | Creación de nuevas actividades |
| **GET** | `/api/v1/bookings` | Bearer JWT (User) | Listado de reservas del usuario autenticado |
| **POST** | `/api/v1/bookings` | Bearer JWT (User) | Creación de reservas para una actividad |
| **GET** | `/health` | Pública | Healthcheck del servicio |

---

## 🛠️ Despliegue Local con Docker

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Aragorn247/campamento-backend.git](https://github.com/Aragorn247/campamento-backend.git)
   cd campamento-backend