from sqlalchemy import select, func
from scripts.sql_alch_ecom import engine, Customer, Order, Product, Session
from sqlalchemy.orm import joinedload


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

        print(
            "\n--- 4.  Busca el cliente con el id=1. Luego, sin hacer una nueva query explícita, imprime la fecha de todos sus pedidos."
        )
        c = session.get(Customer, 1)
        if c:
            print(f"Fecha para los pedidos del cliente: {c.name}")
            for order in c.orders:
                print(f" {order.order_date}")

        print(
            "Encuentra todos los pedidos cuyo total sea superior a 100€. Muestra el ID del pedido y el nombre del cliente que lo hizo."
        )
        res = session.scalars(
            select(Order).where(Order.total > 100).options(joinedload(Order.customer))
        ).all()

        print(f"Pedidos encontrados: {len(res)}")
        for o in res:
            print(f"Id pedido: {o.id} | Cliente: {o.customer.name}")


if __name__ == "__main__":
    queries_execute()
