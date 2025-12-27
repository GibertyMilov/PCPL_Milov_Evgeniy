from order_factory import OrderFactory, OrderType


def demonstrate_factory_pattern():
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНА 'ФАБРИЧНЫЙ МЕТОД'")
    print("=" * 60)

    factory = OrderFactory()

    print("\n1. Создание разных типов заказов:")
    print("-" * 40)

    # Создаем заказы разных типов
    orders_data = [
        (OrderType.STANDARD, "ORD001", 75.0, "Стандартный заказ (75$)"),
        (OrderType.STANDARD, "ORD002", 120.0, "Стандартный заказ с бесплатной доставкой (120$)"),
        (OrderType.EXPRESS, "ORD003", 50.0, "Экспресс заказ (50$)"),
        (OrderType.EXPRESS, "ORD004", 200.0, "Экспресс заказ (200$)"),
        (OrderType.INTERNATIONAL, "ORD005", 150.0, "Международный заказ (150$)"),
        (OrderType.INTERNATIONAL, "ORD006", 500.0, "Международный заказ (500$)")
    ]

    orders = []
    for order_type, order_id, amount, description in orders_data:
        order = factory.create_order(order_type, order_id, amount)
        orders.append((order, description))

    # Выводим информацию о заказах
    for order, description in orders:
        print(f"\n{description}:")
        print(f"  ID: {order.order_id}")
        print(f"  Класс: {order.__class__.__name__}")
        print(f"  Доставка: ${order.calculate_shipping():.2f}")
        print(f"  Срок доставки: {order.get_delivery_days()} дней")

    print("\n2. Обработка заказов:")
    print("-" * 40)

    for order, description in orders[:3]:  # Обрабатываем первые 3 заказа
        print(f"\nОбработка {order.order_id}:")
        result = order.process()
        print(f"  Результат: {result}")
        print(f"  Новый статус: {order.status}")

    print("\n3. Сравнение стоимости доставки:")
    print("-" * 40)

    # Создаем заказы с одинаковой суммой для сравнения
    test_amount = 100.0
    test_orders = [
        ("Стандартный", factory.create_order(OrderType.STANDARD, "TEST1", test_amount)),
        ("Экспресс", factory.create_order(OrderType.EXPRESS, "TEST2", test_amount)),
        ("Международный", factory.create_order(OrderType.INTERNATIONAL, "TEST3", test_amount))
    ]

    print(f"\nПри сумме заказа ${test_amount}:")
    for name, order in test_orders:
        print(f"  {name}: доставка ${order.calculate_shipping():.2f}, {order.get_delivery_days()} дней")

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


def demonstrate_edge_cases():
    """Демонстрация граничных случаев"""
    print("\n\n" + "=" * 60)
    print("ГРАНИЧНЫЕ СЛУЧАИ И ОШИБКИ")
    print("=" * 60)

    factory = OrderFactory()

    try:
        print("\n1. Попытка создать заказ с неверным типом:")
        invalid_order = factory.create_order("INVALID_TYPE", "ERR001", 100.0)
        print("  ОШИБКА: Должно было возникнуть исключение!")
    except ValueError as e:
        print(f"  ✓ Правильно получено исключение: {e}")

    print("\n2. Заказ с нулевой суммой:")
    zero_order = factory.create_order(OrderType.STANDARD, "ZERO1", 0.0)
    print(f"  Доставка: ${zero_order.calculate_shipping():.2f}")

    print("\n3. Заказ с очень большой суммой:")
    big_order = factory.create_order(OrderType.INTERNATIONAL, "BIG1", 10000.0)
    print(f"  Доставка: ${big_order.calculate_shipping():.2f}")
    print(f"  (25 + 10% от 10000 = 25 + 1000 = 1025)")


if __name__ == "__main__":
    demonstrate_factory_pattern()
    demonstrate_edge_cases()

    # Запуск тестов
    print("\n\n" + "=" * 60)
    print("ЗАПУСК МОДУЛЬНЫХ ТЕСТОВ")
    print("=" * 60)

    import subprocess
    import sys

    # Запускаем тесты через subprocess
    result = subprocess.run([sys.executable, "-m", "unittest", "test_order_factory_tdd.TestOrderFactoryTDD", "-v"],
                            capture_output=True, text=True)
    print(result.stdout)

    if result.stderr:
        print("Ошибки:")
        print(result.stderr)