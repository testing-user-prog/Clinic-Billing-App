import tkinter as tk
from tkinter import ttk, messagebox
from models.medicine import get_all_medicines, get_medicine_by_name, add_medicine, increase_medicine_price, increase_stock

def open_update_medicines():
    window = tk.Toplevel()
    window.title("Update Medicines")
    window.geometry("450x380")
    window.resizable(False, False)

    ttk.Label(window, text="Update Medicines", font=("Arial", 16, "bold")).pack(pady=15)

    form_frame = tk.Frame(window)
    form_frame.pack(padx=20, pady=10)

    ttk.Label(form_frame, text="Medicine Name:").grid(row=0, column=0, sticky="w", pady=8)
    medicine_var = tk.StringVar()
    medicine_combo = ttk.Combobox(form_frame, textvariable=medicine_var, width=25)
    medicine_combo.grid(row=0, column=1, padx=10)

    # ── Load once, reuse on every keystroke ─────────────────────
    all_names = []

    def load_medicines():
        nonlocal all_names
        medicines = get_all_medicines()
        all_names = [m.MedicineName for m in medicines]
        medicine_combo["values"] = all_names

    load_medicines()

    ttk.Label(form_frame, text="Current Price:").grid(row=1, column=0, sticky="w", pady=8)
    current_price_label = ttk.Label(form_frame, text="--")
    current_price_label.grid(row=1, column=1, sticky="w", padx=10)

    ttk.Label(form_frame, text="New Price (optional):").grid(row=2, column=0, sticky="w", pady=8)
    new_price_entry = ttk.Entry(form_frame, width=27)
    new_price_entry.grid(row=2, column=1, padx=10)

    ttk.Label(form_frame, text="Add Stock Quantity:").grid(row=3, column=0, sticky="w", pady=8)
    quantity_spinbox = ttk.Spinbox(form_frame, from_=1, to=9999, width=25)
    quantity_spinbox.grid(row=3, column=1, padx=10)

    ttk.Label(form_frame, text="Price (new medicine):").grid(row=4, column=0, sticky="w", pady=8)
    new_medicine_price_entry = ttk.Entry(form_frame, width=27)
    new_medicine_price_entry.grid(row=4, column=1, padx=10)
    new_medicine_price_entry.grid_remove()

    new_medicine_label = form_frame.grid_slaves(row=4, column=0)[0]
    new_medicine_label.grid_remove()

    def on_medicine_input_changed(typed):
        if not typed:
            current_price_label.config(text="--")
            new_medicine_price_entry.grid_remove()
            new_medicine_label.grid_remove()
            return

        # Check for an exact match (case-insensitive)
        exact_match = None
        for name in all_names:
            if name.lower() == typed.lower():
                exact_match = name
                break

        if exact_match:
            medicine = get_medicine_by_name(exact_match)
            if medicine:
                current_price_label.config(text=f"Rs. {medicine.Price:.2f}")
                new_medicine_price_entry.grid_remove()
                new_medicine_label.grid_remove()
            else:
                current_price_label.config(text="New medicine")
                new_medicine_price_entry.grid()
                new_medicine_label.grid()
        else:
            # Check if typed text is a prefix of any medicine name (case-insensitive)
            is_prefix = any(name.lower().startswith(typed.lower()) for name in all_names)
            if is_prefix:
                # User is likely typing an existing medicine name
                current_price_label.config(text="--")
                new_medicine_price_entry.grid_remove()
                new_medicine_label.grid_remove()
            else:
                # User typed a name that doesn't match and isn't a prefix of any existing medicine
                current_price_label.config(text="New medicine")
                new_medicine_price_entry.grid()
                new_medicine_label.grid()

    def on_medicine_selected(event=None):
        name = medicine_var.get().strip()
        on_medicine_input_changed(name)

    def on_keyrelease(event):
        # Ignore navigation keys (except BackSpace)
        if event.keysym in ("Left", "Right", "Up", "Down", "Shift_L", "Shift_R", "Control_L", "Control_R", "Return", "Escape"):
            return

        typed = medicine_var.get().strip()

        if typed:
            filtered = [name for name in all_names if typed.lower() in name.lower()]
        else:
            filtered = all_names

        medicine_combo["values"] = filtered

        on_medicine_input_changed(typed)

    medicine_combo.bind("<<ComboboxSelected>>", on_medicine_selected)
    medicine_combo.bind("<KeyRelease>", on_keyrelease)

    def on_submit():
        name      = medicine_var.get().strip()
        new_price = new_price_entry.get().strip()
        quantity  = quantity_spinbox.get().strip()

        if not name:
            messagebox.showwarning("Warning", "Please enter or select a medicine name!", parent=window)
            return

        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity!", parent=window)
            return

        medicine = get_medicine_by_name(name)

        if medicine:
            if new_price:
                try:
                    new_price = float(new_price)
                    if new_price <= 0:
                        messagebox.showwarning("Warning", "Price must be greater than 0!", parent=window)
                        return
                except ValueError:
                    messagebox.showwarning("Warning", "Invalid price entered!", parent=window)
                    return

            try:
                if new_price:
                    increase_medicine_price(medicine.medicineid, new_price)
                increase_stock(medicine.medicineid, quantity)
                messagebox.showinfo("Success", f"{name} updated successfully!", parent=window)
                on_medicine_selected()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=window)
        else:
            price_input = new_medicine_price_entry.get().strip()
            if not price_input:
                messagebox.showwarning("Warning", "Price is required for a new medicine!", parent=window)
                return
            try:
                price_input = float(price_input)
                if price_input <= 0:
                    messagebox.showwarning("Warning", "Price must be greater than 0!", parent=window)
                    return
            except ValueError:
                messagebox.showwarning("Warning", "Invalid price entered!", parent=window)
                return
            try:
                add_medicine(name, price_input, quantity)
                messagebox.showinfo("Success", f"{name} added to database!", parent=window)
                load_medicines()
                new_medicine_price_entry.delete(0, tk.END)
                new_medicine_price_entry.grid_remove()
                new_medicine_label.grid_remove()
                current_price_label.config(text="--")
                medicine_var.set("")
            except Exception as e:
                if "UNIQUE" in str(e) or "duplicate" in str(e).lower():
                    messagebox.showerror("Error", "Medicine already exists in database!", parent=window)
                else:
                    messagebox.showerror("Error", str(e), parent=window)

    ttk.Button(window, text="Submit", command=on_submit, width=20).pack(pady=15)
