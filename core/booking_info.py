
def booking_details_function(user=None, booking=None, room=None):

    return [f'Name: {user.first_name} {user.last_name}',
            f'Student ID: {user.student_id}',
            f'Room Number: {room.room_no}',
            f'Hostel: {room.Hostel.hostel_name}',
            f'Hostel Bank Deatails: {room.Hostel.hostel_bank_details}',
            f'Hostel Momo: {room.Hostel.hostel_mobile_money_details}',
            f'You have 24 hours to pay hostel fees',
            'or booking will be terminated by',
            f'{booking.end_time.date()}  @{booking.end_time.hour}:{booking.end_time.minute}!!!']

def booking_text_message_function(user=None, booking=None, room=None):

    return [f'Congratulation {user.first_name} {user.last_name} on booking',
            f'Payments must be made to the bank acoount {room.Hostel.hostel_bank_details}',
            f'or the mobile number/momo line {room.Hostel.hostel_mobile_money_details}.',
            f'Note that booking will be terminated by',
            f'{booking.end_time.date()}  @{booking.end_time.hour}:{booking.end_time.minute}!!!',
            f'You have 24 hours to pay the hostel fees to the accounts provided.',
            f'Payments Made Are not reversible............']
