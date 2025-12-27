import mysql.connector
from faker import Faker
import random
import getpass

db_password = getpass.getpass("Introduce tu contraseña de MySQL: ")

DB_CONFIG = {
    "user": "dev_user",
    "password": db_password,
    "host": "localhost",
    "database": "practica_backend",
}

fake = Faker("es_ES")


def generar_datos_mysql():
    try:
        conn = mysql.connector.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")

        print(f"conectado a MySQL: Base de datos {DB_CONFIG['database']}")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                email VARCHAR(100),
                fecha_registro DATE,
                pais VARCHAR(50)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                usuario_id INT,
                fecha_pedido DATE,
                total DECIMAL(10,2),
                estado VARCHAR(20),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        """
        )

        # 3. Limpiar datos viejos (para no duplicar)
        cursor.execute("TRUNCATE TABLE pedidos")
        cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 0"
        )  # Truco necesario en MySQL para borrar tablas con relaciones
        cursor.execute("TRUNCATE TABLE usuarios")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        # 4. Insertar (Igual que antes)
        print("Generando usuarios...")
        usuarios_sql = "INSERT INTO usuarios (nombre, email, fecha_registro, pais) VALUES (%s, %s, %s, %s)"
        usuarios_val = []
        for _ in range(100):
            usuarios_val.append(
                (
                    fake.name(),
                    fake.email(),
                    fake.date_between(start_date="-2y"),
                    fake.country(),
                )
            )

        cursor.executemany(usuarios_sql, usuarios_val)
        conn.commit()  # Importante confirmar cambios en MySQL

        print("Falta generar pedidos...")

        conn.close()
        print("¡Datos generados en MySQL Local!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    generar_datos_mysql()
