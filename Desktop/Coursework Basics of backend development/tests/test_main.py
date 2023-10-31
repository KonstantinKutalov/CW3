from src.main import format_operation
from src import main
import json
import pytest



def test_format_operation():
    # Создаем тестовые данные
    test_operation = {
        "date": "2023-10-30T08:30:45.123456",
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Покупка",
        "from": "Visa 1234567890123456",
        "to": "Счет 1234567890",
        "state": "EXECUTED"
    }

    # Вызываем функцию format_operation
    formatted_result = format_operation(test_operation)

    # Проверяем, что результат соответствует ожидаемому формату
    expected_result = "2023.10.30 Покупка\nXXXX XX** **** 3456 -> Счет **7890\n500.00 руб. (EXECUTED)"
    assert formatted_result == expected_result


def test_format_operation_without_from_and_to_executed():
    # Создаем тестовые данные без номера карты и номера счета, состояние "EXECUTED"
    test_operation = {
        "date": "2023-10-30T08:30:45.123456",
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Покупка",
        "state": "EXECUTED"
    }

    # Вызываем функцию format_operation
    formatted_result = format_operation(test_operation)

    # Проверяем, что результат соответствует ожидаемому формату для "EXECUTED"
    assert "2023.10.30" in formatted_result
    assert "Покупка" in formatted_result
    assert " -> Счет " in formatted_result
    assert "руб. (EXECUTED)" in formatted_result


def test_format_operation_without_from_and_to_canceled():
    # Создаем тестовые данные без номера карты и номера счета, состояние "CANCELED"
    test_operation = {
        "date": "2023-10-30T08:30:45.123456",
        "operationAmount": {
            "amount": "500.00",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Покупка",
        "state": "CANCELED"
    }

    # Вызываем функцию format_operation
    formatted_result = format_operation(test_operation)

    # Проверяем, что результат соответствует ожидаемому формату для "CANCELED"
    assert "2023.10.30" in formatted_result
    assert "Покупка" in formatted_result
    assert " -> Счет " in formatted_result
    assert "руб. (CANCELED)" in formatted_result


# До сюда все работает

data_with_executed_operations = [
    {"state": "EXECUTED", "date": "2023-01-01", "description": "Operation 1"},
    {"state": "EXECUTED", "date": "2023-01-02", "description": "Operation 2"},
    {"state": "EXECUTED", "date": "2023-01-03", "description": "Operation 3"},
    {"state": "EXECUTED", "date": "2023-01-04", "description": "Operation 4"},
    {"state": "EXECUTED", "date": "2023-01-05", "description": "Operation 5"},
]

data_without_executed_operations = [
    {"state": "PENDING", "date": "2023-01-01", "description": "Operation 1"},
    {"state": "PENDING", "date": "2023-01-02", "description": "Operation 2"},
    {"state": "PENDING", "date": "2023-01-03", "description": "Operation 3"},
]

def test_main_with_executed_operations(capsys):
    main.data = data_with_executed_operations
    main.main()
    captured = capsys.readouterr()
    output = captured.out
    assert "2019.12.08 Открытие вклада" in output  # Проверяем, что конкретная операция была напечатана

def test_main_no_executed_or_canceled_operations(capsys):
    main.data = data_without_executed_operations
    main.main()
    captured = capsys.readouterr()
    output = captured.out.splitlines()
    for line in output:
        assert "CANCELED" not in line


# До сюда работает

