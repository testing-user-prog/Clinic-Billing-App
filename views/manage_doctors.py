import tkinter as tk
from tkinter import ttk, messagebox
from models.doctor import get_doctor_names, update_doctor_fee

def open_manage_doctors():
    window = tk.Toplevel()
    window.title("Manage Doctors")
    window.geometry("400x300")
    window.resizable(False, False)

    # ─── TITLE ────────────────────────────────────────────────────────────────
    ttk.Label(window, text="Manage Doctors", font=("Arial", 16, "bold")).pack(pady=15)

    form_frame = tk.Frame(window)
    form_frame.pack(padx=20, pady=10)

    # ─── DOCTOR DROPDOWN ──────────────────────────────────────────────────────
    ttk.Label(form_frame, text="Select Doctor:").grid(row=0, column=0, sticky="w", pady=8)
    doctor_combo = ttk.Combobox(form_frame, width=25, state="readonly")
    doctor_combo.grid(row=0, column=1, padx=10)

    # Load doctor names from DB
    def load_doctors():
        names = get_doctor_names()
        doctor_combo["values"] = names
        

    load_doctors()

    # ─── NEW FEE INPUT ────────────────────────────────────────────────────────
    ttk.Label(form_frame, text="New Fee:").grid(row=1, column=0, sticky="w", pady=8)
    fee_spinbox = ttk.Spinbox(form_frame, from_=0, to=99999, width=25)
    fee_spinbox.grid(row=1, column=1, padx=10)

    # ─── SUBMIT BUTTON ────────────────────────────────────────────────────────
    def on_submit():
        doc_name = doctor_combo.get()
        new_fee  = fee_spinbox.get()

        if not doc_name:
            messagebox.showwarning("Warning", "Please select a doctor!", parent=window)
            return
        if not new_fee:
            messagebox.showwarning("Warning", "Please enter a fee!", parent=window)
            return
        if int(new_fee)<0:
            messagebox.showwarning("Warning!","Invalid fee entered!",parent=window)
            return 

        try:
            update_doctor_fee(doc_name, int(new_fee))
            messagebox.showinfo("Success", f"Fee updated for {doc_name}!", parent=window)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=window)

    ttk.Button(window, text="Update Fee", command=on_submit, width=20).pack(pady=15)