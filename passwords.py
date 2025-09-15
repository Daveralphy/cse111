'''
I included a couple of extra features to make this program more robust and user-friendly,
thereby exceeding the assignment requirements:

1. The user can type 'g' to generate a secure, random password that meets the password strength
requirements.
2. The password strength checker also provides specific and actionable feedback, therefore 
guiding them on how to improve their password.
'''

# First, lets import necessary libraries
import secrets # This will be used for generating secure random passwords

# I think we should then define file paths for dictionary and common passwords in case they change in the future
dictionary_file = "wordlist.txt"
top_passwords_file = "toppasswords.txt"

# Lets create a function that reads the files and checks if the word the user enters is present.
def word_in_file(word, filename, case_sensitive=False):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = (line.strip() for line in file)
            if not case_sensitive:
                return any(word.lower() == line.lower() for line in lines)
            return any(word == line for line in lines)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return False

# We have to define the character sets
LOWER = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
UPPER = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
SPECIAL = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "|", ";", ":", "\"", "'", ",", ".", "<", ">", "?", "/", "`", "~"]

# Lets define another function to check if any character in a word is in the given character set
def word_has_character(word, character_list):
    return any(char in character_list for char in word)

# Now, lets define a function to calculate the complexity of a word. We will be using the ascii sets
# because they are comprehensive and cover all necessary characters instead of just defining the characters.
def word_complexity(word):
    complexity = 0
    if word_has_character(word, LOWER):
        complexity += 1
    if word_has_character(word, UPPER):
        complexity += 1
    if word_has_character(word, DIGITS):
        complexity += 1
    if word_has_character(word, SPECIAL):
        complexity += 1
    return complexity

# Then, lets define the main function to evaluate password strength
def password_strength(password, min_length=10, strong_length=16):
    if word_in_file(password, dictionary_file, case_sensitive=False):
        print("Password is a dictionary word and is not secure.")
        return 0
    if word_in_file(password, top_passwords_file, case_sensitive=True):
        print("Password is a commonly used password and is not secure.")
        return 0
    complexity_score = word_complexity(password)
    strength = 1 + complexity_score
    if len(password) < min_length:
        print("Password is too short and is not secure.")
        return strength
    if len(password) >= strong_length:
        print("Password is long, which is excellent for security.")
        return min(5, strength + 1)
    print(f"Password complexity score: {complexity_score}, strength: {strength}")
    return strength

# ----------------------------------------------------------------------------------------------
# Exceeding Requirements:
# ----------------------------------------------------------------------------------------------

# Lets add a function that checks the complexity and provides feedback.
# This function provides feedback based on the complexity of the password.
def get_strength_feedback(password, feedback):
    if not password.strip():
        return 0, ["Password cannot be empty or only whitespace."]
    complexity_score = word_complexity(password)
    if not word_has_character(password, LOWER): feedback.append("Consider adding lowercase letters.")
    if not word_has_character(password, UPPER): feedback.append("Consider adding uppercase letters.")
    if not word_has_character(password, DIGITS): feedback.append("Consider adding numbers.")
    if not word_has_character(password, SPECIAL): feedback.append("Consider adding special characters (e.g., !@#$%).")
    return 1 + complexity_score, feedback

# Lets add a comprehensive function that combines all checks and provides detailed feedback
def get_detailed_strength(password, min_length=10, strong_length=16):
    if not password.strip():
        return 0, ["Password cannot be empty or only whitespace."]
    feedback = []
    if word_in_file(password, dictionary_file, case_sensitive=False):
        feedback.append("Password is a dictionary word and is not secure.")
        return 0, feedback
    if word_in_file(password, top_passwords_file, case_sensitive=True):
        feedback.append("Password is a commonly used password and is not secure.")
        return 0, feedback
    strength, feedback = get_strength_feedback(password, feedback)
    if len(password) < min_length:
        feedback.insert(0, "Password is too short and is not secure.")
        return 1, feedback
    if len(password) >= strong_length:
        feedback.append("Password is long, which is excellent for security.")
        return 5, feedback
    return strength, feedback

# Lets define a function to generate a strong password.
# This function generates a random password that meets the strong password criteria.
def generate_strong_password(length=16):
    alphabet = LOWER + UPPER + DIGITS + SPECIAL
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if word_complexity(password) == 4:
            return password

# Lets define a function to process password checking
# This function processes the password and prints the strength and feedback.
def process_password_check(password):
    strength, feedback = get_detailed_strength(password)
    print(f"Password strength: {strength}/5")
    for item in feedback:
        print(f"- {item}")
    print()

# ------------------------------------------------------------------------------------------------------

# Its also important that we define the main interactive loop
def main():
    while True:
        password = input("Enter a password to check, 'g' to generate a password, or 'q' to quit: ")
        if password.lower() == 'q':
            print("Exiting password checker.")
            break
        elif password.lower() == 'g':
            new_password = generate_strong_password()
            print(f"Generated strong password: {new_password}\n")
        else:
            process_password_check(password)

# To run the main function if this script is executed
if __name__ == "__main__":
    main()