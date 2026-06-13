import tkinter as tk
from tkinter import ttk, messagebox
from models.medicine import get_all_medicines, decrease_stock
from models.doctor import get_all_doctors
from printbill import print_patient_bill


def open_patient_billing():
    window = tk.Toplevel()
    window.title("Patient Billing")
    window.geometry("620x680")
    window.resizable(False, False)

    ttk.Label(window, text="Patient Billing", font=("Arial", 16, "bold")).pack(pady=12)

    top_frame = tk.Frame(window)
    top_frame.pack(padx=20, fill="x")

    # ── Patient Name ──────────────────────────────────────────────────────────
    ttk.Label(top_frame, text="Patient Name:").grid(row=0, column=0, sticky="w", pady=6)
    patient_name_entry = ttk.Entry(top_frame, width=35)
    patient_name_entry.grid(row=0, column=1, padx=10, pady=6)

    # ── Doctor ComboBox (searchable — same pattern as Medicine ComboBox) ──────
    ttk.Label(top_frame, text="Doctor:").grid(row=1, column=0, sticky="w", pady=6)
    doctor_var = tk.StringVar()
    doctor_combo = ttk.Combobox(top_frame, textvariable=doctor_var, width=28)
    doctor_combo.grid(row=1, column=1, padx=10, pady=6)

    doctor_charges_label = ttk.Label(top_frame, text="Charges: —")
    doctor_charges_label.grid(row=1, column=2, sticky="w", padx=(10, 0))

    all_doctors = {}

    def load_doctors():
        nonlocal all_doctors
        try:
            doctors = get_all_doctors()
            all_doctors = {d.Name: d for d in doctors}
            doctor_combo["values"] = list(all_doctors.keys())
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load doctors:\n{e}", parent=window)

    load_doctors()

    def on_doctor_selected(event=None):
        name = doctor_var.get()
        if name in all_doctors:
            fee = all_doctors[name].fee
            doctor_charges_label.config(text=f"Charges: Rs. {fee:.2f}")
            update_total()
        else:
            doctor_charges_label.config(text="Charges: —")
            update_total()

    def on_doctor_keyrelease(event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Shift_L", "Shift_R",
                            "Control_L", "Control_R", "Return", "Escape"):
            return
        typed = doctor_var.get().strip()
        all_names = list(all_doctors.keys())
        filtered = [n for n in all_names if typed.lower() in n.lower()] if typed else all_names
        doctor_combo["values"] = filtered
        on_doctor_selected()

    doctor_combo.bind("<<ComboboxSelected>>", on_doctor_selected)
    doctor_combo.bind("<KeyRelease>", on_doctor_keyrelease)

    # ── Medicine ComboBox + Quantity (identical to medicinebilling.py) ────────
    ttk.Label(top_frame, text="Medicine:").grid(row=2, column=0, sticky="w", pady=6)
    medicine_var = tk.StringVar()
    medicine_combo = ttk.Combobox(top_frame, textvariable=medicine_var, width=28)
    medicine_combo.grid(row=2, column=1, padx=10, pady=6)

    ttk.Label(top_frame, text="Quantity:").grid(row=2, column=2, sticky="w", padx=(10, 0))
    quantity_spinbox = ttk.Spinbox(top_frame, from_=1, to=1, width=8)
    quantity_spinbox.grid(row=2, column=3, padx=5)

    all_medicines = {}

    def load_medicines():
        nonlocal all_medicines
        try:
            medicines = get_all_medicines()
            all_medicines = {m.MedicineName: m for m in medicines}
            medicine_combo["values"] = list(all_medicines.keys())
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load medicines:\n{e}", parent=window)

    load_medicines()

    def on_medicine_selected(event=None):
        name = medicine_var.get()
        if name in all_medicines:
            max_qty = all_medicines[name].StockQuantity
            if max_qty <= 0:
                messagebox.showwarning("Out of Stock", f"'{name}' is currently out of stock.", parent=window)
                medicine_var.set("")
                quantity_spinbox.config(to=1)
                quantity_spinbox.set(1)
            else:
                quantity_spinbox.config(to=max_qty)
                quantity_spinbox.set(1)

    def on_medicine_keyrelease(event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Shift_L", "Shift_R",
                            "Control_L", "Control_R", "Return", "Escape"):
            return
        typed = medicine_var.get().strip()
        all_names = list(all_medicines.keys())
        filtered = [n for n in all_names if typed.lower() in n.lower()] if typed else all_names
        medicine_combo["values"] = filtered
        on_medicine_selected()

    medicine_combo.bind("<<ComboboxSelected>>", on_medicine_selected)
    medicine_combo.bind("<KeyRelease>", on_medicine_keyrelease)

    # ── Add to Bill ───────────────────────────────────────────────────────────
    def add_to_bill():
        name = medicine_var.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please select a medicine!", parent=window)
            return

        try:
            qty = int(quantity_spinbox.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid quantity!", parent=window)
            return

        if qty <= 0:
            messagebox.showwarning("Warning", "Quantity must be at least 1!", parent=window)
            return

        medicine = all_medicines.get(name)
        if not medicine:
            messagebox.showwarning("Warning", "Medicine not found!", parent=window)
            return

        if medicine.StockQuantity <= 0:
            messagebox.showwarning("Out of Stock", f"'{name}' is out of stock.", parent=window)
            return

        if qty > medicine.StockQuantity:
            messagebox.showwarning(
                "Insufficient Stock",
                f"Only {medicine.StockQuantity} unit(s) of '{name}' available.",
                parent=window
            )
            return

        # If already in bill, update quantity
        for item in bill_tree.get_children():
            values = bill_tree.item(item, "values")
            if values[0] == name:
                existing_qty = int(values[1])
                new_qty = existing_qty + qty
                if new_qty > medicine.StockQuantity:
                    messagebox.showwarning(
                        "Insufficient Stock",
                        f"Cannot add {qty} more. Only {medicine.StockQuantity - existing_qty} additional unit(s) available for '{name}'.",
                        parent=window
                    )
                    return
                total = new_qty * medicine.Price
                bill_tree.item(item, values=(name, new_qty, f"Rs. {medicine.Price:.2f}", f"Rs. {total:.2f}"))
                update_total()
                return

        total = qty * medicine.Price
        bill_tree.insert("", "end", values=(name, qty, f"Rs. {medicine.Price:.2f}", f"Rs. {total:.2f}"))
        update_total()

    ttk.Button(top_frame, text="Add to Bill", command=add_to_bill, width=14).grid(
        row=3, column=1, pady=10, sticky="w", padx=10
    )

    # ── Bill Treeview ─────────────────────────────────────────────────────────
    tree_frame = tk.Frame(window)
    tree_frame.pack(padx=20, pady=(0, 5), fill="both", expand=True)

    columns = ("Medicine", "Qty", "Unit Price", "Total")
    bill_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    for col in columns:
        bill_tree.heading(col, text=col)
        bill_tree.column(col, width=130, anchor="center")
    bill_tree.pack(fill="both", expand=True)

    def remove_selected():
        selected = bill_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row to remove!", parent=window)
            return
        bill_tree.delete(*selected)
        update_total()

    ttk.Button(window, text="Remove Selected", command=remove_selected, width=18).pack(pady=(2, 4))

    # ── Totals ────────────────────────────────────────────────────────────────
    totals_frame = tk.Frame(window)
    totals_frame.pack(pady=4)

    medicine_total_label = ttk.Label(totals_frame, text="Medicine Total: Rs. 0.00", font=("Arial", 10))
    medicine_total_label.grid(row=0, column=0, padx=20)

    doctor_total_label = ttk.Label(totals_frame, text="Doctor Charges: Rs. 0.00", font=("Arial", 10))
    doctor_total_label.grid(row=0, column=1, padx=20)

    grand_total_label = ttk.Label(window, text="Grand Total: Rs. 0.00", font=("Arial", 11, "bold"))
    grand_total_label.pack(pady=4)

    def update_total():
        # Medicine subtotal
        med_total = 0.0
        for item in bill_tree.get_children():
            val = bill_tree.item(item, "values")[3]
            try:
                med_total += float(val.replace("Rs. ", ""))
            except ValueError:
                pass

        # Doctor charges
        doc_name = doctor_var.get()
        doc_charges = 0.0
        if doc_name in all_doctors:
            doc_charges = float(all_doctors[doc_name].fee)

        grand = med_total + doc_charges

        medicine_total_label.config(text=f"Medicine Total: Rs. {med_total:.2f}")
        doctor_total_label.config(text=f"Doctor Charges: Rs. {doc_charges:.2f}")
        grand_total_label.config(text=f"Grand Total: Rs. {grand:.2f}")

    # ── Print Bill ────────────────────────────────────────────────────────────
    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    def on_print_bill():
        patient = patient_name_entry.get().strip()
        if not patient:
            messagebox.showwarning("Warning", "Please enter patient name!", parent=window)
            return

        doc_name = doctor_var.get().strip()
        if not doc_name or doc_name not in all_doctors:
            messagebox.showwarning("Warning", "Please select a valid doctor!", parent=window)
            return

        if not bill_tree.get_children():
            messagebox.showwarning("Warning", "No medicines added to bill!", parent=window)
            return

        # Re-validate stock before printing
        bill_items = []
        med_total = 0.0
        for item in bill_tree.get_children():
            name, qty_str, unit, total = bill_tree.item(item, "values")
            qty = int(qty_str)
            medicine = all_medicines.get(name)

            if not medicine:
                messagebox.showerror("Error", f"Medicine '{name}' no longer exists in the system.", parent=window)
                return
            if qty > medicine.StockQuantity:
                messagebox.showwarning(
                    "Stock Changed",
                    f"Stock for '{name}' has changed. Only {medicine.StockQuantity} unit(s) available but {qty} requested.\nPlease update your bill.",
                    parent=window
                )
                return

            unit_price  = float(unit.replace("Rs. ", ""))
            total_price = float(total.replace("Rs. ", ""))
            bill_items.append((name, qty, unit_price, total_price))
            med_total += total_price

        doc_charges = float(all_doctors[doc_name].fee)
        grand_total = med_total + doc_charges

        # Deduct stock
        try:
            for name, qty, unit_price, total_price in bill_items:
                medicine = all_medicines[name]
                decrease_stock(medicine.medicineid, qty)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update stock:\n{e}", parent=window)
            return

        # Print bill
        try:
            print_patient_bill(patient, doc_name, bill_items, med_total, doc_charges, grand_total)
        except Exception as e:
            messagebox.showerror("Print Error", f"Bill printed but an error occurred:\n{e}", parent=window)

        messagebox.showinfo("Success", f"Bill printed and stock updated for {patient}!", parent=window)

        # Clear form
        patient_name_entry.delete(0, tk.END)
        doctor_var.set("")
        doctor_charges_label.config(text="Charges: —")
        for item in bill_tree.get_children():
            bill_tree.delete(item)
        update_total()
        load_medicines()

    ttk.Button(btn_frame, text="Print Bill", command=on_print_bill, width=16).pack()
