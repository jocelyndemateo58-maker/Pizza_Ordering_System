import tkinter as tk
from tkinter import ttk, messagebox


pizza_prices = {
    "Margherita Classica": 260,
    "Quattro Formaggi": 320,
    "Diavola Spicy Salami": 340,
    "Truffle Mushroom": 350,
    "Prosciutto & Arugula": 380
}

size_prices = {
    "Personal (10\")": 0,
    "Regular (12\")": 75,
    "Family (16\")": 150
}

topping_prices = {
    " Mozzarella": 45,
    "Fresh Basil": 25,
    "Black Olives": 35,
    "Jalapenos": 30,
    "Caramelized Onions": 35
}


window = tk.Tk()
window.title("Forno Classico | Pizza Ordering System")
window.geometry("880x640")
window.resizable(False, False)
window.configure(bg="#FAF3E8")


pizza_var = tk.StringVar(value="Margherita Classica")
size_var = tk.StringVar(value="Personal (10\")")
quantity_var = tk.StringVar(value="1")

topping_vars = {
    topping: tk.BooleanVar(value=False)
    for topping in topping_prices
}


def calculate_total():
    pizza = pizza_var.get()
    size = size_var.get()
    raw_qty = quantity_var.get().strip()

    
    try:
        quantity = int(raw_qty)
        if quantity < 1 or quantity > 50:
            raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Quantity",
            "Please enter a whole number between 1 and 50."
        )
        return

    
    confirm = messagebox.askyesno(
        "Confirm Pizza Order",
        f"Place order for {quantity}x {pizza} ({size})?"
    )
    if not confirm:
        return

    
    base_price = pizza_prices[pizza]
    size_addon = size_prices[size]
    selected_toppings = [t for t, var in topping_vars.items() if var.get()]
    toppings_cost = sum(topping_prices[t] for t in selected_toppings)

    unit_total = base_price + size_addon + toppings_cost
    grand_total = unit_total * quantity

   
    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(tk.END, "========================================\n")
    receipt_text.insert(tk.END, "        FORNO CLASSICO RECEIPT          \n")
    receipt_text.insert(tk.END, "========================================\n\n")
    receipt_text.insert(tk.END, f"Pizza Flavor : {pizza}\n")
    receipt_text.insert(tk.END, f"Base Price   : ₱{base_price:,.2f}\n")
    receipt_text.insert(tk.END, f"Size Tier    : {size} (+₱{size_addon:,.2f})\n\n")
    receipt_text.insert(tk.END, "Extra Toppings:\n")

    if selected_toppings:
        for t in selected_toppings:
            receipt_text.insert(tk.END, f"  + {t:<22} ₱{topping_prices[t]:>6,.2f}\n")
    else:
        receipt_text.insert(tk.END, "  (None selected)\n")

    receipt_text.insert(tk.END, "\n----------------------------------------\n")
    receipt_text.insert(tk.END, f"Price per Pizza : ₱{unit_total:,.2f}\n")
    receipt_text.insert(tk.END, f"Quantity        : {quantity}\n")
    receipt_text.insert(tk.END, "----------------------------------------\n")
    receipt_text.insert(tk.END, f"TOTAL AMOUNT    : ₱{grand_total:,.2f}\n")
    receipt_text.insert(tk.END, "========================================\n")
    receipt_text.config(state="disabled")


def reset_order():
    pizza_var.set("Margherita Classica")
    size_var.set("Personal (10\")")
    quantity_var.set("1")

    for var in topping_vars.values():
        var.set(False)

    receipt_text.config(state="normal")
    receipt_text.delete("1.0", tk.END)
    receipt_text.insert(
        tk.END,
        "Select your pizza options on the left\nand click PLACE ORDER to view receipt."
    )
    receipt_text.config(state="disabled")


header_frame = tk.Frame(window, bg="#2C1810", pady=16)
header_frame.pack(fill="x")

tk.Label(
    header_frame,
    text="FORNO CLASSICO PIZZERIA",
    font=("Georgia", 20, "bold"),
    bg="#2C1810",
    fg="#FAF3E8"
).pack()

tk.Label(
    header_frame,
    text= "Wood-Fired Artisan Pizza  |  Blistered Crusts & Molten Cheese",
    font=("Segoe UI", 10),
    bg="#2C1810",
    fg="#E6A15C"
).pack(pady=(2, 0))


main_container = tk.Frame(window, bg="#FAF3E8", padx=24, pady=18)
main_container.pack(fill="both", expand=True)

left_frame = tk.Frame(
    main_container,
    bg="#FFFFFF",
    padx=20,
    pady=16,
    highlightbackground="#E2D5C8",
    highlightthickness=1
)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

right_frame = tk.Frame(
    main_container,
    bg="#FFFFFF",
    padx=20,
    pady=16,
    highlightbackground="#E2D5C8",
    highlightthickness=1
)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

main_container.columnconfigure(0, weight=1)
main_container.columnconfigure(1, weight=1)


tk.Label(
    left_frame,
    text="1. Choose Pizza Flavor",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#B7410E"
).pack(anchor="w")

pizza_dropdown = ttk.Combobox(
    left_frame,
    textvariable=pizza_var,
    values=list(pizza_prices.keys()),
    state="readonly",
    font=("Segoe UI", 10)
)
pizza_dropdown.pack(fill="x", pady=(4, 12))

tk.Label(
    left_frame,
    text="2. Select Size Tier",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#B7410E"
).pack(anchor="w")

for size, price in size_prices.items():
    label_text = f"{size}  —  Included" if price == 0 else f"{size}  (+₱{price})"
    tk.Radiobutton(
        left_frame,
        text=label_text,
        variable=size_var,
        value=size,
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        fg="#2C1810",
        selectcolor="#FAF3E8",
        activebackground="#FFFFFF"
    ).pack(anchor="w", pady=1)

tk.Label(
    left_frame,
    text="3. Add Extra Toppings",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#B7410E"
).pack(anchor="w", pady=(12, 2))

for topping, price in topping_prices.items():
    tk.Checkbutton(
        left_frame,
        text=f"{topping} (+₱{price})",
        variable=topping_vars[topping],
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        fg="#2C1810",
        selectcolor="#FAF3E8",
        activebackground="#FFFFFF"
    ).pack(anchor="w", pady=1)

tk.Label(
    left_frame,
    text="4. Quantity (1 to 50)",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#B7410E"
).pack(anchor="w", pady=(12, 4))

quantity_spinbox = tk.Spinbox(
    left_frame,
    from_=1,
    to=50,
    textvariable=quantity_var,
    font=("Segoe UI", 11),
    width=10,
    bg="#FAF3E8",
    fg="#2C1810"
)
quantity_spinbox.pack(anchor="w")


tk.Label(
    right_frame,
    text="ORDER SUMMARY & RECEIPT",
    font=("Segoe UI", 11, "bold"),
    bg="#FFFFFF",
    fg="#B7410E"
).pack(anchor="w", pady=(0, 8))

receipt_text = tk.Text(
    right_frame,
    height=18,
    width=42,
    font=("Consolas", 10),
    bg="#FAF3E8",
    fg="#2C1810",
    relief="flat",
    padx=10,
    pady=10
)
receipt_text.pack(fill="both", expand=True)
receipt_text.insert(
    tk.END,
    "Select your pizza options on the left\nand click PLACE ORDER to view receipt."
)
receipt_text.config(state="disabled")

btn_frame = tk.Frame(right_frame, bg="#FFFFFF", pady=12)
btn_frame.pack(fill="x")

place_btn = tk.Button(
    btn_frame,
    text="PLACE ORDER",
    font=("Segoe UI", 10, "bold"),
    bg="#B7410E",
    fg="white",
    activebackground="#96330A",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=8,
    command=calculate_total
)
place_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))

reset_btn = tk.Button(
    btn_frame,
    text="RESET",
    font=("Segoe UI", 10, "bold"),
    bg="#4A6741",
    fg="white",
    activebackground="#395032",
    activeforeground="white",
    relief="flat",
    padx=16,
    pady=8,
    command=reset_order
)
reset_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))


window.mainloop()