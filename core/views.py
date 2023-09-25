from django.utils import timezone
from django.utils.timezone import timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from rooms_app.models import RoomProfile
from campus_app.models import CampusProfile
from hostel_app.models import HostelProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from .models import Booking
from .decorators import if_user_is_login
from .models import Tenant
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter
from django.shortcuts import HttpResponse
from io import BytesIO
from django.conf import settings
from reportlab.lib import colors
from .filters import HostelFilter
from .qrcode import generate_qrcode
from .filters import HostelFilter
from django.shortcuts import render
from . import booking_info as booking_verifications


def index(request):
    # context = {'user':request.user}
    # return render(request, 'index/index.html', context)
    return render(request, 'home/index.html')


# @if_user_is_login
@login_required(login_url='accounts:login')
def hostels(request):
    
    """Get hostel that are related to particular campus and display it
    to the client"""
    campus = CampusProfile.objects.get(campus_code=
                                       request.user.campus.campus_code)
    
    campus_hostels = HostelProfile.objects.filter(campus=campus)

    #context for the page
    context={'hostels':campus_hostels, 
              'campus':campus, 'myform': HostelFilter}
    
    return render(request, 'campus_hostels.html', context)


@login_required(login_url='accounts:login')
def book_room(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    bookings_count =Booking.objects.filter(Room = room).count()
    number_left = room.Room_Capacity - bookings_count

    #check if room is full
    if  Booking.objects.filter(user=request.user).exists():
        get_booking = Booking.objects.get(user = request.user)
        messages.info(request, 'Already Booked for a room please proceed to payment!!!')
        return redirect('PaymentApp:init_payment', kwargs={'room_id':get_booking.room.room_id})
    
    #Checking if room is full
    elif bookings_count >= room.Room_Capacity:
        messages.info(request, 'Room if full for booking try again in 24 hrs')
        return redirect('HostelApp:HostelRooms', pk_HostelName=room.Hostel.hostel_name)

    #Creating booking for user
    elif request.method =='POST':
        student_id = request.user.student_id  
        booked_room = RoomProfile.objects.get(room_id=request.POST.get('room_id')) 
        #Saving booking info
        Book = Booking.objects.create(Room=booked_room, user=request.user, room_number=booked_room.room_No, Hostel=booked_room.Hostel, 
               student_id=student_id, status='Booked', end_time=(timezone.now() + timedelta(seconds=40)), Campus=booked_room.Rooms_campus).save()

        get_booking = Booking.objects.get(user = request.user)
        template = render_to_string('TextTemplates/booking_email.html', {'name':request.user.username, 'booking':get_booking})
        subject = f'Booking was successfull Mr. {request.user.username}'
        message = template
        from_email = settings.EMAIL_HOST_USER
        send_mail(fail_silently=True ,subject=subject, message=message, from_email=from_email, recipient_list=[request.user.email])
        if bookings_count == room.Room_Capacity:
            room.Occupied=True
            room.save()
            pass
        get_room_members = Tenant.objects.filter(room=room)
        return redirect('Core:booking_ver', booking_id=Book.booking_id)
        # return redirect('PaymentApp:room-payment', room_id=room.Room_ID )s
    
@login_required(login_url='Core:login')
def booking_success(request, booking_id) -> HttpResponse:
    get_user = request.user.username
    user = request.user
    get_booking = Booking.objects.get(booking_id=booking_id)
    room = get_booking.Room

    #qrcode name for user
    qrcode_name = f'VerificationFiles/Ver_Qrcodes/{get_user} qrcode.png'

    #tittle of pdf page to be generated
    title = f"{get_user} Booking details"

    #subtittle of the pdf 
    subtitle = 'www.GuudNyt.com'

    """Fucntions to generate a list strings containing booking details for every user"""
    booker_details= booking_verifications.booking_details_function(user=user, 
                                                room=room, booking=get_booking)
    text_template = booking_verifications.booking_text_message_function(user=user, 
                                                    room=room, booking=get_booking)
    
    
    """CODES THAT GENERATE BOOKING PDF USING REPORT-LAB"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    #Title
    pdf.setTitle(title)
    pdf.setFont("Helvetica", 20)
    pdf.drawString(145, 730, title)

    #Subtitle
    pdf.setFont('Helvetica', 15)
    pdf.drawString(250, 699, subtitle)

    #booker_details
    details = pdf.beginText(290, 660)
    details.setFont('Helvetica', 18)
    details.setFillColor(colors.black)
    ##############################
    for detail in booker_details:
        details.textLine(detail)
    pdf.drawText(details)

    #Main content of pdf
    text = pdf.beginText(57, 440)
    text.setFont('Helvetica', 18)
    text.setFillColor(colors.black)
    for line in text_template:
        text.textLine(line)
    pdf.drawText(text)

    #generates qrcode for user
    qr_code_image = generate_qrcode(booking_id)
    qr_code_image.save(qrcode_name)  # Save the QR code image
    pdf.drawImage(qrcode_name, 50, 490, width=200, height=200)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    response = HttpResponse(content_type='application/pdf') 
    response.write(buffer.getvalue())
    return response

def search(request):
    all_hotels = HostelProfile.objects.all()
    search_data = HostelFilter(request.POST, queryset=all_hotels)
    query = search_data.qs
    return render(request, 'home/search.html', {'query':query,'Campus':request.user.campus})

    # return render(request, 'home/search.html', {'query':query, 'Campus':request.user.campus})
