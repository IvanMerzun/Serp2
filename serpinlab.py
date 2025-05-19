import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon


def calculate_n(z):
    return 4 + math.floor(-math.log2(z))

def line_intersection(p1, p2, p3, p4):
    """Находит точку пересечения двух прямых, заданных парами точек (p1,p2) и (p3,p4)"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # Коэффициенты уравнений прямых
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4
    C2 = A2 * x3 + B2 * y3

    # Решаем систему уравнений
    det = A1 * B2 - A2 * B1
    if det == 0:
        return None  # Прямые параллельны
    else:
        x = (B2 * C1 - B1 * C2) / det
        y = (A1 * C2 - A2 * C1) / det
        return (x, y)

def auto_scale(ax, A, B, C, padding=0.1):
    """Автоматически масштабирует график под треугольник."""
    x_min = min(A[0], B[0], C[0]) - padding
    x_max = max(A[0], B[0], C[0]) + padding
    y_min = min(A[1], B[1], C[1]) - padding
    y_max = max(A[1], B[1], C[1]) + padding
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect('equal')

def draw_sierpinski2(ax, A, B, C, n):
    if n == 0:
        triangle = Polygon([A, B, C], closed=True, fill=True, color='blue')
        ax.add_patch(triangle)
    else:
        # Делим стороны на 3 равные части
        AB1 = (A[0] + (B[0] - A[0]) / 3, A[1] + (B[1] - A[1]) / 3)
        AB2 = (A[0] + 2 * (B[0] - A[0]) / 3, A[1] + 2 * (B[1] - A[1]) / 3)

        AC1 = (A[0] + (C[0] - A[0]) / 3, A[1] + (C[1] - A[1]) / 3)
        AC2 = (A[0] + 2 * (C[0] - A[0]) / 3, A[1] + 2 * (C[1] - A[1]) / 3)

        BC1 = (B[0] + (C[0] - B[0]) / 3, B[1] + (C[1] - B[1]) / 3)
        BC2 = (B[0] + 2 * (C[0] - B[0]) / 3, B[1] + 2 * (C[1] - B[1]) / 3)

        # Находим точку D как пересечение двух линий (третья автоматически пройдет через нее)
        # Линия 1: AC1-BC1 (параллельна AB)
        # Линия 2: AB1-BC2 (параллельна AC)

        D = line_intersection(
            AC1, BC1, AB1, BC2
        )

        # Рекурсивно рисуем 6 подтреугольников
        draw_sierpinski2(ax, A, AB1, AC1, n - 1)
        draw_sierpinski2(ax, AB1, AB2, D, n - 1)
        draw_sierpinski2(ax, AB2, B, BC1, n - 1)
        draw_sierpinski2(ax, AC1, D, AC2, n - 1)
        draw_sierpinski2(ax, D, BC1, BC2, n - 1)
        draw_sierpinski2(ax, AC2, BC2, C, n - 1)


def main():
    #n = int(input("Введите количество шагов n: "))

    z = float(input("Введите масштаб z (например, 1, 0.5, 0.33, 0.25): "))
    n = calculate_n(z)

    print("Введите координаты вершин треугольника (x, y):")
    A = tuple(map(float, input("Вершина A (x y): ").split()))
    B = tuple(map(float, input("Вершина B (x y): ").split()))
    C = tuple(map(float, input("Вершина C (x y): ").split()))


    fig, ax = plt.subplots(figsize=(8, 8))
    # Устанавливаем границы видимой области
    ax.set_xlim(0, z)
    ax.set_ylim(0, z)
    ax.set_aspect('equal')
    ax.axis('on')

    draw_sierpinski2(ax, A, B, C, n)

    plt.title(f"Треугольник Серпинского №2 (n = {n}, масштаб z = {z})")

    #Cохранение в JPEG
    plt.savefig("serpiskfrac.jpg", format='jpeg', dpi=300, bbox_inches='tight')

    plt.show()


if __name__ == "__main__":
    main()