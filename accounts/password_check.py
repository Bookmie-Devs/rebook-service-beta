import re

def custom_password_validator(password):
    # Define your password complexity requirements
    min_length = 8
    min_uppercase = 1
    min_lowercase = 1
    min_digits = 1
    min_special_chars = 1

    # Check the password length
    if len(password) < min_length:
        return False, "Password must be at least {} characters long.".format(min_length)

    # Check for uppercase letters
    if len(re.findall(r'[A-Z]', password)) < min_uppercase:
        return False, "Password must contain at least {} uppercase letter(s).".format(min_uppercase)

    # Check for lowercase letters
    if len(re.findall(r'[a-z]', password)) < min_lowercase:
        return False, "Password must contain at least {} lowercase letter(s).".format(min_lowercase)

    # Check for digits
    if len(re.findall(r'[0-9]', password)) < min_digits:
        return False, "Password must contain at least {} digit(s).".format(min_digits)

    # Check for special characters (you can customize the set of special characters)
    if len(re.findall(r'[!@#$%^&*()_+{}[\]:;<>,.?~]", password)) < min_special_chars:
        return False, "Password must contain at least {} special character(s).".format(min_special_chars)

    # If all checks pass, the password is considered strong
    return True, "Password is strong."

# # Example usage
# user_password = "StrongP@ss123"
# is_strong, message = custom_password_validator(user_password)

# if is_strong:
#     print("Password is strong.")
# else:
#     print("Password is weak: {}".format(message))
