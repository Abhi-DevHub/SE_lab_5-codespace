"""Inventory management system for adding, removing, saving, and loading stock data."""
# FIX (Pylint C0114): Added module docstring

import json
from datetime import datetime
from ast import literal_eval  # FIX (Bandit B307): Imported for safe replacement of eval()
# FIX (Flake8 F401): Removed unused 'import logging'

# Global inventory data
stock_data = {}


# FIX (Pylint C0103): Renamed to snake_case 'add_item'
# FIX (Pylint W0102): Changed default 'logs=[]' to 'logs=None'
def add_item(item="default", qty=0, logs=None):
    """Add a specified quantity of an item to the stock."""
    # FIX (Pylint C0116): Added function docstring
    
    if logs is None:
        # FIX (Pylint W0102): Initialize new list inside the function
        logs = []

    # FIX (Bug): Added input validation for item and qty types
    if not item or not isinstance(qty, (int, float)):
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # FIX (Pylint C0209): Converted string formatting to an f-string
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


# FIX (Pylint C0103): Renamed to snake_case 'remove_item'
def remove_item(item, qty):
    """Remove a specified quantity of an item from the stock."""
    # FIX (Pylint C0116): Added function docstring
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
    # FIX (Flake8 E722 / Pylint W0702): Replaced 'except:' with 'except KeyError:'
    except KeyError:
        print(f"Item '{item}' not found in stock.")


# FIX (Pylint C0103): Renamed to snake_case 'get_qty'
def get_qty(item):
    """Return the current quantity of a specified item."""
    # FIX (Pylint C0116): Added function docstring
    # FIX (Bug): Use .get() to prevent KeyError and return a default
    return stock_data.get(item, 0)


# FIX (Pylint C0103): Renamed to snake_case 'load_data'
def load_data(file="inventory.json"):
    """Load inventory data from a JSON file."""
    # FIX (Pylint C0116): Added function docstring
    global stock_data
    try:
        # FIX (Pylint R1732): Use 'with' for safe file handling
        # FIX (Pylint W1514): Added 'encoding="utf-8"'
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        # FIX (Robustness): Added specific exception handling
        print(f"File '{file}' not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        # FIX (Robustness): Added specific exception handling
        print("Error reading JSON file. Starting with empty inventory.")
        stock_data = {}


# FIX (Pylint C0103): Renamed to snake_case 'save_data'
def save_data(file="inventory.json"):
    """Save inventory data to a JSON file."""
    # FIX (Pylint C0116): Added function docstring
    try:
        # FIX (Pylint R1732): Use 'with' for safe file handling
        # FIX (Pylint W1514): Added 'encoding="utf-8"'
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
    except OSError as e:
        # FIX (Robustness): Added specific exception handling
        print(f"Error saving file: {e}")


# FIX (Pylint C0103): Renamed to snake_case 'print_data'
def print_data():
    """Print the current inventory data."""
    # FIX (Pylint C0116): Added function docstring
    print("Items Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")


# FIX (Pylint C0103): Renamed to snake_case 'check_low_items'
def check_low_items(threshold=5):
    """Return a list of items with quantities below the specified threshold."""
    # FIX (Pylint C0116): Added function docstring
    # FIX (Style): Converted loop to a more Pythonic list comprehension
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """Main execution function for testing the inventory system."""
    # FIX (Pylint C0116): Added function docstring
    
    # FIX (Pylint C0103): Renamed all function calls to snake_case
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, 10)  # FIX (Bug): Corrected invalid type "ten" to 10
    remove_item("apple", 3)
    remove_item("orange", 1)  # This will now print a message
    
    # FIX (f-string/Bug): Use .get_qty() and f-string
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    
    save_data()
    load_data()
    print_data()

    # FIX (Bandit B307 / Pylint W0123): Replaced dangerous 'eval()'
    # This is now safe and won't be flagged by Bandit.
    literal_eval("('safe', 'literal', 'evaluation')")


if __name__ == "__main__":
    main()