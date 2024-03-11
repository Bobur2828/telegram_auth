import re

# Regular expression for Korean phone number validation
KOR = r'^\+82\d{2}\d{4}\d{4}$'

def validate_korean_phone_number(phone_number):
    """
    Validates Korean phone number.
    
    Parameters:
    phone_number (str): Phone number to validate.
    
    Returns:
    bool: True if the phone number is valid, False otherwise.
    """
    return bool(re.match(KOR, phone_number))

# Example usage:
phone_number = "+821234567890"
if validate_korean_phone_number(phone_number):
    print(f"{phone_number} is a valid Korean phone number.")
else:
    print(f"{phone_number} is not a valid Korean phone number.")
