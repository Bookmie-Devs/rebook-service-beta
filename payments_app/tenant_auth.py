
def tenant_auth_details(user=None, tenant=None, room=None):

    return [f'Name: {user.first_name} {user.last_name}',
            f'Student ID: {user.student_id}',
            f'Room Number: {room.room_no}',
            f'Hostel: {room.hostel.hostel_name}',
            f'Payment made to: {room.hostel.account_number}',
            f'Hostel Momo: {room.hostel.mobile_money}',

            f'This authentication pdf must', 
            f'be sent to {tenant.hostel.hostel_name}', 
            'the hostel for authentication',]
           
def tenant_auth_message(user=None, tenant=None, room=None):

    return [f'Congratulation {user.username}',
            f'Welcome to {tenant.hostel.hostel_name}',
            f'Note that authentication is valid for a year!!!',
            f'{tenant.end_date.date()}  @{tenant.end_date.hour}:{tenant.end_date.minute}!!!',
             'Note: AUTHENTICATION IS VALID FOR A YEAR',
            f'VALID TILL {tenant.end_date.date()}  @{tenant.end_date.hour}:{tenant.end_date.minute}!!!'
            f'Enjoy your stay............']
