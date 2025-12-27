from abc import ABC, abstractmethod
from enum import Enum


class OrderType(Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    INTERNATIONAL = "international"


class Order(ABC):
    def __init__(self, order_id: str, total_amount: float):
        self.order_id = order_id
        self.total_amount = total_amount
        self.status = "created"

    @abstractmethod
    def calculate_shipping(self) -> float:
        pass

    @abstractmethod
    def get_delivery_days(self) -> int:
        pass

    def process(self):
        self.status = "processing"
        return f"Order {self.order_id} is being processed"


class StandardOrder(Order):
    def calculate_shipping(self) -> float:
        return 5.0 if self.total_amount < 100 else 0.0

    def get_delivery_days(self) -> int:
        return 7


class ExpressOrder(Order):
    def calculate_shipping(self) -> float:
        return 15.0

    def get_delivery_days(self) -> int:
        return 2


class InternationalOrder(Order):
    def calculate_shipping(self) -> float:
        return 25.0 + (0.1 * self.total_amount)

    def get_delivery_days(self) -> int:
        return 14


class OrderFactory:
    @staticmethod
    def create_order(order_type: OrderType, order_id: str, amount: float) -> Order:
        if order_type == OrderType.STANDARD:
            return StandardOrder(order_id, amount)
        elif order_type == OrderType.EXPRESS:
            return ExpressOrder(order_id, amount)
        elif order_type == OrderType.INTERNATIONAL:
            return InternationalOrder(order_id, amount)
        else:
            raise ValueError(f"Unknown order type: {order_type}")