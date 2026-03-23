from datetime import datetime


def log_activity(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[LOG] Function Name : {func.__name__}")
        print(f"[LOG] Timestamp     : {timestamp}")
        print(f"[LOG] Arguments     : args={args}, kwargs={kwargs}")

        result = func(*args, **kwargs)

        print(f"[LOG] Return Value  : {result}")
        print("-" * 40)

        return result
    return wrapper


@log_activity
def calculate_total(price, quantity):
    return price * quantity


@log_activity
def apply_discount(total, discount):
    return total - (total * discount / 100)


@log_activity
def greet_customer(name):
    return f"Hello, {name}!"

total = calculate_total(200, 3)
final_price = apply_discount(total, 15)
message = greet_customer("Muneeb")