from rooms_app.models import RoomProfile
def register_room(hostel, room_no, room_price ,agent, gender, floor_number, bed_space_left):
    # try:
    room = RoomProfile.objects.create(hostel=hostel, room_no=room_no, 
                                    room_price=float(room_price), gender=gender,
                                    # agent_affiliate=agent, 
                                    floor_no=int(floor_number),
                                    bed_space_left=int(bed_space_left),)
    room.save()
    return 201
    # except:
    #     return 000