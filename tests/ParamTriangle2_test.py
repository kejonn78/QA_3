import pytest
import sys
sys.path.append('d:/testPython/')
from triangle import TriangleCalculator

@pytest.fixture
def make_triangle():
    """Фабрика для создания объектов TriangleCalculator"""
    def _make(a, b, c):
        return TriangleCalculator(a, b, c)
    return _make


@pytest.mark.parametrize(
    "a,b,c,expected_area",
    [
        (3, 4, 5, 6.0),
        (5, 5, 5, 10.83),
        (7, 8, 9, 26.83),
    ],
)
def test_get_area_parametrized(make_triangle, a, b, c, expected_area):
    calculator = make_triangle(a, b, c)
    assert calculator.get_area() == pytest.approx(expected_area, abs=0.01)


@pytest.mark.parametrize(
    "a,b,c,expected_perimeter",
    [
        (3, 4, 5, 12.0),
        (5, 5, 5, 15.0),
        (7, 8, 9, 24.0),
    ],
)
def test_get_perimeter_parametrized(make_triangle, a, b, c, expected_perimeter):
    calculator = make_triangle(a, b, c)
    assert calculator.get_perimeter() == pytest.approx(expected_perimeter, abs=0.01)


@pytest.mark.parametrize(
    "a,b,c,expected_type",
    [
        (3, 4, 5, "разносторонний, прямоугольный"),
        (5, 5, 5, "равносторонний, остроугольный"),
        (6, 6, 8, "равнобедренный, остроугольный"),
    ],
)
def test_get_triangle_type_parametrized(make_triangle, a, b, c, expected_type):
    calculator = make_triangle(a, b, c)
    assert calculator.get_triangle_type() == expected_type