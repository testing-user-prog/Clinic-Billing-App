from db import get_connection

def get_doctor_names():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM getdoctornames")
        return [row.Name for row in cursor.fetchall()]

def get_all_doctors():
    """Return all doctors with their fee — used by Patient Billing."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Name, fee FROM Doctor")
        return cursor.fetchall()

def update_doctor_fee(doc_name, new_fee):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC updatedoctorfee @doc_name=?, @new_fee=?", doc_name, new_fee)
        conn.commit()