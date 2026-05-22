"""
Section 5: Short Conceptual Questions
=======================================
Each question is answered with explanation AND working code examples.
"""


# ═══════════════════════════════════════════════════════════════
#  Q1: What is *args and **kwargs?
# ═══════════════════════════════════════════════════════════════

def demo_args_kwargs():
    """
    *args  — Collects positional arguments into a TUPLE.
    **kwargs — Collects keyword arguments into a DICTIONARY.

    Use cases:
      - When you don't know how many arguments a function will receive
      - When writing wrapper/decorator functions
      - When forwarding arguments to another function
    """
    def greet(*args, **kwargs):
        for name in args:
            print(f"  Hello, {name}!")
        for key, value in kwargs.items():
            print(f"  {key} = {value}")

    print("── *args and **kwargs ──")
    greet("Tvisha", "Rahul", role="Developer", company="Professional Soft-Tech")


# ═══════════════════════════════════════════════════════════════
#  Q2: @staticmethod vs @classmethod vs instance methods
# ═══════════════════════════════════════════════════════════════

def demo_method_types():
    """
    - Instance method: Takes `self`, operates on instance data.
    - @classmethod:    Takes `cls`, operates on class-level data.
                       Often used as alternative constructors.
    - @staticmethod:   Takes neither `self` nor `cls`.
                       A utility function that belongs to the class namespace.
    """
    class Employee:
        company = "Professional Soft-Tech"

        def __init__(self, name, role):
            self.name = name
            self.role = role

        # Instance method — accesses instance attributes via self
        def introduce(self):
            return f"  I am {self.name}, a {self.role} at {self.company}"

        # Class method — accesses/modifies class-level attributes via cls
        @classmethod
        def change_company(cls, new_name):
            cls.company = new_name

        # Alternative constructor using classmethod
        @classmethod
        def from_string(cls, data_string):
            name, role = data_string.split("-")
            return cls(name.strip(), role.strip())

        # Static method — no access to self or cls; pure utility
        @staticmethod
        def is_valid_role(role):
            valid_roles = ["Developer", "Designer", "Manager", "Tester"]
            return role in valid_roles

    print("── @staticmethod vs @classmethod vs instance method ──")
    emp = Employee("Tvisha", "Developer")
    print(emp.introduce())
    print(f"  Valid role? {Employee.is_valid_role('Developer')}")

    emp2 = Employee.from_string("Rahul - Manager")
    print(emp2.introduce())


# ═══════════════════════════════════════════════════════════════
#  Q3: When would you use set instead of list?
# ═══════════════════════════════════════════════════════════════

def demo_set_vs_list():
    """
    Use SET when:
      ✅ You need unique elements (automatic deduplication)
      ✅ Fast membership testing — O(1) vs O(n) for list
      ✅ Set operations: union, intersection, difference

    Use LIST when:
      ✅ Order matters (sets are unordered)
      ✅ You need duplicate values
      ✅ You need index-based access
    """
    print("── set vs list ──")

    # Deduplication
    names = ["Tvisha", "Rahul", "Tvisha", "Priya", "Rahul"]
    unique = set(names)
    print(f"  List: {names}")
    print(f"  Set (unique): {unique}")

    # Fast membership test
    large_list = list(range(100000))
    large_set = set(large_list)
    print(f"  99999 in list: {99999 in large_list}")  # O(n)
    print(f"  99999 in set:  {99999 in large_set}")   # O(1)

    # Set operations
    team_a = {"Tvisha", "Rahul", "Priya"}
    team_b = {"Priya", "Amit", "Rahul"}
    print(f"  Common members: {team_a & team_b}")
    print(f"  Only in Team A: {team_a - team_b}")


# ═══════════════════════════════════════════════════════════════
#  Q4: What is method overriding?
# ═══════════════════════════════════════════════════════════════

def demo_method_overriding():
    """
    Method overriding occurs when a child class provides its own
    implementation of a method already defined in the parent class.
    The child's version replaces the parent's version for instances
    of the child class.
    """
    class Animal:
        def speak(self):
            return "Some generic sound"

    class Dog(Animal):
        def speak(self):  # Overrides Animal.speak()
            return "Woof!"

    class Cat(Animal):
        def speak(self):  # Overrides Animal.speak()
            return "Meow!"

    print("── Method Overriding ──")
    animals = [Animal(), Dog(), Cat()]
    for animal in animals:
        print(f"  {animal.__class__.__name__}: {animal.speak()}")


# ═══════════════════════════════════════════════════════════════
#  Q5: What is super()?
# ═══════════════════════════════════════════════════════════════

def demo_super():
    """
    super() returns a proxy object that allows you to call methods
    from the parent class. It's essential for:
      - Calling the parent's __init__ in child classes
      - Extending (not replacing) parent behavior
      - Proper MRO (Method Resolution Order) in multiple inheritance
    """
    class Vehicle:
        def __init__(self, brand, speed):
            self.brand = brand
            self.speed = speed

        def info(self):
            return f"{self.brand} — {self.speed} km/h"

    class ElectricCar(Vehicle):
        def __init__(self, brand, speed, battery_kwh):
            super().__init__(brand, speed)   # Calls Vehicle.__init__
            self.battery_kwh = battery_kwh

        def info(self):
            base = super().info()            # Extends parent method
            return f"{base}, Battery: {self.battery_kwh} kWh"

    print("── super() ──")
    car = ElectricCar("Tesla", 250, 100)
    print(f"  {car.info()}")


# ═══════════════════════════════════════════════════════════════
#  Q6: How to create custom exceptions?
# ═══════════════════════════════════════════════════════════════

def demo_custom_exceptions():
    """
    Custom exceptions are created by inheriting from Exception (or
    a more specific built-in exception class). They make error
    handling more descriptive and domain-specific.
    """
    class InsufficientBalanceError(Exception):
        def __init__(self, balance, amount):
            self.balance = balance
            self.amount = amount
            super().__init__(
                f"Cannot withdraw ₹{amount}. Current balance: ₹{balance}"
            )

    class InvalidAccountError(Exception):
        pass

    def withdraw(balance, amount):
        if amount > balance:
            raise InsufficientBalanceError(balance, amount)
        return balance - amount

    print("── Custom Exceptions ──")
    try:
        withdraw(500, 1000)
    except InsufficientBalanceError as e:
        print(f"  Caught: {e}")
        print(f"  Balance: ₹{e.balance}, Attempted: ₹{e.amount}")


# ═══════════════════════════════════════════════════════════════
#  Q7: Handle API failure safely
# ═══════════════════════════════════════════════════════════════

def demo_api_failure_handling():
    """
    Best practices for handling API failures:
      1. Use try/except around the request
      2. Set timeouts to avoid hanging
      3. Implement retries with exponential backoff
      4. Check response status codes
      5. Log errors for debugging
      6. Return sensible defaults or raise custom exceptions
    """
    import time

    def fetch_data_with_retry(url, max_retries=3, timeout=5):
        """Demonstrates retry logic (simulated without actual HTTP)."""
        for attempt in range(1, max_retries + 1):
            try:
                # Simulating an API call that fails
                if attempt < 3:
                    raise ConnectionError("Server unreachable")

                # Simulating success on 3rd attempt
                return {"status": "success", "data": [1, 2, 3]}

            except ConnectionError as e:
                wait = 2 ** attempt  # Exponential backoff: 2, 4, 8...
                print(f"  Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait}s...")
                time.sleep(0.1)  # Shortened for demo

        print("  All retries exhausted. Returning default.")
        return {"status": "error", "data": []}

    print("── API Failure Handling ──")
    result = fetch_data_with_retry("https://api.example.com/data")
    print(f"  Result: {result}")


# ═══════════════════════════════════════════════════════════════
#  Q8: Encapsulation
# ═══════════════════════════════════════════════════════════════

def demo_encapsulation():
    """
    Encapsulation = Bundling data and methods together while
    restricting direct access to internal state.

    In Python:
      - _single_underscore  → Convention for "protected" (internal use)
      - __double_underscore → Name mangling (harder to access from outside)
      - @property           → Controlled access via getters/setters
    """
    class BankAccount:
        def __init__(self, owner, balance):
            self.owner = owner         # Public
            self._balance = balance    # Protected (convention)
            self.__pin = 1234          # Private (name-mangled)

        @property
        def balance(self):
            """Read-only access to balance."""
            return self._balance

        @balance.setter
        def balance(self, amount):
            if amount < 0:
                raise ValueError("Balance cannot be negative")
            self._balance = amount

        def deposit(self, amount):
            if amount <= 0:
                raise ValueError("Deposit must be positive")
            self._balance += amount

    print("── Encapsulation ──")
    acc = BankAccount("Tvisha", 10000)
    print(f"  Owner: {acc.owner}")
    print(f"  Balance (via property): ₹{acc.balance}")
    acc.deposit(5000)
    print(f"  After deposit: ₹{acc.balance}")

    try:
        acc.balance = -100
    except ValueError as e:
        print(f"  Setter guard: {e}")


# ═══════════════════════════════════════════════════════════════
#  Q9: Context Managers (with statement)
# ═══════════════════════════════════════════════════════════════

def demo_context_managers():
    """
    Context managers handle resource setup and teardown automatically.
    They implement __enter__ and __exit__ methods (or use @contextmanager).

    Common uses:
      - File handling (auto-close)
      - Database connections
      - Locks in threading
      - Temporary changes to state
    """
    import os
    from contextlib import contextmanager

    # Class-based context manager
    class Timer:
        def __enter__(self):
            import time
            self.start = time.time()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            import time
            self.elapsed = time.time() - self.start
            print(f"  Elapsed: {self.elapsed:.4f}s")
            return False  # Don't suppress exceptions

    # Decorator-based context manager
    @contextmanager
    def temp_file(filename):
        try:
            with open(filename, "w") as f:
                f.write("temporary data")
            yield filename
        finally:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"  Temp file '{filename}' cleaned up.")

    print("── Context Managers ──")

    # Timer context manager
    with Timer() as t:
        total = sum(range(1_000_000))

    # Temp file context manager
    with temp_file("_temp_demo.txt") as fname:
        print(f"  Using temp file: {fname}")


# ═══════════════════════════════════════════════════════════════
#  Q10: List Comprehension vs Loop
# ═══════════════════════════════════════════════════════════════

def demo_comprehension_vs_loop():
    """
    List Comprehension:
      ✅ More concise and Pythonic
      ✅ Generally faster (optimized at C level in CPython)
      ✅ Best for simple transformations and filtering

    Traditional Loop:
      ✅ Better for complex logic with multiple statements
      ✅ Easier to debug (can add breakpoints)
      ✅ More readable for beginners or multi-step operations
    """
    import time

    numbers = list(range(1, 1_000_001))

    # Loop approach
    start = time.time()
    squares_loop = []
    for n in numbers:
        if n % 2 == 0:
            squares_loop.append(n ** 2)
    loop_time = time.time() - start

    # List comprehension
    start = time.time()
    squares_comp = [n ** 2 for n in numbers if n % 2 == 0]
    comp_time = time.time() - start

    print("── List Comprehension vs Loop ──")
    print(f"  Loop time          : {loop_time:.4f}s")
    print(f"  Comprehension time : {comp_time:.4f}s")
    print(f"  Results match: {squares_loop == squares_comp}")
    print(f"  Comprehension is ~{loop_time/comp_time:.1f}x faster")


# ═══════════════════════════════════════════════════════════════
#  Q11: ERP System Structure with Django/Flask
# ═══════════════════════════════════════════════════════════════

def explain_erp_structure():
    """
    How I would structure an ERP system using Python and Django/Flask:

    ┌─────────────────────────────────────────────────┐
    │  ERP System Architecture (Django Example)       │
    ├─────────────────────────────────────────────────┤
    │                                                 │
    │  erp_project/                                   │
    │  ├── manage.py                                  │
    │  ├── erp_project/                               │
    │  │   ├── settings.py    # DB, auth, middleware  │
    │  │   ├── urls.py        # Root URL routing      │
    │  │   └── celery.py      # Async task queue      │
    │  ├── apps/                                      │
    │  │   ├── inventory/     # Products, stock       │
    │  │   ├── sales/         # Orders, invoices      │
    │  │   ├── purchasing/    # Purchase orders       │
    │  │   ├── accounting/    # Ledger, reports       │
    │  │   ├── hr/            # Employees, payroll    │
    │  │   └── crm/           # Customers, leads      │
    │  ├── api/               # REST API (DRF)        │
    │  └── templates/         # Frontend templates    │
    │                                                 │
    │  Key Principles:                                │
    │  • Each module = separate Django app             │
    │  • Shared models linked via ForeignKey           │
    │  • Role-based access control (RBAC)             │
    │  • Celery for background tasks (reports, emails)│
    │  • REST API for mobile/frontend integration     │
    └─────────────────────────────────────────────────┘

    For Flask: Use Blueprints instead of Django apps,
    SQLAlchemy instead of Django ORM, and Flask-RESTful for APIs.
    """
    print("── ERP System Structure ──")
    print("  Recommended: Django with modular apps (inventory, sales, hr, etc.)")
    print("  Each module is a separate Django app with its own models/views/serializers.")
    print("  Use Django REST Framework for API, Celery for async tasks.")
    print("  For Flask: Use Blueprints + SQLAlchemy + Flask-RESTful.")


# ═══════════════════════════════════════════════════════════════
#  Q12: Advantages of ORM in ERP Development
# ═══════════════════════════════════════════════════════════════

def explain_orm_advantages():
    """
    Advantages of using ORM (SQLAlchemy / Django ORM) in ERP:

    1. Database Abstraction — Switch between MySQL, PostgreSQL, SQLite
       without changing code.
    2. Security — Automatic parameterized queries prevent SQL injection.
    3. Productivity — Write Python objects instead of raw SQL.
    4. Migrations — Schema changes tracked and versioned automatically.
    5. Relationships — ForeignKey, ManyToMany handled elegantly.
    6. Query Optimization — Lazy loading, eager loading, query chaining.
    7. Maintainability — Code is more readable and testable.
    """
    print("── ORM Advantages in ERP ──")
    advantages = [
        "Database portability (switch DB engines easily)",
        "SQL injection prevention (parameterized queries)",
        "Faster development (Python objects, not raw SQL)",
        "Automatic schema migrations",
        "Clean relationship management (ForeignKey, M2M)",
        "Built-in query optimization (lazy/eager loading)",
        "Better code readability and maintainability",
    ]
    for i, adv in enumerate(advantages, 1):
        print(f"  {i}. {adv}")


# ═══════════════════════════════════════════════════════════════
#  Q13: Handling Concurrency for Stock Updates
# ═══════════════════════════════════════════════════════════════

def explain_concurrency_handling():
    """
    How to handle concurrency when multiple users update stock:

    1. Database-Level Locking:
       - SELECT ... FOR UPDATE (row-level lock in PostgreSQL)
       - Prevents race conditions at the DB level

    2. Optimistic Locking:
       - Add a `version` column to the products table
       - UPDATE ... WHERE id = ? AND version = ?
       - If version doesn't match, retry the operation

    3. Django/SQLAlchemy Solutions:
       - Django: F() expressions for atomic updates
         Product.objects.filter(id=1).update(stock=F('stock') - quantity)
       - SQLAlchemy: with_for_update() for pessimistic locking

    4. Application-Level:
       - Redis distributed locks for cross-server scenarios
       - Queue-based processing (Celery) for sequential stock updates

    5. Transaction Isolation:
       - Use SERIALIZABLE isolation level for critical operations
    """
    print("── Concurrency Handling ──")
    print("  Strategy 1: SELECT FOR UPDATE (pessimistic row locking)")
    print("  Strategy 2: Optimistic locking with version column")
    print("  Strategy 3: Django F() expressions for atomic updates")
    print("  Strategy 4: Redis distributed locks for multi-server")
    print("  Strategy 5: SERIALIZABLE transaction isolation level")
    print()
    print("  Example (Django F-expression — atomic update):")
    print("    Product.objects.filter(id=1).update(stock=F('stock') - qty)")
    print("  This generates: UPDATE products SET stock = stock - qty WHERE id = 1")
    print("  The DB handles atomicity, preventing race conditions.")


# ═══════════════════════════════════════════════════════════════
#  Run All Demos
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  Section 5: Conceptual Questions — Code Demos")
    print("=" * 60)

    demos = [
        ("Q1", "*args and **kwargs", demo_args_kwargs),
        ("Q2", "@staticmethod vs @classmethod", demo_method_types),
        ("Q3", "set vs list", demo_set_vs_list),
        ("Q4", "Method Overriding", demo_method_overriding),
        ("Q5", "super()", demo_super),
        ("Q6", "Custom Exceptions", demo_custom_exceptions),
        ("Q7", "API Failure Handling", demo_api_failure_handling),
        ("Q8", "Encapsulation", demo_encapsulation),
        ("Q9", "Context Managers", demo_context_managers),
        ("Q10", "List Comprehension vs Loop", demo_comprehension_vs_loop),
        ("Q11", "ERP Structure (Django/Flask)", explain_erp_structure),
        ("Q12", "ORM Advantages", explain_orm_advantages),
        ("Q13", "Concurrency Handling", explain_concurrency_handling),
    ]

    for qid, title, func in demos:
        print(f"\n{'─' * 60}")
        print(f"  {qid}: {title}")
        print(f"{'─' * 60}")
        func()

    print("\n\n✅ Section 5 completed!\n")
