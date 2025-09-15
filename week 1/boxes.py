import math

manufactured_items = int(input("Enter the number of manufactured items: "))
items_per_box = int(input("Enter the number of items you will pack per box: "))

boxes_needed = math.ceil(manufactured_items / items_per_box)
print(f"You would need {boxes_needed} boxes.")