from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random
import os
from dotenv import load_dotenv


# Obtener password del .env
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"jdbc:postgresql://postgres:{DB_PASSWORD}localhost:5432/postgres"
# jdbc:postgresql://{host}[:{port}]/[{database}]

# iniciar conexion
engine = create_engine(DB_URL, echo=True)


# clase base para definir
Base = declarative_base()

# configurar sesion
Session = sessionmaker(autoflush=False, bing=engine)

session = Session()


# Definir modelos/tablas
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    register_date = Column(Date)
    country = Column(String)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
    )  # Falta foreign
    order_date = Column(Date)
    total = Column(Float)
    estado = Column(String)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    stock = Column(Integer)


class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    producto_id = Column(Integer)
    amount = Column(Integer)
    subtotal = Column(Float)


try:
    Base.metadata.create_all(engine)
    print("base de conectada y tabla craeda")
except Exception as e:
    print(f"Se ha producido un error: {e}")
