"""Simple command-line calculator application.

def calculator():
    """Run an interactive command-line calculator.

    Prompts the user to input two numbers and an operation (+, -, *, /)
    then computes and displays the result. Handles special cases such as
    division by zero and invalid operators.

    Returns:
        None
    """
    print("Simple Calculator")
    a = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    b = float(input("Enter second number: "))

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    elif op == "*":
        result = a * b
    elif op == "/":
        if b == 0:
            print("Error: Division by zero")
            return
        result = a / b
    else:
        print("Invalid operator")
        return

    print("Result:", result)


calculator()
