# SQL Lab Practice
Entorno de práctica para desarrollo centrado en **SQL** y generación de datos sintéticos con **Python**.

### Objetivo
1. Crear un script que simule la base de datos de un Comercio electrónico (e‑commerce)

2. Registrar mi progreso y construir una librería de consultas SQL resueltas
   que pueda reutilizar y revisar en el futuro.

### Stack
- **Python**: Scripting y generación de datos 
(`Faker`, `mysql-connector`).
- **MySQL**: Base de datos relacional objetivo.
- **DBeaver/Workbench**: Clientes SQL.

### Cómo usar
1. Instalar dependencias: 
`pip install -r requirements.txt`

2. Configurar la conexión a la base de datos en `e-commerce_db.py`
(usuario, password, host, nombre de la base de datos).

3. Ejecutar el generador de datos:
python3 scripts/e-commerce_db.py

### Progreso
- Añadir features a script de generación de datos.

- Documentación de preguntas de negocio y consultas SQL en la carpeta `/queries/e-commerce`