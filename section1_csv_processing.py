"""
Section 1: Core Python - CSV Processing
========================================
Reads a CSV file containing product data (name, category, price, stock),
groups products by category, and returns total stock count per category.
Includes robust error handling for missing files and invalid data.
"""

import csv
import os


def read_products(filepath: str) -> list[dict]:
    """
    Reads a CSV file and returns a list of product dictionaries.

    Args:
        filepath: Path to the CSV file.

    Returns:
        List of dicts with keys: name, category, price, stock.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or has invalid data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    products = []

    with open(filepath, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        # Validate required columns
        required_columns = {"name", "category", "price", "stock"}
        if reader.fieldnames is None:
            raise ValueError("CSV file is empty or has no headers.")

        missing_cols = required_columns - set(reader.fieldnames)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

        for line_num, row in enumerate(reader, start=2):
            try:
                product = {
                    "name": row["name"].strip(),
                    "category": row["category"].strip(),
                    "price": float(row["price"]),
                    "stock": int(row["stock"]),
                }

                # Validate data integrity
                if not product["name"]:
                    raise ValueError("Product name cannot be empty")
                if product["price"] < 0:
                    raise ValueError(f"Negative price: {product['price']}")
                if product["stock"] < 0:
                    raise ValueError(f"Negative stock: {product['stock']}")

                products.append(product)

            except (ValueError, KeyError) as e:
                print(f"  [WARNING] Skipping line {line_num}: {e}")

    if not products:
        raise ValueError("No valid product records found in the CSV file.")

    return products


def group_by_category(products: list[dict]) -> dict:
    """
    Groups products by category and calculates total stock per category.

    Args:
        products: List of product dictionaries.

    Returns:
        Dictionary with category as key and total stock count as value.
        Example: {"Electronics": 165, "Clothing": 425}
    """
    category_stock = {}
    for product in products:
        category = product["category"]
        stock = product["stock"]
        category_stock[category] = category_stock.get(category, 0) + stock

    return category_stock


def display_report(category_stock: dict) -> None:
    """Prints a formatted report of stock per category."""
    print("\n" + "=" * 50)
    print("  PRODUCT STOCK REPORT (Grouped by Category)")
    print("=" * 50)
    total = 0
    for category, stock in sorted(category_stock.items()):
        print(f"  {category:<20} : {stock:>6} units")
        total += stock
    print("-" * 50)
    print(f"  {'TOTAL':<20} : {total:>6} units")
    print("=" * 50)


# -- Main Demo --------------------------------------------------
if __name__ == "__main__":

    csv_file = "products.csv"

    # --- Test 1: Valid file ---
    print("\n[SUCCESS] Test 1: Reading valid CSV file")
    try:
        products = read_products(csv_file)
        print(f"  Loaded {len(products)} products successfully.")
        category_stock = group_by_category(products)
        display_report(category_stock)
    except (FileNotFoundError, ValueError) as e:
        print(f"  Error: {e}")

    # --- Test 2: Missing file ---
    print("\n[SUCCESS] Test 2: Handling missing file")
    try:
        read_products("nonexistent_file.csv")
    except FileNotFoundError as e:
        print(f"  Caught expected error -> {e}")

    # --- Test 3: Invalid data (created on-the-fly) ---
    print("\n[SUCCESS] Test 3: Handling invalid data in CSV")
    invalid_csv = "test_invalid.csv"
    with open(invalid_csv, "w") as f:
        f.write("name,category,price,stock\n")
        f.write("GoodProduct,Electronics,999,10\n")
        f.write("BadPrice,Electronics,not_a_number,5\n")     # invalid price
        f.write("NegativeStock,Clothing,100,-20\n")          # negative stock
        f.write(",Grocery,50,100\n")                         # empty name

    try:
        products = read_products(invalid_csv)
        result = group_by_category(products)
        print(f"  Valid products loaded: {len(products)}")
        print(f"  Category stock: {result}")
    except ValueError as e:
        print(f"   Error: {e}")
    finally:
        os.remove(invalid_csv)

    print("\n[SUCCESS] All Section 1 tests completed!\n")
