from sqlalchemy import create_engine, Integer, String, DECIMAL, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from sqlalchemy.engine import URL
from faker import Faker
from datetime import date
import random
import os
from dotenv import load_dotenv
from typing import List
import getpass

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")
if not DB_PASSWORD:
    DB_PASSWORD = getpass.getpass("Password DB: ...")
DB_URL = f"postgresql+psycopg2://postgres:{DB_PASSWORD}@localhost:5432/postgres"

engine = create_engine(DB_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    register_date: Mapped[date] = mapped_column()
    country: Mapped[str] = mapped_column(String(50))
    orders: Mapped[List["Order"]] = relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    stock: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    order_date: Mapped[date] = mapped_column()
    total: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0)
    state: Mapped[str] = mapped_column(String(20))
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    details: Mapped[List["OrderDetail"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderDetail(Base):
    __tablename__ = "order_details"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    amount: Mapped[int] = mapped_column(Integer)
    subtotal: Mapped[float] = mapped_column(DECIMAL(10, 2))

    order: Mapped["Order"] = relationship(back_populates="details")
    product: Mapped["Product"] = relationship()


class DataGenerator:
    def __init__(self, session: Session):
        self.session = session
        self.fake = Faker("es_ES")

    def clear_tables(self):
        print("Recreando tablas...")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def customers_generator(self):
        print("Generando clientes ...")
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

    def products_generator(self):
        print("Generando productos ...")

        products = []
        for _ in range(25):
            p = Product(
                name=self.fake.catch_phrase(),
                price=round(random.uniform(10.0, 100.0), 2),
                stock=random.randint(0, 20),
            )
            products.append(p)
        self.session.add_all(products)
        self.session.commit()

    def orders_generator(self):
        print("Generando pedidos...")
        states = ["Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado"]
        orders = []
        customers = self.session.scalars(select(Customer)).all()

        for _ in range(100):
            customer_random = random.choice(customers)
            o = Order(
                customer=customer_random,
                order_date=self.fake.date_between(start_date="-2y"),
                total=0,
                state=random.choice(states),
            )
            orders.append(o)
        self.session.add_all(orders)
        self.session.commit()

    def details_generator(self):
        print("Generando detalles...")
        products = self.session.scalars(select(Product)).all()
        orders = self.session.scalars(select(Order)).all()

        details = []

        total_orders = {o: 0.0 for o in orders}

        for _ in range(100):
            prod = random.choice(products)
            order = random.choice(orders)
            amount = random.randint(1, 5)
            price_float = float(prod.price)
            subtotal = round(price_float * amount, 2)

            d = OrderDetail(order=order, product=prod, amount=amount, subtotal=subtotal)
            details.append(d)

            total_orders[order] += subtotal

        self.session.add_all(details)

        for order, total in total_orders.items():
            if total > 0:
                order.total = round(total, 2)

        self.session.commit()


if __name__ == "__main__":
    try:
        with Session(engine) as session:
            gen = DataGenerator(session)

            gen.clear_tables()
            gen.customers_generator()
            gen.products_generator()
            gen.orders_generator()
            gen.details_generator()

            print("\n¡Proceso completado con éxito!")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
