import sys
import math

def read_coefficient(name, args, index):
    value = None
    if index < len(args):
        try:
            value = float(args[index])
        except ValueError:
            pass

    while value is None:
        try:
            value = float(input(f"Введите коэффициент {name}: "))
        except ValueError:
            print("Ошибка: введите вещественное число!")

    return value


def solve_equation(a, b, c):
    print(f"\nУравнение: {a} * x^4 + {b} * x^2 + {c} = 0")

    D = b**2 - 4*a*c
    print(f"D = {D}")

    roots = []

    if D < 0:
        print("Действительных корней нет.")
        return roots

    y1 = (-b + math.sqrt(D)) / (2 * a)
    y2 = (-b - math.sqrt(D)) / (2 * a)

    for y in (y1, y2):
        if y > 0:
            roots.append(math.sqrt(y))
            roots.append(-math.sqrt(y))
        elif y == 0:
            roots.append(0)

    if roots:
        print("Действительные корни:", ", ".join(map(str, roots)))
    else:
        print("Действительных корней нет.")

    return roots


def main():
    args = sys.argv[1:]
    a = read_coefficient("A", args, 0)
    b = read_coefficient("B", args, 1)
    c = read_coefficient("C", args, 2)

    solve_equation(a, b, c)


if __name__ == "__main__":
    main()
