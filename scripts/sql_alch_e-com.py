from sqlalchemy import create_engine, Integer, String, DECIMAL, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from sqlalchemy.engine import URL
from faker import Faker
from datetime import date
import random
import os
from dotenv import load_dotenv


load_dotenv()
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD}localhost:5432/postgres"

engine = create_engine(DB_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    register_date: Mapped[date] = mapped_column()
    country: Mapped[str] = mapped_column(String(50))


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[String] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    stock: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    order_date: Mapped[date] = mapped_column()
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0)
    estado: Mapped[str] = mapped_column(String(20))
    cliente: Mapped["Customer"] = relationship()


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    amount: Mapped[int] = mapped_column(Integer)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10, 2))

    order: Mapped["Order"] = relationship()
    product: Mapped["Product"] = relationship()


class Data_generator:
    def __init__(self, session, Session):
        self.session = session
        self.fake = Faker("es_ES")

    def clear_tables(self):
        print("Recreando tablas...")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def custormers_generator(self):
        customers = []
        for _ in range(25):
            c = Customer(
                name=self.fake.name(),
                email=self.fake.email(),
                register_date=self.fake.date_between(start_date="-2y"),
                country=self.fake.country(),
            )
            customers.append(c)
        self.session.add_all(customers)
        self.session.commit()
