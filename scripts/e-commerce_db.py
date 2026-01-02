import mysql.connector
from faker import Faker
import random
import getpass

db_password = getpass.getpass("Introduce tu contraseña de MySQL: ")

DB_CONFIG = {
    "user": "root",
    "password": db_password,
    "host": "localhost",
    "database": "practica_backend",
}


def inicializar_conexion():
    conn = mysql.connector.connect(
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
    )
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    cursor.execute(f"USE {DB_CONFIG['database']}")
    print(f"conectado a MySQL: Base de datos {DB_CONFIG['database']}")
    return conn


def generar_tablas_mysql(conn):

    cursor = conn.cursor()

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

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100),
                precio DECIMAL(10,2),
                stock INT
            )
        """
    )

    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS detalles_pedidos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pedido_id INT,
                producto_id INT,
                cantidad INT,
                precio_unitario DECIMAL(10,2)
            )
        """
    )


class GeneradorDatos:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()
        self.fake = Faker("es_ES")

    def limpiar_datos(self):

        print("Limpiando datos antiguos...")
        self.cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 0"
        )  # desactiva el checkeo de foreign key para que mysql permita borrar las tablas que tengan esta llave.
        self.cursor.execute(
            "TRUNCATE TABLE pedidos"
        )  # borrar contenido de tabla pedidos.
        self.cursor.execute("TRUNCATE TABLE usuarios")
        self.cursor.execute("TRUNCATE TABLE productos")
        self.cursor.execute("TRUNCATE TABLE detalles_pedidos")

        self.cursor.execute(
            "SET FOREIGN_KEY_CHECKS = 1"
        )  # Vuelve a activar el checkeo foreign key

    def generar_usuarios(self):
        print("Generando usuarios...")
        usuarios_sql = "INSERT INTO usuarios (nombre, email, fecha_registro, pais) VALUES (%s, %s, %s, %s)"
        usuarios_val = []
        for _ in range(100):
            usuarios_val.append(
                (
                    self.fake.name(),
                    self.fake.email(),
                    self.fake.date_between(start_date="-2y"),
                    self.fake.country(),
                )
            )
        self.cursor.executemany(usuarios_sql, usuarios_val)
        self.conn.commit()  # Importante confirmar cambios en MySQL

    def generar_pedidos(self):
        print("Generando pedidos...")
        pedidos_sql = "INSERT INTO pedidos (usuario_id, fecha_pedido, total, estado) VALUES (%s, %s, %s, %s)"
        pedidos_val = []
        estados = ["Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado"]
        for i in range(100):
            pedidos_val.append(
                (
                    random.randint(1, 100),
                    self.fake.date_time_this_year(),
                    0,
                    random.choice(estados),
                )
            )
        self.cursor.executemany(pedidos_sql, pedidos_val)
        self.conn.commit()

    def generar_productos(self):
        print("Generando productos...")
        productos_sql = (
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        )
        productos_val = []
        for _ in range(25):
            productos_val.append(
                (
                    self.fake.catch_phrase(),
                    round(random.uniform(10.0, 100.0), 2),
                    random.randint(0, 20),
                )
            )
        self.cursor.executemany(productos_sql, productos_val)
        self.conn.commit()


if __name__ == "__main__":
    try:
        conexion = inicializar_conexion()
        generar_tablas_mysql(conexion)
        generador = GeneradorDatos(conexion)
        generador.limpiar_datos()
        generador.generar_usuarios()
        generador.generar_pedidos()
        generador.generar_productos()
        print("¡Datos generados en MySQL Local!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if "conexion" in locals() and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")


# NEW TODO Una tabla detalles, id, pedido_id -> id(pedidos), productos(1-5)
def generar_detalles_pedido():
    # PUede tener una foreign key que apunte al id de pedido.

    # Para cada pedido, asignar entre 1 y 5 productos aleatorios.
    # Calcular el total del pedido sumando (precio_producto * cantidad).
    # Actualizar la tabla 'pedidos' con ese total real.
    pass
