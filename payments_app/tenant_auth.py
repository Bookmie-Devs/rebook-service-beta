
def tenant_auth_details(user=None, tenant=None, room=None):

    return [f'Name: {user.first_name} {user.last_name}',
            f'Student ID: {user.student_id}',
            f'Room Number: {room.room_no}',
            f'Hostel: {room.Hostel.hostel_name}',
            f'Payment made to: {room.Hostel.hostel_bank_details}',
            f'Hostel Momo: {room.Hostel.hostel_mobile_money_details}',

            f'This authentication pdf must be sent to the hostel for authentication',

            'Note: AUTHENTICATION IS VALID FOR A YEAR',
            f'VALID TILL {tenant.end_time.date()}  @{tenant.end_time.hour}:{tenant.end_time.minute}!!!']

def tenant_auth_message(user=None, tenant=None, room=None):

    return [f'Congratulation {user.username}',
            f'Welcome to {tenant.hostel.hostel_name}'
            f'Note that booking will be terminated by',
            f'{tenant.end_time.date()}  @{tenant.end_time.hour}:{tenant.end_time.minute}!!!',
            f'You have 24 hours to pay the hostel fees to the accounts provided.',
            f'Payments Made Are not reversible............']
