import tkinter as tk
from tkinter import messagebox

CATEGORIES = {
    "Кафе и топли": [
        ("Еспресо", 1.80),
        ("Капучино", 2.40),
        ("Чай", 1.60),
    ],
    "Закуски": [
        ("Баничка", 2.20),
        ("Кроасан", 1.90),
        ("Сандвич", 3.80),
    ],
    "Напитки": [
        ("Вода 0.5л", 1.20),
        ("Сок", 2.10),
        ("Газирана напитка", 2.00),
    ],
    "Услуги": [
        ("Билет градски", 1.00),
        ("Лотариен билет", 3.00),
        ("Ваучер", 10.00),
    ],
}


class LafkaApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Лафка — Бърза поръчка")
        self.root.geometry("680x460")
        self.root.configure(bg="#1E2024")

        self.cart: list[tuple[str, float]] = []
        self.active_category = tk.StringVar(value="Кафе и топли")

        self._build_ui()
        self._render_items()

    def _build_ui(self):
        # Top header
        header = tk.Frame(self.root, bg="#D9232E", pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="ЛАФКА",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#D9232E",
        ).pack()

        # Main layout: left (categories + items), right (order/cart)
        main = tk.Frame(self.root, bg="#1E2024", padx=14, pady=14)
        main.pack(fill=tk.BOTH, expand=True)

        left = tk.Frame(main, bg="#1E2024")
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        right = tk.Frame(main, bg="#2A2D34", width=220, padx=12, pady=12)
        right.pack(side=tk.RIGHT, fill=tk.Y)

        # Category buttons row
        cat_bar = tk.Frame(left, bg="#1E2024")
        cat_bar.pack(fill=tk.X, pady=(0, 12))

        self.cat_buttons: dict[str, tk.Button] = {}
        for cat in CATEGORIES:
            btn = tk.Button(
                cat_bar,
                text=cat,
                font=("Arial", 10, "bold"),
                relief=tk.FLAT,
                padx=10,
                pady=8,
                cursor="hand2",
                command=lambda c=cat: self._select_category(c),
            )
            btn.pack(side=tk.LEFT, padx=(0, 6))
            self.cat_buttons[cat] = btn

        # Item buttons grid
        self.items_frame = tk.Frame(left, bg="#1E2024")
        self.items_frame.pack(fill=tk.BOTH, expand=True)

        # Right side: Cart & action buttons
        tk.Label(
            right,
            text="Избрани артикули",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2A2D34",
        ).pack(anchor="w", pady=(0, 8))

        self.cart_listbox = tk.Listbox(
            right,
            font=("Arial", 10),
            bg="#181A1F",
            fg="white",
            selectbackground="#D9232E",
            relief=tk.FLAT,
            height=12,
        )
        self.cart_listbox.pack(fill=tk.BOTH, expand=True)

        self.total_label = tk.Label(
            right,
            text="Общо: 0.00 лв.",
            font=("Arial", 12, "bold"),
            fg="#FFD166",
            bg="#2A2D34",
            pady=10,
        )
        self.total_label.pack(anchor="w")

        tk.Button(
            right,
            text="Премахни избрания",
            font=("Arial", 10),
            bg="#444852",
            fg="white",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=self._remove_selected,
        ).pack(fill=tk.X, pady=(0, 6))

        tk.Button(
            right,
            text="Изчисти",
            font=("Arial", 10),
            bg="#6C343A",
            fg="white",
            relief=tk.FLAT,
            pady=6,
            cursor="hand2",
            command=self._clear_cart,
        ).pack(fill=tk.X, pady=(0, 6))

        tk.Button(
            right,
            text="Завърши поръчка",
            font=("Arial", 11, "bold"),
            bg="#2EC4B6",
            fg="#111317",
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
            command=self._checkout,
        ).pack(fill=tk.X)

    def _select_category(self, category: str):
        self.active_category.set(category)
        self._render_items()

    def _render_items(self):
        current = self.active_category.get()

        # Highlight active category button
        for cat, btn in self.cat_buttons.items():
            if cat == current:
                btn.configure(bg="#D9232E", fg="white")
            else:
                btn.configure(bg="#2F333B", fg="#D0D4DC")

        # Clear previous item buttons
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        items = CATEGORIES[current]
        for idx, (name, price) in enumerate(items):
            row, col = divmod(idx, 2)
            btn = tk.Button(
                self.items_frame,
                text=f"{name}\n{price:.2f} лв.",
                font=("Arial", 11, "bold"),
                bg="#2A2D34",
                fg="white",
                activebackground="#3A3F4A",
                activeforeground="white",
                relief=tk.FLAT,
                height=3,
                cursor="hand2",
                command=lambda n=name, p=price: self._add_item(n, p),
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        self.items_frame.grid_columnconfigure(0, weight=1)
        self.items_frame.grid_columnconfigure(1, weight=1)

    def _add_item(self, name: str, price: float):
        self.cart.append((name, price))
        self._refresh_cart()

    def _remove_selected(self):
        selection = self.cart_listbox.curselection()
        if selection:
            idx = selection[0]
            self.cart.pop(idx)
            self._refresh_cart()

    def _clear_cart(self):
        self.cart.clear()
        self._refresh_cart()

    def _refresh_cart(self):
        self.cart_listbox.delete(0, tk.END)
        total = 0.0
        for name, price in self.cart:
            self.cart_listbox.insert(tk.END, f"{name} — {price:.2f} лв.")
            total += price
        self.total_label.config(text=f"Общо: {total:.2f} лв.")

    def _checkout(self):
        if not self.cart:
            messagebox.showwarning("Празна поръчка", "Първо избери поне един артикул.")
            return
        total = sum(price for _, price in self.cart)
        messagebox.showinfo(
            "Поръчката е готова",
            f"Артикули: {len(self.cart)}\nОбща сума: {total:.2f} лв.",
        )
        self._clear_cart()


if __name__ == "__main__":
    root = tk.Tk()
    LafkaApp(root)
    root.mainloop()