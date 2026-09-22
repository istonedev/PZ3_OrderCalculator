import tkinter as tk
from tkinter import ttk, messagebox

from order_logic import calculate_order, parse_positive_number
from config.colors import *


class OrderCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор стоимости заказа")
        self.root.geometry("520x560")
        
        self.price_var = tk.StringVar(value="100")
        self.quantity_var = tk.StringVar(value="1")
        self.extra_discount_var = tk.IntVar(value=0)
        self.status_var = tk.StringVar(value="Введите данные заказа")
        
        self._build_ui()
        self._bind_events()
        self.recalculate()
    
    # Привязка событий
    def _bind_events(self):
        # Событие нажатия кнопки
        self.calc_button.config(command=self.on_calculate_click)
        self.clear_button.config(command=self.on_clear_click)
        
        # Событие клавиатуры: пересчет при вводе символа
        self.price_entry.bind("<KeyRelease>", self.on_input_change)
        self.quantity_entry.bind("<KeyRelease>", self.on_input_change)
        
        # Событие изменения переменной (выбор промокода)
        self.extra_discount_var.trace_add("write", self.on_promo_change)
        
        # Событие нажатия Enter в окне
        self.root.bind("<Return>", self.on_calculate_click)
        
        # Событие закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
    # Обработчики событий
    def on_calculate_click(self, event=None):
        self.recalculate(show_error_dialog=True)
    
    def on_input_change(self, event=None):
        self.recalculate()
    
    def on_promo_change(self, *args):
        self.recalculate()
    
    def on_clear_click(self):
        self.price_var.set("")
        self.quantity_var.set("")
        self.extra_discount_var.set(0)
        self.show_empty_result()
        self.price_entry.focus_set()
    
    def on_close(self):
        if messagebox.askokcancel("Выход", "Зыкрыть приложение?"):
            self.root.destroy()
    
    # Обновление интерфейса
    def recalculate(self, show_error_dialog=False):
        try:
            price = parse_positive_number(self.price_var.get(), "Цена за единицу")
            quantity = parse_positive_number(self.quantity_var.get(), "Количество")
            result = calculate_order(price, quantity, self.extra_discount_var.get())
        except ValueError as error:
            self.show_empty_result()
            self.set_status(str(error), ok = False)
            if show_error_dialog:
                messagebox.showerror("Ошибка ввода", str(error))
            return
        
        self.base_label.config(text=f"Сумма без скидки: {result['base_amount']:.2f} RUB")
        self.discount_label.config(text=f"Скидка: {result['total_discount']:.0f} %"
                                   f"(за объем) {result['volume_discount']} %")
        self.saved_label.config(text=f"Экономия: {result['saved']:.2f} RUB")
        self.total_label.config(text=f"Итого: {result['final_amount']:.2f} RUB")
        self.set_status("Расчёт выполнен", ok=True)
        
    def _build_ui(self):
        self.root.configure(bg=BG)

        tk.Label(self.root, text="Калькулятор стоимости заказа",
                 font=("Segoe UI Semibold", 15), bg=BG,
                 fg=TEXT_DARK).pack(pady=(18, 4))

        # Карточка ввода данных
        form = tk.Frame(self.root, bg=CARD_BG, padx=20, pady=16,
                        highlightbackground="#DDE3E7", highlightthickness=1)
        form.pack(fill="x", padx=20)

        tk.Label(form, text="Цена за единицу, руб.", bg=CARD_BG,
                 fg=TEXT_GRAY).grid(row=0, column=0, sticky="w")
        self.price_entry = tk.Entry(form, textvariable=self.price_var,
                                    width=18, relief="solid", bd=1)
        self.price_entry.grid(row=0, column=1, sticky="e", pady=6)

        tk.Label(form, text="Количество, шт.", bg=CARD_BG,
                 fg=TEXT_GRAY).grid(row=1, column=0, sticky="w")
        self.quantity_entry = tk.Entry(form, textvariable=self.quantity_var,
                                       width=18, relief="solid", bd=1)
        self.quantity_entry.grid(row=1, column=1, sticky="e", pady=6)
        form.columnconfigure(0, weight=1)
        
        # Переключатели промокода
        promo = tk.LabelFrame(self.root, text=" Промокод ", bg=BG,
                              fg=TEXT_GRAY, padx=12, pady=8)
        promo.pack(fill="x", padx=20, pady=14)
        for text, value in [("Без промокода", 0), ("STUDENT (5 %)", 5),
                            ("SALE (12 %)", 12)]:
            tk.Radiobutton(promo, text=text, value=value,
                           variable=self.extra_discount_var, bg=BG,
                           selectcolor=CARD_BG, anchor="w").pack(anchor="w")
        
        # Кнопки
        buttons = tk.Frame(self.root, bg=BG)
        buttons.pack(fill="x", padx=20)
        self.calc_button = tk.Button(buttons, text="Рассчитать", bg=ACCENT,
                                     fg="white", relief="flat",
                                     padx=18, pady=7, cursor="hand2")
        self.calc_button.pack(side="left")
        self.clear_button = tk.Button(buttons, text="Clear", bg="#E4E9ED",
                                      fg=TEXT_DARK, relief="flat",
                                      padx=18, pady=7, cursor="hand2")
        self.clear_button.pack(side="left", padx=8)
        
        # Карточка результата
        card = tk.Frame(self.root, bg=CARD_BG, padx=20, pady=16,
                        highlightbackground="#DDE3E7", highlightthickness=1)
        card.pack(fill="x", padx=20, pady=16)
        
        self.base_label = tk.Label(card, text="Сумма без скидки: -",
                                   bg=CARD_BG, fg=TEXT_GRAY, anchor="w")
        self.base_label.pack(fill="x")
        self.discount_label = tk.Label(card, text="Скидка: -",
                                       bg=CARD_BG, fg=TEXT_GRAY, anchor="w")
        self.discount_label.pack(fill="x", pady=2)
        self.saved_label = tk.Label(card, text="Экономия: -",
                                    bg=CARD_BG, fg=OK_GREEN, anchor="w")
        self.saved_label.pack(fill="x", pady=2)
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=8)
        self.total_label = tk.Label(card, text="ИТОГО: -",
                                    font=("Segoe UI Semibold", 18),
                                    bg=CARD_BG, fg=ACCENT, anchor="w")
        self.total_label.pack(fill="x")
        
        # Строка состояния
        self.status_label = tk.Label(self.root, textvariable=self.status_var,
                                     bg=BG, fg=TEXT_GRAY, anchor="w")
        self.status_label.pack(fill="x", padx=22)
    
    def show_empty_result(self):
        self.base_label.config(text="Сумма без скидки: -")
        self.discount_label.config(text="Скидка: -")
        self.saved_label.config(text="Экономия: -")
        self.total_label.config(text="Итого: -")
    
    def set_status(self, message, ok = True):
        self.status_var.set(message)
        self.status_label.config(fg=TEXT_GRAY if ok else ERROR_RED)
        
def main():
    root = tk.Tk()
    OrderCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()