import re 
from django.core.exceptions import ValidationError

UZB = r'^\+998\d{9}$'
KAZ = r'^\+77[0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}$'
RUS = r'^\+79[0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}$'
AME = r'^\+1\d{10}$'
KOR = r'^\+82\d{2}\d{4}\d{4}$'

def check_country(user_input):
    if re.match(UZB, user_input) is not None:
        return 'UZBEKISTAN'
    elif re.match(KAZ, user_input) is not None:
        return 'KAZAKHSTAN'
    elif re.match(RUS, user_input) is not None:
        return 'RUSSIA'
    elif re.match(AME, user_input) is not None:
        return 'AMERICA'
    elif re.match(KOR, user_input) is not None:
        return 'KOREA'
    else:
        raise ValidationError("Nomalum davlat")