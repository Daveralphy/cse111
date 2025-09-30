"""
To exceed the requirements for this assignment, I added features that prints how many days 
until New Year's Sale on January 1, prints a "return by" date 30 days in the future at 9:00 PM, 
applies buy one, get one half-off discount for product D083, and prints a coupon for a randomly 
selected product from the order.
"""

import csv
import os
from datetime import datetime, timedelta
import random

SALES_TAX_RATE = 0.06
BOGO_PRODUCT = "D083"

def read_dictionary(filename, key_column_index=0):
    dictionary = {}
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                key = row[key_column_index]
                dictionary[key] = row
    except FileNotFoundError as f:
        print(f"Error: missing products file '{filename}'")
        raise f
    return dictionary

def read_order(filename):
    orders = []
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                orders.append((row[0], int(row[1])))
    except FileNotFoundError as f:
        print(f"Error: missing request file '{filename}'")
        raise f
    return orders

def calculate_bogo_price(product_num, quantity, price):
    if product_num != BOGO_PRODUCT:
        return quantity * price
    full_pairs = quantity // 2
    remainder = quantity % 2
    total = full_pairs * (price + price * 0.5) + remainder * price
    return total

def process_order(products_dict, orders):
    total_items = 0
    subtotal = 0.0
    ordered_products = []

    for product_num, quantity in orders:
        try:
            product_info = products_dict[product_num]
        except KeyError:
            print(f"Error: unknown product ID '{product_num}' in request.csv")
            continue

        name = product_info[1]
        price = float(product_info[2])
        total_price = calculate_bogo_price(product_num, quantity, price)

        total_items += quantity
        subtotal += total_price
        ordered_products.append(name)

        if product_num == BOGO_PRODUCT and quantity > 1:
            print(f"{name}: {quantity} @ {price:.2f} (BOGO applied: {total_price:.2f})")
        else:
            print(f"{name}: {quantity} @ {price:.2f}")

    return total_items, subtotal, ordered_products

def print_receipt(total_items, subtotal, ordered_products):
    print("Inkom Emporium")
    sales_tax = subtotal * SALES_TAX_RATE
    total = subtotal + sales_tax

    print(f"Number of Items: {total_items}")
    print(f"Subtotal: {subtotal:.2f}")
    print(f"Sales Tax: {sales_tax:.2f}")
    print(f"Total: {total:.2f}")
    print("Thank you for shopping at the Inkom Emporium.")

    now = datetime.now()
    print(now.strftime("%a %b %d %H:%M:%S %Y"))

    next_year = datetime(now.year + 1, 1, 1)
    days_until_new_year = (next_year - now).days
    print(f"Days until New Year's Sale: {days_until_new_year}")

    return_by = now + timedelta(days=30)
    return_by = return_by.replace(hour=21, minute=0, second=0, microsecond=0)
    print(f"Return by: {return_by.strftime('%a %b %d %I:%M %p %Y')}")

    if ordered_products:
        coupon_product = random.choice(ordered_products)
        print(f"Coupon: Get 10% off your next purchase of {coupon_product}!")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    products_path = os.path.join(script_dir, "products.csv")
    request_path = os.path.join(script_dir, "request.csv")

    products_dict = read_dictionary(products_path)
    orders = read_order(request_path)
    total_items, subtotal, ordered_products = process_order(products_dict, orders)
    print_receipt(total_items, subtotal, ordered_products)

if __name__ == "__main__":
    main()