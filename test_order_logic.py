import unittest

from order_logic import (
    apply_discount,
    calculate_order,
    get_volume_discount,
    parse_positive_number
)


class TestVolumeDiscount(unittest.TestCase):
    """
    Тесты скидки за объем (проверка граничных значений)
    """
    
    def test_no_discount_below_threshold(self):
        self.assertEqual(get_volume_discount(9), 0)
        
    def test_three_percent_at_ten_items(self):
        self.assertEqual(get_volume_discount(10), 3)
        
    def test_five_percent_at_twenty_items(self):
        self.assertEqual(get_volume_discount(20), 5)
        
    def test_ten_percent_at_fifty_items(self):
        self.assertEqual(get_volume_discount(50), 10)


class TestParsePositiveNumber(unittest.TestCase):
    """
    Тесты разбора пользовательского ввода
    """
    
    def test_parses_integer_string(self):
        self.assertEqual(parse_positive_number("120", "Цена"), 120.0)
        
    def test_text_instead_of_number_raises_error(self):
        with self.assertRaises(ValueError):
            parse_positive_number("сто", "Цена")
    
    def test_negative_number_raises_error(self):
        with self.assertRaises(ValueError):
            parse_positive_number("-10", "Цена")
            

class TestCalculatorOrder(unittest.TestCase):
    """
    Тесты итогового расчета заказа
    """
    
    def test_order_with_volume_discount(self):
        result = calculate_order(price=100, quantity=20)
        self.assertEqual(result["base_amount"], 2000)
        self.assertEqual(result["final_amount"], 1900)
    
    def test_fractional_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            calculate_order(price=100, quantity=2.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)