import random

words = ["big", "red", "funny", "Yellow", "wait"]

def main():
    numbers = [16.2, 75.1, 52.3]
    word_list = []
    print(numbers)
    append_random_numbers(numbers)
    print(numbers)
    append_random_numbers(numbers, 3)
    print(numbers)
    append_random_words(word_list)
    print(word_list)
    append_random_words(word_list, 3)
    print(word_list)

def append_random_words(word_list, quantity = 1):
    for _ in range(quantity):
        word_list.append(random.choice(words))
def append_random_numbers(numbers_list, quantity=1):
    for _ in range(quantity):
        num = random.uniform(0, 100)
        num = round(num, 1)
        numbers_list.append(num)

if __name__ == "__main__":
    main()