# main.py
from order_factory import OrderFactory, OrderType


def demonstrate_factory():
    print("=== Демонстрация фабричного метода ===")
    factory = OrderFactory()

    orders = [
        factory.create_order(OrderType.STANDARD, "ORD001", 75.0),
        factory.create_order(OrderType.EXPRESS, "ORD002", 120.0),
        factory.create_order(OrderType.INTERNATIONAL, "ORD003", 300.0)
    ]

    for order in orders:
        print(f"\nЗаказ {order.order_id}:")
        print(f"  Сумма: ${order.total_amount}")
        print(f"  Доставка: ${order.calculate_shipping()}")
        print(f"  Дней доставки: {order.get_delivery_days()}")
        print(f"  Обработка: {order.process()}")


if __name__ == "__main__":
    demonstrate_factory()