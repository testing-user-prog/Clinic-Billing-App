import tkinter as tk
from tkinter import ttk
import pyodbc
from db import get_connection
from views.manage_doctors import open_manage_doctors
from views.addstock import open_update_medicines
from views.medicinebilling import open_medicine_billing
from views.patientbilling import open_patient_billing
from views.checkinventory import open_check_inventory
# ─── TEST CONNECTION ──────────────────────────────────────────────────────────
try:
    conn = get_connection()
    print("Connected successfully!")
    conn.close()
except pyodbc.Error as e:
    print(f"Connection failed: {e}")

# ─── MAIN WINDOW ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Medicine Billing System")
root.geometry("500x500")
root.resizable(False, False)

# ─── FRAMES ───────────────────────────────────────────────────────────────────
top_frame    = tk.Frame(root, bg="white")
bottom_frame = tk.Frame(root, bg="white")

top_frame.pack(fill="x", padx=10, pady=20)
bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

# ─── TITLE ────────────────────────────────────────────────────────────────────
ttk.Label(top_frame, text="Medicine Billing System", font=("Arial", 22, "bold")).pack()
ttk.Label(top_frame, text="Select an option to continue", font=("Arial", 10)).pack(pady=5)

# ─── BUTTONS ──────────────────────────────────────────────────────────────────
btn_style = {"width": 25, "padding": 10}

ttk.Button(bottom_frame, text="Manage Doctors",    command=open_manage_doctors,                              **btn_style).pack(pady=8)
ttk.Button(bottom_frame, text="Do Patient Billing",command=open_patient_billing,                             **btn_style).pack(pady=8)
ttk.Button(bottom_frame, text="Do Medicine Billing",command=open_medicine_billing,    **btn_style).pack(pady=8)
ttk.Button(bottom_frame, text="Add Stock",         command=open_update_medicines,               **btn_style).pack(pady=8)
ttk.Button(bottom_frame, text="Check Inventory",   command=open_check_inventory,                **btn_style).pack(pady=8)

# ─── START ────────────────────────────────────────────────────────────────────
root.mainloop()