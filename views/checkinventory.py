import tkinter as tk
from tkinter import ttk, messagebox
from models.medicine import get_low_stock_medicines

THRESHOLD = 10


def open_check_inventory():
    window = tk.Toplevel()
    window.title("Check Inventory")
    window.geometry("480x400")
    window.resizable(False, False)

    ttk.Label(window, text="Low Stock Inventory", font=("Arial", 16, "bold")).pack(pady=12)
    ttk.Label(
        window,
        text=f"Medicines with stock below {THRESHOLD} unit(s)",
        font=("Arial", 9),
        foreground="gray"
    ).pack()

    tree_frame = tk.Frame(window)
    tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

    columns = ("Medicine", "Unit Price", "Stock")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)

    tree.heading("Medicine",   text="Medicine Name")
    tree.heading("Unit Price", text="Unit Price")
    tree.heading("Stock",      text="Stock Qty")

    tree.column("Medicine",   width=230, anchor="w")
    tree.column("Unit Price", width=110, anchor="center")
    tree.column("Stock",      width=90,  anchor="center")

    # Tag colours: red for out-of-stock, orange for low stock
    tree.tag_configure("out",  foreground="#cc0000")
    tree.tag_configure("low",  foreground="#b35900")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    count_label = ttk.Label(window, text="", font=("Arial", 9, "italic"))
    count_label.pack(pady=(0, 4))

    def load_data():
        # Clear existing rows
        for item in tree.get_children():
            tree.delete(item)

        try:
            rows = get_low_stock_medicines(THRESHOLD)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load inventory:\n{e}", parent=window)
            return

        for row in rows:
            tag = "out" if row.StockQuantity <= 0 else "low"
            tree.insert(
                "", "end",
                values=(row.MedicineName, f"Rs. {row.Price:.2f}", row.StockQuantity),
                tags=(tag,)
            )

        count = len(rows)
        if count == 0:
            count_label.config(text="All medicines are sufficiently stocked.", foreground="green")
        else:
            count_label.config(text=f"{count} medicine(s) need restocking.", foreground="#b35900")

    load_data()

    ttk.Button(window, text="Refresh", command=load_data, width=16).pack(pady=(0, 12))
