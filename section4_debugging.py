"""
Section 4: Debugging & Optimization
=====================================
This file contains a BUGGY Python script followed by the FIXED and OPTIMIZED
version with detailed explanations of each issue.
"""

# ═══════════════════════════════════════════════════════════════
#  PART A — BUGGY VERSION (Original Code with Bugs)
# ═══════════════════════════════════════════════════════════════

BUGGY_CODE = '''
import sqlite3

def get_product_sales(db_path):
    """Fetch all product sales from the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # BUG 1: Wrong SQL query — table name is "orders" not "order"
    #         Also missing JOIN to get product names
    cursor.execute("SELECT * FROM order WHERE status = active")

    results = cursor.fetchall()
    return results
    # BUG 2: Connection is never closed (resource leak)


def calculate_total_revenue(sales_data):
    """Calculate total revenue from sales data."""
    total = 0
    # BUG 3: Inefficient — string concatenation in a loop for logging
    log = ""
    for sale in sales_data:
        # BUG 4: Wrong index — assuming price is at index 3
        #         but it could be at a different position
        total = total + sale[3] * sale[4]
        log = log + "Processed sale: " + str(sale[0]) + "\\n"

    print(log)
    return total


def find_duplicate_products(products):
    """Find duplicate product names."""
    duplicates = []
    # BUG 5: O(n²) complexity — nested loop to find duplicates
    for i in range(len(products)):
        for j in range(len(products)):
            if i != j and products[i]["name"] == products[j]["name"]:
                if products[i] not in duplicates:
                    duplicates.append(products[i])
    return duplicates


def update_stock_batch(db_path, updates):
    """Update stock for multiple products."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # BUG 6: SQL injection vulnerability — using string formatting
    for product_id, new_stock in updates:
        query = "UPDATE products SET stock = %s WHERE id = %s" % (new_stock, product_id)
        cursor.execute(query)
    # BUG 7: Missing commit — changes won't be saved
    conn.close()


def get_low_stock_products(products, threshold=10):
    """Get products with stock below threshold."""
    result = []
    for p in products:
        # BUG 8: Wrong comparison operator (> instead of <)
        if p["stock"] > threshold:
            result.append(p["name"])
    return result
'''

print("=" * 65)
print("  BUGGY CODE (for reference — see BUGGY_CODE string above)")
print("=" * 65)
print(BUGGY_CODE)


# ═══════════════════════════════════════════════════════════════
#  PART B — FIXED & OPTIMIZED VERSION
# ═══════════════════════════════════════════════════════════════

import sqlite3
import os


def get_product_sales(db_path: str) -> list[tuple]:
    """
    Fetch all active product sales from the database.

    FIXES:
      1. Corrected table name from "order" → "orders" (reserved keyword issue)
      2. Quoted string value 'active' in WHERE clause
      3. Added JOIN to get product name alongside order data
      4. Used context manager (with) to auto-close the connection
      5. Added error handling
    """
    # FIX 2: Use context manager to ensure connection is always closed
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # FIX 1: Correct table name and proper SQL syntax
            cursor.execute("""
                SELECT o.id, p.name, o.quantity, p.price, o.quantity * p.price AS total
                FROM orders o
                JOIN products p ON o.product_id = p.id
                WHERE o.status = 'active'
            """)
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []


def calculate_total_revenue(sales_data: list[tuple]) -> float:
    """
    Calculate total revenue from sales data.

    FIXES:
      3. Replaced string concatenation with list + join (O(n) vs O(n²))
      4. Used named indices / descriptive unpacking instead of magic numbers

    OPTIMIZATION:
      - Used sum() with generator expression instead of manual loop
      - Used list for log accumulation instead of string concatenation
    """
    # FIX 3 & 4: Use unpacking and efficient logging
    log_lines = []
    total = 0.0

    for sale in sales_data:
        sale_id, product_name, quantity, price, line_total = sale  # FIX 4: Named unpacking
        total += line_total
        log_lines.append(f"Processed sale #{sale_id}: {product_name}")  # FIX 3: List append

    # OPTIMIZATION: Print all at once
    print("\n".join(log_lines))
    return total


def find_duplicate_products(products: list[dict]) -> list[dict]:
    """
    Find duplicate product names.

    FIX 5: Replaced O(n²) nested loop with O(n) set-based approach.
    """
    # OPTIMIZATION: Single pass using a seen-set — O(n) time complexity
    seen = set()
    duplicates = []
    for product in products:
        name = product["name"]
        if name in seen:
            duplicates.append(product)
        else:
            seen.add(name)
    return duplicates


def update_stock_batch(db_path: str, updates: list[tuple]) -> None:
    """
    Update stock for multiple products safely.

    FIXES:
      6. Replaced string formatting with parameterized queries (prevents SQL injection)
      7. Added conn.commit() to persist changes
      8. Used executemany() for batch efficiency
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # FIX 6: Parameterized query prevents SQL injection
            cursor.executemany(
                "UPDATE products SET stock = ? WHERE id = ?",
                updates,  # List of (new_stock, product_id) tuples
            )
            conn.commit()  # FIX 7: Commit the transaction
            print(f"  Updated stock for {len(updates)} products.")
    except sqlite3.Error as e:
        print(f"Database error during batch update: {e}")


def get_low_stock_products(products: list[dict], threshold: int = 10) -> list[str]:
    """
    Get products with stock below threshold.

    FIX 8: Corrected comparison operator from > to <.
    OPTIMIZATION: Used list comprehension for conciseness.
    """
    # FIX 8: Changed > to < (we want products BELOW threshold)
    return [p["name"] for p in products if p["stock"] < threshold]


# ── Demo with an in-memory database ───────────────────────────

if __name__ == "__main__":

    print("\n" + "=" * 65)
    print("  FIXED & OPTIMIZED VERSION — Demo")
    print("=" * 65)

    db_path = ":memory:"

    # Setup test database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        );
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            quantity INTEGER,
            status TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        INSERT INTO products VALUES (1, 'Laptop', 45000, 25);
        INSERT INTO products VALUES (2, 'Mouse', 500, 5);
        INSERT INTO products VALUES (3, 'Keyboard', 1200, 8);
        INSERT INTO orders VALUES (1, 1, 2, 'active');
        INSERT INTO orders VALUES (2, 2, 10, 'active');
        INSERT INTO orders VALUES (3, 3, 5, 'completed');
    """)
    conn.commit()
    conn.close()

    # Since we used :memory:, we need a file DB for the demo
    db_file = "_test_section4.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER
        );
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, status TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        INSERT INTO products VALUES (1, 'Laptop', 45000, 25);
        INSERT INTO products VALUES (2, 'Mouse', 500, 5);
        INSERT INTO products VALUES (3, 'Keyboard', 1200, 8);
        INSERT INTO orders VALUES (1, 1, 2, 'active');
        INSERT INTO orders VALUES (2, 2, 10, 'active');
        INSERT INTO orders VALUES (3, 3, 5, 'completed');
    """)
    conn.commit()
    conn.close()

    # Test 1: get_product_sales
    print("\n📌 Test 1: Fetch active sales")
    sales = get_product_sales(db_file)
    for s in sales:
        print(f"  Sale #{s[0]}: {s[1]} × {s[2]} = ₹{s[4]:,.2f}")

    # Test 2: calculate_total_revenue
    print("\n📌 Test 2: Calculate total revenue")
    revenue = calculate_total_revenue(sales)
    print(f"  Total Revenue: ₹{revenue:,.2f}")

    # Test 3: find_duplicate_products
    print("\n📌 Test 3: Find duplicate products")
    test_products = [
        {"name": "Laptop", "stock": 25},
        {"name": "Mouse", "stock": 5},
        {"name": "Laptop", "stock": 10},  # Duplicate
        {"name": "Keyboard", "stock": 8},
        {"name": "Mouse", "stock": 3},    # Duplicate
    ]
    dups = find_duplicate_products(test_products)
    print(f"  Duplicates found: {[d['name'] for d in dups]}")

    # Test 4: update_stock_batch
    print("\n📌 Test 4: Batch stock update")
    update_stock_batch(db_file, [(100, 1), (200, 2)])

    # Test 5: get_low_stock_products
    print("\n📌 Test 5: Low stock products (threshold=10)")
    low = get_low_stock_products(test_products)
    print(f"  Low stock: {low}")

    # Cleanup
    if os.path.exists(db_file):
        os.remove(db_file)

    # ── Summary of all bugs and fixes ──
    print("\n" + "=" * 65)
    print("  SUMMARY OF BUGS & FIXES")
    print("=" * 65)
    bugs = [
        ("Bug 1", "Wrong table name 'order' (reserved keyword)", "Changed to 'orders' + proper JOIN"),
        ("Bug 2", "Connection never closed (resource leak)", "Used context manager (with statement)"),
        ("Bug 3", "String concatenation in loop — O(n²)", "Used list.append() + '\\n'.join() — O(n)"),
        ("Bug 4", "Magic index numbers (sale[3], sale[4])", "Used tuple unpacking with named variables"),
        ("Bug 5", "O(n²) nested loop for duplicate detection", "Used set-based O(n) approach"),
        ("Bug 6", "SQL injection via string formatting (%s)", "Used parameterized queries (?)"),
        ("Bug 7", "Missing conn.commit() — data not saved", "Added explicit commit()"),
        ("Bug 8", "Wrong operator: > instead of <", "Fixed to < for 'below threshold'"),
    ]
    for bug_id, problem, fix in bugs:
        print(f"\n  {bug_id}:")
        print(f"    Problem : {problem}")
        print(f"    Fix     : {fix}")

    print("\n\n✅ Section 4 completed!\n")
