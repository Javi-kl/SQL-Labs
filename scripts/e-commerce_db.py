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
            CREATE TABLE IF NOT EXISTS clientes (
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
                cliente_id INT,
                fecha_pedido DATE,
                total DECIMAL(10,2),
                estado VARCHAR(20),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
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
                subtotal DECIMAL(10,2),
                FOREIGN KEY (producto_id) REFERENCES productos(id),
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
            )
        """
    )


class GeneradorDatos:
    def __init__(self, conn) -> None:
        self.conn = conn
        self.cursor = conn.cursor()
        self.fake = Faker("es_ES")

    def limpiar_tablas(self):
        print("Limpiando datos antiguos...")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        self.cursor.execute("DROP TABLE IF EXISTS detalles_pedidos")
        self.cursor.execute("DROP TABLE IF EXISTS pedidos")
        self.cursor.execute("DROP TABLE IF EXISTS clientes")
        self.cursor.execute("DROP TABLE IF EXISTS productos")
        self.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    def generar_clientes(self):
        print("Generando clientes...")
        usuarios_sql = "INSERT INTO clientes (nombre, email, fecha_registro, pais) VALUES (%s, %s, %s, %s)"
        usuarios_val = []
        for _ in range(1, 101):
            usuarios_val.append(
                (
                    self.fake.name(),
                    self.fake.email(),
                    self.fake.date_between(start_date="-2y"),
                    self.fake.country(),
                )
            )
        self.cursor.executemany(usuarios_sql, usuarios_val)
        self.conn.commit()

    def generar_pedidos(self):
        print("Generando pedidos...")
        pedidos_sql = "INSERT INTO pedidos (cliente_id, fecha_pedido, total, estado) VALUES (%s, %s, %s, %s)"
        pedidos_val = []
        estados = ["Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado"]
        for _ in range(1, 101):
            pedidos_val.append(
                (
                    random.randint(1, 100),
                    self.fake.date_between(start_date="-2y"),
                    0,
                    random.choice(estados),
                )
            )
        self.cursor.executemany(pedidos_sql, pedidos_val)
        self.conn.commit()

    def generar_detalles_pedidos(self):
        print("Generando detalles de pedidos...")
        self.cursor.execute("SELECT id, precio FROM productos")
        precios_productos = dict(self.cursor.fetchall())
        detalles_p_sql = "INSERT INTO detalles_pedidos (pedido_id, producto_id, cantidad, subtotal) VALUES (%s, %s, %s, %s)"
        detalles_p_val = []
        for _ in range(1, 101):
            prod_id = random.randint(1, 25)
            cantidad = random.randint(1, 5)
            precio_unitario = precios_productos.get(prod_id)
            subtotal = round(precio_unitario * cantidad, 2)
            detalles_p_val.append(
                (  # Nota: Asignamos detalles a pedidos al azar (random 1-100).
                    # Esto provoca que algunos pedidos tengan varios productos y otros NINGUNO.
                    # Es intencional para simular pedidos con distintos productos.
                    random.randint(1, 100),
                    prod_id,
                    cantidad,
                    subtotal,
                )
            )

        self.cursor.executemany(detalles_p_sql, detalles_p_val)
        self.conn.commit()

        self.actualizar_totales_pedidos()

    def generar_productos(self):
        print("Generando productos...")
        productos_sql = (
            "INSERT INTO productos (nombre, precio, stock) VALUES (%s, %s, %s)"
        )
        productos_val = []
        for _ in range(1, 26):
            productos_val.append(
                (
                    self.fake.catch_phrase(),
                    round(random.uniform(10.0, 100.0), 2),
                    random.randint(0, 20),
                )
            )
        self.cursor.executemany(productos_sql, productos_val)
        self.conn.commit()

    def actualizar_totales_pedidos(self):
        print("Actualizando totales en tabla pedidos...")
        self.cursor.execute(
            """
            SELECT pedido_id, SUM(subtotal)
            FROM detalles_pedidos
            GROUP BY pedido_id
            """
        )
        resultados = self.cursor.fetchall()

        actualizar_tabla = "UPDATE pedidos SET total = %s WHERE id = %s"
        for pedido_id, suma_total in resultados:
            self.cursor.execute(actualizar_tabla, (suma_total, pedido_id))

        self.conn.commit()
        print(f"Actualizados {len(resultados)} correctamente.")


if __name__ == "__main__":
    try:
        conexion = inicializar_conexion()
        generador = GeneradorDatos(conexion)
        generador.limpiar_tablas()
        generar_tablas_mysql(conexion)
        generador.generar_clientes()
        generador.generar_pedidos()
        generador.generar_productos()
        generador.generar_detalles_pedidos()
        print("¡Datos generados en MySQL Local!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if "conexion" in locals() and conexion.is_connected():
            conexion.close()
            print("Conexión cerrada.")
