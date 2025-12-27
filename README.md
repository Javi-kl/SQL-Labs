# SQL Lab Practice
Entorno de práctica para desarrollo centrado en **SQL** y generación de datos sintéticos con **Python**.

### Objetivo
1. Crear scripts que simulen bases de datos de distintos dominios:
   - Comercio electrónico (e‑commerce)
   - Recursos humanos (HR)
   - Redes sociales / contenido

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

2. Configurar la conexión a la base de datos en `scripts/nombre_archivo.py`
(usuario, password, host, nombre de la base de datos).

3. Ejecutar el generador de datos:
python3 scripts/nombre_archivo.py

### Progreso
- Scripts de generación de datos para distintos tipos de negocio (en evolución).

- Documentación de preguntas de negocio y consultas SQL en la carpeta `/sessions/tipo_negocio`