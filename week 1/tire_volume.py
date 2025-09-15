"""
Exceeding Requirements: I have added functionality to provide prices for different tire volumes.
It then asks the user if they would like to purchase the tire and collects their phone number if they do.
"""

import math
from datetime import date

today = date.today()

pi = math.pi
w_input = input("Enter the width of the tire in mm (for example 205): ")
a_input = input("Enter the aspect ratio of the tire (for example 60): ")
d_input = input("Enter the diameter of the wheel in inches (for example 15): ")

# To convert the user input to numbers.
if w_input.isdigit() and a_input.isdigit() and d_input.isdigit():
    w = float(w_input)
    a = float(a_input)
    d = float(d_input)

# To check if the numbers are positive or valid.
    if w > 0 and a > 0 and d > 0:
        v = round((pi * w**2 * a * (w * a + 2540 * d)) / 10000000000, 2)
        print(f"\nThe approximate volume is {v:.2f} liters.")

# Exceeding Requirements: I added a price list.
        prices = {
            (185, 50, 14): 45000,
            (205, 60, 15): 52000,
            (215, 65, 16): 58000
        }
        key = (w, a, d)
        if key in prices:
            print(f"The price for this tire size is ${prices[key]:,}")

# Exceeding Requirements: I added prompt that asks the user if they would like to purchase the tire.
# If yes, it collects their phone number.
# If no, it skips the phone number input.
        purchase = input("Would you like to purchase this tire? (yes/no): ").strip().lower()
        if purchase == 'yes' or purchase == 'y':
            phone_number = input("Please enter your phone number: ")
            print("Thank you for your purchase! We will contact you soon.")
        else:
            phone_number = ""
            print("No problem! Let us know if you change your mind.")

# To log the data into the volume.txt file
        with open("volume.txt", "at") as file:
            file.write(f"{today:%Y-%m-%d}, {w:.0f}, {a:.0f}, {d:.0f}, {v}, {phone_number} \n")
        print("Your request has been logged.")
    else:
        print("Invalid input. Please enter positive numbers.")
else:
    print("Invalid input. Please enter numbers only.")