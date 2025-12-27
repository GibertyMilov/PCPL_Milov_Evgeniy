# test_order_factory_tdd.py
import unittest
from unittest.mock import Mock, patch, MagicMock, PropertyMock
from order_factory import OrderFactory, OrderType, Order, StandardOrder, ExpressOrder, InternationalOrder


class TestOrderFactoryTDD(unittest.TestCase):
    """TDD тесты для фабрики заказов - тестируем основную функциональность"""
    def setUp(self):
        self.factory = OrderFactory()

    def test_create_standard_order_success(self):
        """Тест 1: Успешное создание стандартного заказа"""
        # Arrange (подготовка)
        order_id = "ORD001"
        amount = 50.0

        # Act (действие)
        order = self.factory.create_order(OrderType.STANDARD, order_id, amount)

        # Assert (проверка)
        self.assertIsInstance(order, StandardOrder)
        self.assertEqual(order.order_id, order_id)
        self.assertEqual(order.total_amount, amount)
        self.assertEqual(order.status, "created")

    def test_create_express_order_success(self):
        """Тест 2: Успешное создание экспресс заказа"""
        order = self.factory.create_order(OrderType.EXPRESS, "ORD002", 150.0)

        self.assertIsInstance(order, ExpressOrder)
        self.assertEqual(order.order_id, "ORD002")
        self.assertEqual(order.total_amount, 150.0)

    def test_create_international_order_success(self):
        """Тест 3: Успешное создание международного заказа"""
        order = self.factory.create_order(OrderType.INTERNATIONAL, "ORD003", 200.0)

        self.assertIsInstance(order, InternationalOrder)
        self.assertEqual(order.order_id, "ORD003")
        self.assertEqual(order.total_amount, 200.0)

    def test_create_order_invalid_type(self):
        """Тест 4: Создание заказа с неверным типом (отрицательный тест)"""
        with self.assertRaises(ValueError):
            self.factory.create_order("INVALID_TYPE", "ORD004", 100.0)

    def test_standard_order_shipping_calculation(self):
        """Тест 5: Расчет доставки для стандартного заказа"""
        # Тест для суммы < 100
        order1 = self.factory.create_order(OrderType.STANDARD, "ORD005", 50.0)
        self.assertEqual(order1.calculate_shipping(), 5.0)

        # Тест для суммы >= 100
        order2 = self.factory.create_order(OrderType.STANDARD, "ORD006", 100.0)
        self.assertEqual(order2.calculate_shipping(), 0.0)

        order3 = self.factory.create_order(OrderType.STANDARD, "ORD007", 150.0)
        self.assertEqual(order3.calculate_shipping(), 0.0)

    def test_express_order_shipping_calculation(self):
        """Тест 6: Расчет доставки для экспресс заказа"""
        # Проверяем фиксированную стоимость
        order1 = self.factory.create_order(OrderType.EXPRESS, "ORD008", 50.0)
        self.assertEqual(order1.calculate_shipping(), 15.0)

        order2 = self.factory.create_order(OrderType.EXPRESS, "ORD009", 500.0)
        self.assertEqual(order2.calculate_shipping(), 15.0)

    def test_international_order_shipping_calculation(self):
        """Тест 7: Расчет доставки для международного заказа"""
        order = self.factory.create_order(OrderType.INTERNATIONAL, "ORD010", 300.0)
        # 25 + 0.1 * 300 = 55
        expected_shipping = 25.0 + (0.1 * 300.0)
        self.assertEqual(order.calculate_shipping(), expected_shipping)

    def test_delivery_days_for_all_order_types(self):
        """Тест 8: Получение дней доставки для всех типов заказов"""
        standard_order = self.factory.create_order(OrderType.STANDARD, "ORD011", 100.0)
        express_order = self.factory.create_order(OrderType.EXPRESS, "ORD012", 100.0)
        international_order = self.factory.create_order(OrderType.INTERNATIONAL, "ORD013", 100.0)

        self.assertEqual(standard_order.get_delivery_days(), 7)
        self.assertEqual(express_order.get_delivery_days(), 2)
        self.assertEqual(international_order.get_delivery_days(), 14)

    def test_order_processing(self):
        """Тест 9: Обработка заказа"""
        order = self.factory.create_order(OrderType.STANDARD, "ORD014", 75.0)

        # Проверяем начальный статус
        self.assertEqual(order.status, "created")

        # Обрабатываем заказ
        result = order.process()

        # Проверяем изменение статуса
        self.assertEqual(order.status, "processing")

        # Проверяем возвращаемое сообщение
        self.assertIn("ORD014", result)
        self.assertIn("is being processed", result)

class TestOrderFactoryWithMocks(unittest.TestCase):
    def test_mock_order_object(self):
        """Тест 10: Использование Mock объекта вместо реального заказа"""
        # Создаем mock объект, имитирующий Order
        mock_order = Mock(spec=Order)
        mock_order.order_id = "MOCK001"
        mock_order.total_amount = 100.0
        mock_order.status = "created"
        mock_order.calculate_shipping.return_value = 10.0
        mock_order.get_delivery_days.return_value = 5
        mock_order.process.return_value = "Mock order processed"

        # Проверяем, что mock работает
        self.assertEqual(mock_order.order_id, "MOCK001")
        self.assertEqual(mock_order.calculate_shipping(), 10.0)
        self.assertEqual(mock_order.get_delivery_days(), 5)

        # Проверяем вызовы методов
        mock_order.process()
        mock_order.process.assert_called_once()


    def test_mock_multiple_orders(self):
        """Тест 11: Тестирование нескольких mock заказов"""
        # Создаем список mock объектов
        mock_orders = []
        for i in range(3):
            mock_order = Mock(spec=Order)
            mock_order.order_id = f"MOCK{i + 1}"
            mock_order.total_amount = (i + 1) * 50.0
            mock_order.calculate_shipping.return_value = i * 5.0
            mock_orders.append(mock_order)

        # Имитируем обработку всех заказов
        shipping_costs = []
        for order in mock_orders:
            shipping_costs.append(order.calculate_shipping())

        # Проверяем результаты
        self.assertEqual(len(shipping_costs), 3)
        self.assertEqual(shipping_costs, [0.0, 5.0, 10.0])

        # Проверяем вызовы calculate_shipping
        for order in mock_orders:
            order.calculate_shipping.assert_called_once()

    def test_mock_order_processing_sequence(self):
        """Тест 12: Тестирование последовательности вызовов с mock"""
        mock_order = Mock(spec=Order)

        # Настраиваем последовательность вызовов
        mock_order.process.side_effect = [
            "Processing started",
            "Processing in progress",
            "Processing completed"
        ]

        # Имитируем процесс обработки
        results = []
        for _ in range(3):
            results.append(mock_order.process())

        # Проверяем результаты
        expected_results = [
            "Processing started",
            "Processing in progress",
            "Processing completed"
        ]
        self.assertEqual(results, expected_results)

        # Проверяем, что метод вызывался 3 раза
        self.assertEqual(mock_order.process.call_count, 3)

class TestOrderFactoryBDDStyle(unittest.TestCase):
    """Тесты в стиле BDD (поведенческие)"""

    def test_standard_order_free_shipping_condition(self):
        """Когда сумма заказа >= 100, тогда доставка бесплатная"""
        # Given (дано)
        order_under_100 = OrderFactory.create_order(OrderType.STANDARD, "BDD1", 99.0)
        order_over_100 = OrderFactory.create_order(OrderType.STANDARD, "BDD2", 100.0)

        # When (когда)
        shipping_under = order_under_100.calculate_shipping()
        shipping_over = order_over_100.calculate_shipping()

        # Then (тогда)
        self.assertEqual(shipping_under, 5.0)  # Платная доставка
        self.assertEqual(shipping_over, 0.0)  # Бесплатная доставка

    def test_express_order_fixed_shipping(self):
        """Для экспресс заказа доставка всегда стоит 15.0"""
        # Given
        order_small = OrderFactory.create_order(OrderType.EXPRESS, "BDD3", 10.0)
        order_large = OrderFactory.create_order(OrderType.EXPRESS, "BDD4", 1000.0)

        # When
        shipping_small = order_small.calculate_shipping()
        shipping_large = order_large.calculate_shipping()

        # Then
        self.assertEqual(shipping_small, 15.0)
        self.assertEqual(shipping_large, 15.0)  # Та же фиксированная стоимость


def run_tests():
    loader = unittest.TestLoader()

    # Добавляем все тестовые классы
    test_suite = unittest.TestSuite()
    test_suite.addTests(loader.loadTestsFromTestCase(TestOrderFactoryTDD))
    test_suite.addTests(loader.loadTestsFromTestCase(TestOrderFactoryWithMocks))
    test_suite.addTests(loader.loadTestsFromTestCase(TestOrderFactoryBDDStyle))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Выводим статистику
    print(f"\n{'=' * 60}")
    print("СТАТИСТИКА ТЕСТОВ:")
    print(f"{'=' * 60}")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")

    if result.failures:
        print(f"\nПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print(f"\nТЕСТЫ С ОШИБКАМИ:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()

    # Демонстрационный пример использования
    if success:
        print(f"\n{'=' * 60}")
        print("ДЕМОНСТРАЦИЯ РАБОТЫ ФАБРИКИ:")
        print(f"{'=' * 60}")

        # Пример использования фабрики
        factory = OrderFactory()

        orders = [
            factory.create_order(OrderType.STANDARD, "DEMO1", 80.0),
            factory.create_order(OrderType.EXPRESS, "DEMO2", 120.0),
            factory.create_order(OrderType.INTERNATIONAL, "DEMO3", 250.0)
        ]

        for order in orders:
            print(f"\nЗаказ: {order.order_id}")
            print(f"  Тип: {order.__class__.__name__}")
            print(f"  Сумма: ${order.total_amount}")
            print(f"  Доставка: ${order.calculate_shipping():.2f}")
            print(f"  Дней: {order.get_delivery_days()}")
            print(f"  Статус: {order.status}")

            # Обрабатываем заказ
            print(f"  {order.process()}")
            print(f"  Новый статус: {order.status}")