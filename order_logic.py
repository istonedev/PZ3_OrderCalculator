""" Модуль бизнес-логики калькулятора стоимости заказа. """

# Пороги скидки за объем: (количество, процент)
VOLUME_DISCOUNTS = [
    (50, 10),
    (20, 5),
    (10, 3),
]


def parse_positive_number(text, field_name):
    """ Преобразует строку в положительное число. """
    text = text.strip().replace(",", ".")
    if not text:
        raise ValueError(f"Поле <<{field_name}>> не заполнено")
    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"Поле <<{field_name}>>: <<{text}>> не является числом")
    if value < 0:
        raise ValueError(f"Поле <<{field_name}>> не может быть отрицательным числом")
    return value


def get_volume_discount(quantity):
    """
    Возвращает процент скидки за объем заказа.
    """
    for threshold, percent in VOLUME_DISCOUNTS:
        if quantity >= threshold:
            return percent
    return 0

def apply_discount(amount, discount_percent):
    """
    Применяет скидку к сумме.
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Скидка должна быть в диапозоне от 0 до 100%")
    return amount * (1 - discount_percent / 100)

def calculate_order(price, quantity, extra_discount=0.0):
    """
    Рассчитывает итоговую стоимость заказа.
    """
    if quantity != int(quantity):
        raise ValueError("Количество должно быть целым числом")
    
    quantity = int(quantity)
    base_amount = price * quantity
    volume_discount = get_volume_discount(quantity)
    total_discount = volume_discount + extra_discount
    
    if total_discount > 100:
        total_discount = 100
    
    final_amount = apply_discount(base_amount, total_discount)
    
    return {
        "base_amount": round(base_amount, 2),
        "volume_discount": volume_discount,
        "total_discount": total_discount,
        "saved": round(base_amount - final_amount, 2),
        "final_amount": round(final_amount, 2)
    }