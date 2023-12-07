
# VALIDATION OF NUMBER

def check_number(number: str):
    if number[:1]=="0" and len(number)==10:
        return number

    elif number[:3]=="233" and len(number[3:])==9:
        return ("0" + "%s") % number[3:]

    elif number[:4]=="+233" and len(number[4:])==9:
        return ("0" + "%s") % number[4:]
    else:
        return "number-error"