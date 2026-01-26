from sqlalchemy import select, func
from scripts.sql_alch_ecom import engine, Customer, Order, Product, Session


def queries_execute():
    with Session(engine) as session:
        print("\n--- 1. Clientes de un país ---")
        res = session.scalars(select(Customer).where(Customer.country == "India")).all()
        for customer in res:
            print(customer.name)

        print("\n--- 2. Productos caros ---")
        res = session.scalars(select(Product).where(Product.price > 50)).all()
        for p in res:
            print(p.name, p.price)

        print("\n--- 3. Cuántos pedidos hay en estado 'Pendiente'")
        res = session.scalar(
            select(func.count()).select_from(Order).where(Order.state == "Pendiente")
        )
        print(f"Pedidos en 'Pendiente': {res}")


if __name__ == "__main__":
    queries_execute()
