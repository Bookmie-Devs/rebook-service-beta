
# VALIDATION OF NUMBER

def check_number(number: str):
    valid_phone = number.replace(" ","")
    if valid_phone[:1]=="0" and len(valid_phone)==10:
        return valid_phone

    elif valid_phone[:3]=="233" and len(valid_phone[3:])==9:
        return ("0" + "%s") % valid_phone[3:]

    elif valid_phone[:4]=="+233" and len(valid_phone[4:])==9:
        return ("0" + "%s") % valid_phone[4:]
    else:
        return "number-error"