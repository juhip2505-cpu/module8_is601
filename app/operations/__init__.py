from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        raise NotImplementedError


class AddOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(Operation):
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class CalculationFactory:
    _operations = {
        "Add": AddOperation,
        "Sub": SubtractOperation,
        "Multiply": MultiplyOperation,
        "Divide": DivideOperation,
    }

    @classmethod
    def create_operation(cls, calculation_type: str) -> Operation:
        operation_class = cls._operations.get(calculation_type)

        if operation_class is None:
            raise ValueError(
                f"Unsupported calculation type: {calculation_type}"
            )

        return operation_class()


def calculate_result(
    a: float,
    b: float,
    calculation_type: str,
) -> float:
    operation = CalculationFactory.create_operation(calculation_type)
    return operation.calculate(a, b)

def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b