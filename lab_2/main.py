from lab_python_oop.rectangle import Rectangle
from lab_python_oop.circle import Circle
from lab_python_oop.square import Square
import requests


def main():
    N = 20

    print("Лабораторная работа №2")

    rectangle = Rectangle(N, N, "синий")
    circle = Circle(N, "зеленый")
    square = Square(N, "красный")

    print(rectangle)
    print(circle)
    print(square)

    print("Демонстрация работы внешнего пакета (requests):")

    try:
        response = requests.get("https://httpbin.org/json")
        if response.status_code == 200:
            data = response.json()
            print("Успешный запрос к API! Получены данные:")
            print(f"Заголовок: {data['slideshow']['title']}")
            print(f"Автор: {data['slideshow']['author']}")
        else:
            print(f"Ошибка запроса: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")

    input("\nНажмите Enter для выхода...")


if __name__ == "__main__":
    main()