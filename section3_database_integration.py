"""
Section 3: Database Integration
================================
Demonstrates connecting to a database using SQLAlchemy ORM,
creating tables (Products, Customers, Orders), and performing
insert, fetch, and update operations.

Uses SQLite for easy portability. To switch to MySQL/PostgreSQL,
simply change the DATABASE_URL below.
"""

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey, text
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# ── Database Configuration ─────────────────────────────────────
# SQLite (default — no server required):
DATABASE_URL = "sqlite:///erp_database.db"

# To use PostgreSQL, replace with:
# DATABASE_URL = "postgresql://username:password@localhost:5432/erp_db"
#
# To use MySQL, replace with:
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/erp_db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# ── ORM Models (Tables) ───────────────────────────────────────

class Product(Base):
    """Products table — stores product information."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', stock={self.stock})>"


class Customer(Base):
    """Customers table — stores customer information."""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(15))
    created_at = Column(DateTime, default=datetime.now)

    # Relationship: A customer can have many orders
    orders = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', email='{self.email}')>"


class Order(Base):
    """Orders table — stores order transactions."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    order_date = Column(DateTime, default=datetime.now)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product")

    def __repr__(self):
        return (f"<Order(id={self.id}, customer_id={self.customer_id}, "
                f"product_id={self.product_id}, qty={self.quantity})>")


# ── Database Operations ───────────────────────────────────────

def create_tables():
    """Creates all tables in the database."""
    Base.metadata.create_all(engine)
    print("  ✅ Tables created: products, customers, orders")


def drop_tables():
    """Drops all tables (for clean re-runs during testing)."""
    Base.metadata.drop_all(engine)


def insert_product(session, name: str, category: str, price: float, stock: int) -> Product:
    """
    Inserts a new product record into the database.

    Args:
        session: Active SQLAlchemy session.
        name: Product name.
        category: Product category.
        price: Unit price.
        stock: Available stock quantity.

    Returns:
        The inserted Product object.
    """
    product = Product(name=name, category=category, price=price, stock=stock)
    session.add(product)
    session.commit()
    return product


def insert_customer(session, name: str, email: str, phone: str = None) -> Customer:
    """Inserts a new customer record."""
    customer = Customer(name=name, email=email, phone=phone)
    session.add(customer)
    session.commit()
    return customer


def place_order(session, customer_id: int, product_id: int, quantity: int) -> Order:
    """
    Places an order and automatically updates the product stock.

    Args:
        session: Active SQLAlchemy session.
        customer_id: ID of the customer placing the order.
        product_id: ID of the product being ordered.
        quantity: Number of units to order.

    Returns:
        The created Order object.

    Raises:
        ValueError: If insufficient stock or invalid inputs.
    """
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")

    customer = session.query(Customer).filter_by(id=customer_id).first()
    if not customer:
        raise ValueError(f"Customer with ID {customer_id} not found.")

    if product.stock < quantity:
        raise ValueError(
            f"Insufficient stock for '{product.name}'. "
            f"Available: {product.stock}, Requested: {quantity}"
        )

    # Create order
    order = Order(
        customer_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        total_price=product.price * quantity,
    )
    session.add(order)

    # Update stock after order
    product.stock -= quantity

    session.commit()
    return order


def fetch_customer_orders(session, customer_id: int) -> list[Order]:
    """
    Fetches all orders for a given customer.

    Args:
        session: Active SQLAlchemy session.
        customer_id: Target customer ID.

    Returns:
        List of Order objects for the specified customer.
    """
    orders = (
        session.query(Order)
        .filter(Order.customer_id == customer_id)
        .all()
    )
    return orders


def update_stock(session, product_id: int, new_stock: int) -> None:
    """
    Updates the stock for a given product.

    Args:
        session: Active SQLAlchemy session.
        product_id: Target product ID.
        new_stock: New stock value (must be >= 0).
    """
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise ValueError(f"Product with ID {product_id} not found.")
    if new_stock < 0:
        raise ValueError("Stock cannot be negative.")
    product.stock = new_stock
    session.commit()


# ── Main Demo ──────────────────────────────────────────────────

if __name__ == "__main__":
    import os

    # Clean start for demo
    db_file = "erp_database.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    print("\n" + "=" * 60)
    print("  Section 3: Database Integration Demo")
    print("=" * 60)

    # Step 1: Create tables
    print("\n📌 Step 1: Creating database tables...")
    create_tables()

    session = SessionLocal()

    try:
        # Step 2: Insert products
        print("\n📌 Step 2: Inserting products...")
        p1 = insert_product(session, "Laptop", "Electronics", 45000, 25)
        p2 = insert_product(session, "Smartphone", "Electronics", 15000, 40)
        p3 = insert_product(session, "T-Shirt", "Clothing", 800, 200)
        p4 = insert_product(session, "Office Chair", "Furniture", 8000, 30)
        print(f"  Inserted: {p1.name}, {p2.name}, {p3.name}, {p4.name}")

        # Step 3: Insert customers
        print("\n📌 Step 3: Inserting customers...")
        c1 = insert_customer(session, "Rahul Sharma", "rahul@example.com", "9876543210")
        c2 = insert_customer(session, "Priya Patel", "priya@example.com", "9123456789")
        print(f"  Inserted: {c1.name}, {c2.name}")

        # Step 4: Place orders
        print("\n📌 Step 4: Placing orders...")
        o1 = place_order(session, c1.id, p1.id, 2)  # Rahul buys 2 Laptops
        print(f"  Order #{o1.id}: {c1.name} → 2x {p1.name} = ₹{o1.total_price:,.2f}")

        o2 = place_order(session, c1.id, p3.id, 5)  # Rahul buys 5 T-Shirts
        print(f"  Order #{o2.id}: {c1.name} → 5x {p3.name} = ₹{o2.total_price:,.2f}")

        o3 = place_order(session, c2.id, p2.id, 3)  # Priya buys 3 Smartphones
        print(f"  Order #{o3.id}: {c2.name} → 3x {p2.name} = ₹{o3.total_price:,.2f}")

        # Step 5: Fetch orders for a customer
        print(f"\n📌 Step 5: Fetching all orders for '{c1.name}'...")
        rahul_orders = fetch_customer_orders(session, c1.id)
        for order in rahul_orders:
            print(f"  Order #{order.id}: Product={order.product.name}, "
                  f"Qty={order.quantity}, Total=₹{order.total_price:,.2f}")

        # Step 6: Check updated stock
        print("\n📌 Step 6: Verifying stock after orders...")
        for product in session.query(Product).all():
            print(f"  {product.name:<20} → Stock: {product.stock}")

        # Step 7: Manual stock update
        print("\n📌 Step 7: Manually updating Laptop stock to 50...")
        update_stock(session, p1.id, 50)
        refreshed = session.query(Product).filter_by(id=p1.id).first()
        print(f"  {refreshed.name} stock is now: {refreshed.stock}")

    finally:
        session.close()

    # Cleanup demo database
    if os.path.exists(db_file):
        os.remove(db_file)

    print("\n✅ Section 3 completed!\n")
