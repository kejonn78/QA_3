import math

class SideException(Exception):
    """Пользовательское исключение для ошибок с длинами сторон"""
    pass

class TriangleCalculator:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def _validate_sides(self):
        """Внутренняя проверка сторон треугольника"""
        # Проверка диапазона сторон
        if not (1 <= self.a < 100 and 1 <= self.b < 100 and 1 <= self.c < 100):
            raise SideException("Стороны должны быть от 1 до 100")

        # Проверка возможности образования треугольника (неравенство треугольника)
        if (self.a >= self.b + self.c or
            self.b >= self.a + self.c or
            self.c >= self.a + self.b):
            raise SideException("Недопустимые длины сторон: треугольник не может существовать")

    def get_area(self) -> float:
        """Вычисление площади треугольника по формуле Герона"""
        self._validate_sides()

        # Вычисление полупериметра
        p = (self.a + self.b + self.c) / 2

        # Вычисление площади
        try:
            area = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))
        except ValueError:
            raise SideException("Невозможно вычислить площадь треугольника")

        return round(area, 2)

    def get_perimeter(self) -> float:
        """Вычисление периметра треугольника"""
        self._validate_sides()
        return round(self.a + self.b + self.c, 2)

    def get_triangle_type(self) -> str:
        """Определение типа треугольника по сторонам и углам"""
        self._validate_sides()

        # Сортируем стороны для удобства работы (c — предполагаемая гипотенуза)
        sides = sorted([self.a, self.b, self.c])
        a, b, c = sides[0], sides[1], sides[2]

        # Тип по сторонам
        if self.a == self.b == self.c:
            side_type = "равносторонний"
        elif self.a == self.b or self.b == self.c or self.a == self.c:
            side_type = "равнобедренный"
        else:
            side_type = "разносторонний"

        # Тип по углам (используем теорему Пифагора)
        # c² = a² + b² — прямоугольный
        # c² < a² + b² — остроугольный
        # c² > a² + b² — тупоугольный
        c_squared = c ** 2
        ab_squared_sum = a ** 2 + b ** 2

        if abs(c_squared - ab_squared_sum) < 1e-10:  # Учитываем погрешности вычислений
            angle_type = "прямоугольный"
        elif c_squared < ab_squared_sum:
            angle_type = "остроугольный"
        else:
            angle_type = "тупоугольный"

        return f"{side_type}, {angle_type}"

        # Создаём экземпляр треугольника
triangle = TriangleCalculator(3, 4, 5)

# Вычисляем площадь
#print("Площадь:", triangle.get_area())  # Площадь: 6.0

# Вычисляем периметр
#print("Периметр:", triangle.get_perimeter())  # Периметр: 12.0

# Определяем тип треугольника
#print("Тип треугольника:", triangle.get_triangle_type())  # Тип треугольника: разносторонний, прямоугольный