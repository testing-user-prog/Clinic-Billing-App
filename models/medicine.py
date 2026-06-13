from db import get_connection

def get_all_medicines():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT medicineid, MedicineName, Price, StockQuantity FROM Medicines")
        return cursor.fetchall()

def get_low_stock_medicines(threshold=10):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MedicineName, Price, StockQuantity FROM Medicines WHERE StockQuantity < ? ORDER BY StockQuantity ASC",
            threshold
        )
        return cursor.fetchall()

def get_medicine_by_name(name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT medicineid, MedicineName, Price, StockQuantity FROM Medicines WHERE MedicineName = ?", name)
        return cursor.fetchone()

def add_medicine(name, price, stock=1):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Medicines (MedicineName, Price, StockQuantity) VALUES (?, ?, ?)",
            name, price, stock
        )
        conn.commit()

def increase_medicine_price(medicineid, new_price):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC increasemedicineprice @medicineid=?, @new_price=?", medicineid, new_price)
        conn.commit()

def increase_stock(medicineid, quantity):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC increasestockquantity @medicineid=?, @quantity=?", medicineid, quantity)
        conn.commit()

def decrease_stock(medicineid, quantity):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC decreasestockquantity @medicineid=?, @quantity=?", medicineid, quantity)
        conn.commit()