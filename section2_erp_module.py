"""
Section 2: ERP Module Simulation
=================================
A simple ERP-like module that allows adding products, processing sales,
updating stock, and generating summary reports.
Designed with modular classes and functions.
"""

from dataclasses import dataclass, field
from datetime import datetime


# ── Data Models ────────────────────────────────────────────────

@dataclass
class Product:
    """Represents a product in the ERP system."""
    product_id: int
    name: str
    category: str
    price: float
    stock: int


@dataclass
class SaleRecord:
    """Represents a single sale transaction."""
    sale_id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    timestamp: str


# ── Custom Exceptions ──────────────────────────────────────────

class ProductNotFoundError(Exception):
    """Raised when a product is not found in the system."""
    pass


class InsufficientStockError(Exception):
    """Raised when there isn't enough stock for a sale."""
    pass


class DuplicateProductError(Exception):
    """Raised when trying to add a product that already exists."""
    pass


# ── ERP System ─────────────────────────────────────────────────

class ERPSystem:
    """
    A simple ERP system for managing products and sales.

    Attributes:
        products: Dictionary mapping product_id to Product objects.
        sales: List of SaleRecord objects.
    """

    def __init__(self):
        self.products: dict[int, Product] = {}
        self.sales: list[SaleRecord] = []
        self._next_product_id: int = 1
        self._next_sale_id: int = 1

    # ── Product Management ─────────────────────────────────

    def add_product(self, name: str, category: str, price: float, stock: int) -> Product:
        """
        Adds a new product to the system.

        Args:
            name: Product name.
            category: Product category.
            price: Unit price (must be > 0).
            stock: Initial stock quantity (must be >= 0).

        Returns:
            The newly created Product object.

        Raises:
            ValueError: If price or stock values are invalid.
            DuplicateProductError: If a product with the same name already exists.
        """
        if price <= 0:
            raise ValueError(f"Price must be positive, got: {price}")
        if stock < 0:
            raise ValueError(f"Stock cannot be negative, got: {stock}")

        # Check for duplicate names
        for existing in self.products.values():
            if existing.name.lower() == name.lower():
                raise DuplicateProductError(f"Product '{name}' already exists (ID: {existing.product_id})")

        product = Product(
            product_id=self._next_product_id,
            name=name,
            category=category,
            price=price,
            stock=stock,
        )
        self.products[product.product_id] = product
        self._next_product_id += 1
        return product

    def get_product(self, product_id: int) -> Product:
        """Fetches a product by ID. Raises ProductNotFoundError if not found."""
        if product_id not in self.products:
            raise ProductNotFoundError(f"Product with ID {product_id} not found.")
        return self.products[product_id]

    def update_stock(self, product_id: int, new_stock: int) -> None:
        """Manually updates the stock of a product."""
        product = self.get_product(product_id)
        if new_stock < 0:
            raise ValueError("Stock cannot be negative.")
        product.stock = new_stock

    # ── Sales Management ───────────────────────────────────

    def make_sale(self, product_id: int, quantity: int) -> SaleRecord:
        """
        Processes a sale: deducts stock and records the transaction.

        Args:
            product_id: ID of the product to sell.
            quantity: Number of units to sell (must be > 0).

        Returns:
            The SaleRecord for this transaction.

        Raises:
            ProductNotFoundError: If the product doesn't exist.
            InsufficientStockError: If not enough stock is available.
            ValueError: If quantity is not positive.
        """
        if quantity <= 0:
            raise ValueError(f"Sale quantity must be positive, got: {quantity}")

        product = self.get_product(product_id)

        if product.stock < quantity:
            raise InsufficientStockError(
                f"Not enough stock for '{product.name}'. "
                f"Available: {product.stock}, Requested: {quantity}"
            )

        # Deduct stock
        product.stock -= quantity

        # Record the sale
        sale = SaleRecord(
            sale_id=self._next_sale_id,
            product_id=product_id,
            product_name=product.name,
            quantity=quantity,
            unit_price=product.price,
            total_amount=product.price * quantity,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.sales.append(sale)
        self._next_sale_id += 1
        return sale

    # ── Reporting ──────────────────────────────────────────

    def generate_report(self) -> dict:
        """
        Generates a summary report of total sales and remaining stock.

        Returns:
            Dictionary with:
              - total_sales_count: Number of sale transactions
              - total_revenue: Total sales revenue
              - products: List of product summaries (name, stock, etc.)
              - sales_by_product: Revenue breakdown per product
        """
        total_revenue = sum(sale.total_amount for sale in self.sales)
        total_units_sold = sum(sale.quantity for sale in self.sales)

        # Sales breakdown per product
        sales_by_product = {}
        for sale in self.sales:
            if sale.product_name not in sales_by_product:
                sales_by_product[sale.product_name] = {"units_sold": 0, "revenue": 0.0}
            sales_by_product[sale.product_name]["units_sold"] += sale.quantity
            sales_by_product[sale.product_name]["revenue"] += sale.total_amount

        return {
            "total_sales_count": len(self.sales),
            "total_units_sold": total_units_sold,
            "total_revenue": total_revenue,
            "remaining_stock": {
                p.name: p.stock for p in self.products.values()
            },
            "sales_by_product": sales_by_product,
        }

    def print_report(self) -> None:
        """Prints a formatted summary report."""
        report = self.generate_report()

        print("\n" + "=" * 60)
        print("  📊 ERP SYSTEM — SALES & STOCK REPORT")
        print("=" * 60)

        print(f"\n  Total Transactions : {report['total_sales_count']}")
        print(f"  Total Units Sold   : {report['total_units_sold']}")
        print(f"  Total Revenue      : ₹{report['total_revenue']:,.2f}")

        print("\n  ── Sales Breakdown by Product ──")
        for product_name, data in report["sales_by_product"].items():
            print(f"    {product_name:<20} | {data['units_sold']:>4} units | ₹{data['revenue']:>10,.2f}")

        print("\n  ── Remaining Stock ──")
        for product_name, stock in report["remaining_stock"].items():
            status = "✅" if stock > 0 else "❌ OUT OF STOCK"
            print(f"    {product_name:<20} | {stock:>4} units  {status if stock == 0 else ''}")

        print("\n" + "=" * 60)


# ── Main Demo ──────────────────────────────────────────────────

if __name__ == "__main__":

    erp = ERPSystem()

    # Add products
    print("✅ Adding products...")
    erp.add_product("Laptop", "Electronics", 45000, 25)
    erp.add_product("Smartphone", "Electronics", 15000, 40)
    erp.add_product("T-Shirt", "Clothing", 800, 200)
    erp.add_product("Office Chair", "Furniture", 8000, 30)
    erp.add_product("Rice (10kg)", "Grocery", 600, 500)
    print(f"  Added {len(erp.products)} products.")

    # Make some sales
    print("\n✅ Processing sales...")
    sale1 = erp.make_sale(1, 5)   # 5 Laptops
    print(f"  Sale #{sale1.sale_id}: {sale1.quantity}x {sale1.product_name} = ₹{sale1.total_amount:,.2f}")

    sale2 = erp.make_sale(2, 10)  # 10 Smartphones
    print(f"  Sale #{sale2.sale_id}: {sale2.quantity}x {sale2.product_name} = ₹{sale2.total_amount:,.2f}")

    sale3 = erp.make_sale(3, 50)  # 50 T-Shirts
    print(f"  Sale #{sale3.sale_id}: {sale3.quantity}x {sale3.product_name} = ₹{sale3.total_amount:,.2f}")

    sale4 = erp.make_sale(4, 3)   # 3 Office Chairs
    print(f"  Sale #{sale4.sale_id}: {sale4.quantity}x {sale4.product_name} = ₹{sale4.total_amount:,.2f}")

    sale5 = erp.make_sale(5, 100) # 100 Rice bags
    print(f"  Sale #{sale5.sale_id}: {sale5.quantity}x {sale5.product_name} = ₹{sale5.total_amount:,.2f}")

    # Test insufficient stock
    print("\n✅ Testing error handling...")
    try:
        erp.make_sale(1, 999)
    except InsufficientStockError as e:
        print(f"  Caught expected error → {e}")

    try:
        erp.make_sale(99, 1)
    except ProductNotFoundError as e:
        print(f"  Caught expected error → {e}")

    # Generate report
    erp.print_report()
    print("\n✅ Section 2 completed!\n")
