from src.decorators import log_func_call

@log_func_call()
def divide(a, b):
    return a / b

if __name__ == "__main__":
    divide(10, 2)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass
