import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []  # Fix for W0102: Dangerous default value
    
    if not item:
        return
    
    stock_data[item] = stock_data.get(item, 0) + qty
    # Use f-string for cleaner formatting
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Fix for W0702/E722: Use specific exception
        pass


def get_qty(item):
    return stock_data[item]


def load_data(file="inventory.json"):
    global stock_data
    try:
        # Fix for R1732: Use 'with' and W1514: Specify encoding
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        stock_data = {}  # Start with an empty inventory if no file
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    # Fix for R1732: Use 'with' and W1514: Specify encoding
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4))


def print_data():
    print("Items Report")
    print("------------------")
    for i in stock_data:
        print(f"{i} -> {stock_data[i]}")
    print("------------------")


def check_low_items(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


def main():
    load_data()  # Load first in case a file already exists
    
    add_item("apple", 10)
    add_item("banana", -2)  # This is questionable logic, but we'll allow it
    
    # This line had multiple issues (type errors)
    # add_item(123, "ten")  
    # For now, let's add a valid item instead
    add_item("orange", 20)

    remove_item("apple", 3)
    remove_item("grape", 1)  # This will silently fail (KeyError)
    
    try:
        print(f"Apple stock: {get_qty('apple')}")
    except KeyError:
        print("Apple stock: 0")

    print(f"Low items: {check_low_items()}")
    
    print_data()
    save_data()
    
    # eval("print('eval used')")  # Fix for B307/W0123: Removed dangerous eval


if __name__ == "__main__":
    main()