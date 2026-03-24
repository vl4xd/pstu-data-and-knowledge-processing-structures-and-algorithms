
def find_last_operator(s: str, operators: str) -> int:
    """Возвращает индекс последнего оператора из operators, который не внутри скобок.
    Если не найден, возвращает -1."""
    bracket_level = 0
    for i in range(len(s)-1, -1, -1):
        ch = s[i]
        if ch == ')':
            bracket_level += 1
        elif ch == '(':
            bracket_level -= 1
        elif ch in operators and bracket_level == 0:
            return i
    return -1

def addition(operand1: float, operand2: float) -> float:
    return operand1 + operand2

def subtraction(operand1: float, operand2: float) -> float:
    return operand1 - operand2

def multiplication(operand1: float, operand2: float) -> float:
    return operand1 * operand2

def division(operand1: float, operand2: float) -> float:
    return operand1 / operand2