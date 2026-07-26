import pytest
from pydantic import ValidationError

from app.operations import CalculationFactory, calculate_result
from app.schemas import CalculationCreate


def test_add_operation():
    assert calculate_result(10, 5, "Add") == 15


def test_subtract_operation():
    assert calculate_result(10, 5, "Sub") == 5


def test_multiply_operation():
    assert calculate_result(10, 5, "Multiply") == 50


def test_divide_operation():
    assert calculate_result(10, 5, "Divide") == 2


def test_factory_rejects_invalid_type():
    with pytest.raises(ValueError, match="Unsupported calculation type"):
        CalculationFactory.create_operation("Power")


def test_schema_rejects_invalid_type():
    with pytest.raises(ValidationError):
        CalculationCreate(a=10, b=5, type="Power")


def test_schema_rejects_division_by_zero():
    with pytest.raises(ValidationError, match="Cannot divide by zero"):
        CalculationCreate(a=10, b=0, type="Divide")