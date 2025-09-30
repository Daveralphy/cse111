import csv
import os

def read_dictionary(filename, key_column_index=0):
    students = {}
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            key = row[key_column_index].replace("-", "")
            value = row[1]
            students[key] = value
    return students

def validate_id(user_id):
    clean_id = user_id.replace("-", "")
    if not clean_id.isdigit():
        return None, "Invalid ID Number: contains non-digit characters"
    if len(clean_id) < 4:
        return None, "Invalid ID Number: too few digits"
    if len(clean_id) > 10:
        return None, "Invalid ID Number: too many digits"
    return clean_id, None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "students.csv")
    
    students = read_dictionary(csv_path)
    
    while True:
        user_id = input("Enter a student ID (or 'quit' to exit): ")
        if user_id.lower() == "quit":
            print("Exiting program.")
            break

        clean_id, error = validate_id(user_id)
        if error:
            print(error)
            continue

        if clean_id in students:
            print(f"Student Name: {students[clean_id]}")
        else:
            print("No such student")

if __name__ == "__main__":
    main()
