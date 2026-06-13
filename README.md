# Medicine Billing System

A desktop application for managing medicine inventory, doctor records, and generating printed pharmacy bills. Built with Python and Tkinter, backed by Microsoft SQL Server.

---

## Features

- **Medicine Billing** — Select medicines, set quantities, and print a formatted bill directly to a thermal/receipt printer
- **Stock Management** — Add new medicines or restock existing ones; optionally update prices at the same time
- **Doctor Management** — Update consultation fees for registered doctors
- **Direct Printer Support** — Bills are sent to a physical printer via the Windows GDI (`pywin32`), formatted for receipt-style output
- **Stock Validation** — Prevents billing more units than available; re-validates stock at print time
- **Stored Procedures** — All DB writes go through SQL Server stored procedures (`increasestockquantity`, `decreasestockquantity`, `increasemedicineprice`, `updatedoctorfee`)

---

## Tech Stack

- **Python** (Tkinter for GUI)
- **Microsoft SQL Server** (via `pyodbc`)
- **pywin32** (printer access on Windows)
- **Pillow** (image support)

---

## Project Structure

```
Medicine Billing/
├── main.py                  # Entry point, main window
├── db.py                    # DB connection using config.json
├── config.json              # Server, database, printer config
├── requirements.txt         # Python dependencies
├── ddl.sql                  # Table definitions
├── procedures.sql           # Stored procedures and views
├── printbill.py             # Bill printing via Windows GDI
├── models/
│   ├── medicine.py          # Medicine queries and stored proc calls
│   └── doctor.py            # Doctor queries and stored proc calls
└── views/
    ├── medicinebilling.py   # Medicine billing window
    ├── addstock.py          # Add/update stock window
    └── manage_doctors.py    # Doctor fee management window
```

---

## Setup

### Prerequisites

- Windows OS
- Python 3.x
- Microsoft SQL Server (Express or full)
- ODBC Driver 17 for SQL Server ([download here](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server))

### 1. Clone the repository

```bash
git clone https://github.com/your-username/medicine-billing.git
cd medicine-billing
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> After installing, run the pywin32 post-install script:
> ```bash
> python Scripts/pywin32_postinstall.py -install
> ```

### 4. Set up the database

Open SQL Server Management Studio (SSMS) and run the following scripts in order:

```sql
-- 1. Create the tables
-- Run: ddl.sql

-- 2. Create stored procedures and views
-- Run: procedures.sql
```

### 5. Configure the app

Edit `config.json` to match your environment:

```json
{
    "server": "YOUR_SERVER_NAME\\SQLEXPRESS",
    "database": "MedicineBilling",
    "driver": "ODBC Driver 17 for SQL Server",
    "trusted_connection": true,
    "username": "",
    "password": "",
    "printer_name": "Your Printer Name",
    "clinic_name": "Your Clinic Name"
}
```

- Set `trusted_connection` to `true` to use Windows Authentication, or `false` and fill in `username`/`password` for SQL Server auth.
- `printer_name` must exactly match the printer name in Windows Settings → Printers & Scanners.

### 6. Run the app

```bash
python main.py
```

---

## Database Schema

**Medicines**
| Column | Type |
|---|---|
| medicineid | INT IDENTITY |
| MedicineName | VARCHAR(150) UNIQUE |
| Price | DECIMAL(10,2) |
| StockQuantity | INT |

**Doctor**
| Column | Type |
|---|---|
| doctorid | INT IDENTITY |
| Name | VARCHAR(50) |
| fee | INT |

---

## Notes

- This application is Windows-only due to the use of `pywin32` for printer access.
- The printer must be installed and set as accessible in Windows before billing.
- `config.json` contains sensitive server info — add it to `.gitignore` if forking for production use.
