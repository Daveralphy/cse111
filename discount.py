from datetime import datetime

discount_rate = .1
tax_rate = .06
today = datetime.now()
weekday = today.isoweekday()

subtotal = 0
quantity = 1
while quantity != 0:
    quantity = int(input("Enter the quantity of items: "))
    if quantity == 0:
        break
    price = float(input("Enter the price: "))
    subtotal += quantity * price
    print(f"Subtotal: {subtotal:.2f}")

discount = 0
if weekday == 2 or weekday == 3:
    if subtotal >= 50:
        discount = round(subtotal * discount_rate, 2)
        print(f"Discount: {discount:.2f}")
    else:
        short = 50 - subtotal
        print(f"You can get a discount by ordering {short:.2f} more")
else:
    discount = 0

subtotal -= discount
tax = round(subtotal * tax_rate, 2)
total = round(subtotal + tax, 2)
print(f"Tax: {tax:.2f}")
print(f"Total Due: {total:.2f}")
