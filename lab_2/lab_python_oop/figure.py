from abc import ABC, abstractmethod


class Figure(ABC):
    @abstractmethod
    def area(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass