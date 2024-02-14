from accounts.models import Student
from core.models import Tenant
from rooms_app.models import RoomProfile

def tenant_auth_details(student:Student=None, 
                        tenant:Tenant=None, 
                        room:RoomProfile=None):
    
    return [f'Name: {student.user.username}',
            f'Student ID: {student.student_id}',
            f'Room Number: {room.room_no}',
            f'Hostel: {room.hostel.hostel_name}',
            f'Payment made to: {room.hostel.account_number}',
            f'Hostel Contact: {room.hostel.hostel_contact}',
            #########[space in pdf]
            '',
            '',
            'Please Note:',
            f'This authentication pdf must', 
            f'be sent to {tenant.hostel.hostel_name}', 
            'for authentication',]
           
def tenant_auth_message(student:Student=None, 
                        tenant:Tenant=None, 
                        room:RoomProfile=None):

    return [f'Terms And Conditions:',
            f'Welcome once again to {tenant.hostel.hostel_name}',
            '',
            f'Note that AUTHENTICATION IS VALID FOR A YEAR!!!',
            f'From now to {tenant.end_date.date()}  @{tenant.end_date.hour}:{tenant.end_date.minute}!!!',
            '',
             'Also users can decide to update their scanable qrcode for the',
            f'same hostel in which they are in.', 
            'Thank You!',
            f'Enjoy your stay............!!!']
