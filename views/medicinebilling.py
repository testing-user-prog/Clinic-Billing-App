import tkinter as tk
from tkinter import ttk, messagebox
from models.medicine import get_all_medicines, decrease_stock
from printbill import print_bill

def open_medicine_billing():
    window = tk.Toplevel()
    window.title("Medicine Billing")
    window.geometry("620x600")
    window.resizable(False, False)

    ttk.Label(window, text="Medicine Billing", font=("Arial", 16, "bold")).pack(pady=12)

    top_frame = tk.Frame(window)
    top_frame.pack(padx=20, fill="x")

    ttk.Label(top_frame, text="Patient Name:").grid(row=0, column=0, sticky="w", pady=6)
    patient_name_entry = ttk.Entry(top_frame, width=35)
    patient_name_entry.grid(row=0, column=1, padx=10, pady=6)

    ttk.Label(top_frame, text="Medicine:").grid(row=1, column=0, sticky="w", pady=6)
    medicine_var = tk.StringVar()
    medicine_combo = ttk.Combobox(top_frame, textvariable=medicine_var, width=28)
    medicine_combo.grid(row=1, column=1, padx=10, pady=6)

    ttk.Label(top_frame, text="Quantity:").grid(row=1, column=2, sticky="w", padx=(10, 0))
    quantity_spinbox = ttk.Spinbox(top_frame, from_=1, to=1, width=8)
    quantity_spinbox.grid(row=1, column=3, padx=5)

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

    def on_keyrelease(event):
        if event.keysym in ("Left", "Right", "Up", "Down", "Shift_L", "Shift_R", "Control_L", "Control_R", "Return", "Escape"):
            return

        typed = medicine_var.get().strip()
        all_names = list(all_medicines.keys())

        if typed:
            filtered = [name for name in all_names if typed.lower() in name.lower()]
        else:
            filtered = all_names

        medicine_combo["values"] = filtered
        on_medicine_selected()

    medicine_combo.bind("<<ComboboxSelected>>", on_medicine_selected)
    medicine_combo.bind("<KeyRelease>", on_keyrelease)

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
        row=2, column=1, pady=10, sticky="w", padx=10
    )

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

    total_label = ttk.Label(window, text="Grand Total: Rs. 0.00", font=("Arial", 11, "bold"))
    total_label.pack(pady=4)

    def update_total():
        grand = 0.0
        for item in bill_tree.get_children():
            val = bill_tree.item(item, "values")[3]
            try:
                grand += float(val.replace("Rs. ", ""))
            except ValueError:
                pass
        total_label.config(text=f"Grand Total: Rs. {grand:.2f}")

    btn_frame = tk.Frame(window)
    btn_frame.pack(pady=10)

    def on_print_bill():
        patient = patient_name_entry.get().strip()
        if not patient:
            messagebox.showwarning("Warning", "Please enter patient name!", parent=window)
            return
        if not bill_tree.get_children():
            messagebox.showwarning("Warning", "No medicines added to bill!", parent=window)
            return

        # Re-validate stock before printing (in case stock changed while window was open)
        bill_items = []
        grand = 0.0
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
            grand += total_price

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
            print_bill(patient, bill_items, grand)
        except Exception as e:
            messagebox.showerror("Print Error", f"Bill printed but an error occurred:\n{e}", parent=window)
            # Don't return — stock was already deducted, so still clear the form

        messagebox.showinfo("Success", f"Bill printed and stock updated for {patient}!", parent=window)

        # Clear form
        patient_name_entry.delete(0, tk.END)
        for item in bill_tree.get_children():
            bill_tree.delete(item)
        update_total()
        load_medicines()

    ttk.Button(btn_frame, text="Print Bill", command=on_print_bill, width=16).pack()