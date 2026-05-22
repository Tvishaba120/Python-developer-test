# Python Developer Practical Test — Tvisha Mori

## Project Structure

```
python_test/
├── products.csv                      # Sample product data
├── section1_csv_processing.py        # Section 1: Core Python (CSV)
├── section2_erp_module.py            # Section 2: ERP Module Simulation
├── section3_database_integration.py  # Section 3: Database Integration
├── section4_debugging.py             # Section 4: Debugging & Optimization
├── section5_conceptual_answers.py    # Section 5: Conceptual Questions
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Setup & Run

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run each section
python section1_csv_processing.py
python section2_erp_module.py
python section3_database_integration.py
python section4_debugging.py
python section5_conceptual_answers.py
```

## Section Overview

| Section | Topic | Key Concepts |
|---------|-------|-------------|
| 1 | CSV Processing | `csv.DictReader`, error handling, data grouping |
| 2 | ERP Module | OOP, dataclasses, sales tracking, reporting |
| 3 | Database Integration | SQLAlchemy ORM, SQLite, CRUD, relationships |
| 4 | Debugging | 8 bug fixes, SQL injection, optimization |
| 5 | Conceptual Questions | 13 answers with working code examples |

## Technologies Used

- **Python 3.12+**
- **SQLAlchemy** — ORM for database integration
- **SQLite** — Portable database (no server needed)
- **csv** — Standard library for CSV processing
