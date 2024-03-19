"""Custom imports"""
from django.http import HttpRequest
from .models import PaymentHistory, PhysicalPaymentHistory
from rooms_app.models import RoomProfile
from core.qrcode import generate_qrcode
from config.sms import send_sms_message
from .payStack import (paystack_verification, 
                       payment_is_confirm,
                    #    redirect_payment
                       )
from core import forms
from .sales import calculate_year_sales, calculate_agent_year_sales
from core.models import Tenant
from core.models import Booking
from accounts.models import Student
from hostel_app.models import HostelProfile
from .physical_payment_auth import (tenant_auth_details, 
                          tenant_auth_message)

"""Packeges """
from reportlab.lib.pagesizes import letter
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.conf import settings
from django.shortcuts import render, redirect
from reportlab.lib import colors



@login_required()
def physical_payment(request: HttpRequest, room_id):
    student = Student.objects.get(user=request.user)
    booking = Booking.objects.get(student=student)
    room = RoomProfile.objects.get(room_id=room_id)
    email = request.POST.get('email')
    if booking._has_expired():
        booking.delete()
        messages.info(request, 'Sorry, Booking has expired please book another room', extra_tags="danger")
        return redirect('accounts:booking-and-payments')
    """
    Check if booking is for upadting vcode
    and create a new payment history and skip the
    check for if room is occupied (beacuse at the time of update it will surely be occcupied)
    """
    if booking.is_updating_vcode:
        #save payment details
        payment = PhysicalPaymentHistory.objects.create(
        student=student,
        email=email,
        amount=room.ptf_room_price,
        account_payed_to=room.hostel.account_number,
        room=room,
        hostel=room.hostel,
        )
        payment.save()            
        return redirect('payments:physical-payment-confirm', payment_id=payment.payment_id)

    elif room.occupied:
        messages.info(request, 'Sorry, room has just been occupied by someone, please select new one')
        booking.delete()
        return redirect('accounts:booking-and-payments')

    else:
        if PaymentHistory.objects.filter(student=student, successful=False).exists():
            # check if there is an unsuccessful payment
            PaymentHistory.objects.filter(student=student, successful=False).delete()
            # save payment details
            payment = PhysicalPaymentHistory.objects.create(
            student=student,
            email=request.POST.get('email'),
            amount=room.ptf_room_price,
            account_payed_to=room.hostel.account_number,
            room=room,
            hostel=room.hostel,)
            payment.save()
            return redirect('payments:physical-payment-confirm', payment_id=payment.payment_id)
        else:
            #save payment details
            payment = PhysicalPaymentHistory.objects.create(
            student=student,
            email=request.POST.get('email'),
            amount=room.ptf_room_price,
            account_payed_to=room.hostel.account_number,
            room=room,
            hostel=room.hostel,
            )
            payment.save()            
            return  redirect('payments:physical-payment-confirm', payment_id=payment.payment_id)



@login_required()
def physical_payment_confirm(request: HttpRequest, payment_id):  
    student = Student.objects.get(user=request.user)
    """
    To prevent more than one payament history being query use user
    and referene_id to query history after payment is made
    """
    payment = get_object_or_404(PhysicalPaymentHistory, student=student, payment_id=payment_id)

    # room payed for    
    acquired_room = RoomProfile.objects.get(room_id=payment.room.room_id)
   
    tenant = Tenant.objects.create(student=student, room=payment.room, hostel=payment.hostel)
    tenant.save()

    # calculate sales on each payment
    calculate_year_sales(hostel=payment.hostel,amount_paid=payment.room.room_price)
    # agent sales
    calculate_agent_year_sales(hostel=payment.hostel)

    # count active tenants in th room after user booking is payed for
    count_members: int = Tenant.objects.filter(room=payment.room, end_date__gt=payment.room.campus.end_of_acadamic_year).count()

    # SET ROOM TO FULL IF CAPACITY HAS BEEN FIELED OR REDUCE BED SPACE LEFT
    acquired_room.reduce_bed_spaces(count_members=count_members)
    # change the room gender if the room is open and the the tenant is the first person
    acquired_room.change_room_gender(members=count_members,user_gender=request.user.gender)
    # DELETE BOOKING FOR USER
    booking = Booking.objects.get(student=student)
    booking.delete()    

    current_domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META['HTTP_HOST'])
    # send sms
    msg = render_to_string('emails/tenant_sms.html',{"user":request.user,"tenant":tenant,"amount":payment.amount,"domain":current_domain})
    send_sms_message(user_contact=request.user.phone, msg=msg)
    # send sms to manager
    manager_msg = render_to_string('emails/hostel_manager_msg.html',{'manager':tenant.hostel.hostel_manager,
                                                                        'tenant':tenant})
    send_sms_message(user_contact=tenant.hostel.hostel_manager.phone,msg=manager_msg)

    # send emails
    subject = f'Confirmation: Your Room Booking is Complete!'
    send_mail(from_email=settings.EMAIL_HOST_USER, fail_silently=True,
    recipient_list=[request.user.email], subject=subject, 
    message=render_to_string('emails/tenant_email.html',{"user":request.user,"tenant":tenant,"amount":payment.amount,"domain":current_domain})),
    return redirect('payments:generate-details', payment_id=payment_id)


def generate_physical_payemnt_details(request, payment_id):
    student = Student.objects.get(user=request.user)
    payment = get_object_or_404(PhysicalPaymentHistory, student=student, payment_id=payment_id)
    get_tenant = Tenant.objects.get(student=student)

    # room of tenant
    room = get_tenant.room

    #qrcode name for user after payments
    qrcode_name = f'media/auth_qrcodes/{request.user.username}-{get_tenant.tenant_id}-qrcode.png'

    #tittle of pdf page to be generated
    title = f"{request.user.username} Authentication details@Bookmie.com"

    #subtittle of the pdf 
    subtitle = f"Congratulation On Securing A Room @{get_tenant.hostel.hostel_name.capitalize()}"

    """Fucntions to generate a list strings containing booking details for every user"""
    booker_details= tenant_auth_details(student=student, 
                                        room=room, tenant=get_tenant, 
                                        reference=payment.reference
                                        )

    text_template = tenant_auth_message(student=student, 
                                        room=room, tenant=get_tenant)


    """CODES THAT GENERATE BOOKING PDF USING REPORT-LAB"""
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    #Title of auth pdf
    pdf.setTitle(title)
    pdf.setFont("Helvetica", 20)
    pdf.drawString(87, 730, title)

    #Subtitle of auth pdf
    pdf.setFont('Helvetica', 17)
    pdf.drawString(130, 690, subtitle)


    #tenant_details
    details = pdf.beginText(345, 635)
    details.setFont('Helvetica', 18)
    details.setFillColor(colors.black)
    ##############################
    #looping over a list of strings
    for detail in booker_details:
        details.textLine(detail)
    pdf.drawText(details)

    #Terms and Conditions content of pdf
    text = pdf.beginText(45, 350)
    text.setFont('Helvetica', 18)
    text.setFillColor(colors.black)
    for line in text_template:
        text.textLine(line)
    pdf.drawText(text)

    #generates qrcode for user
    qr_code_image = generate_qrcode(verification_code=get_tenant.verification_code)
    
    qr_code_image.save(qrcode_name)  # Save the QR code image
    # qrcode size and position on pdf
    pdf.drawImage(qrcode_name, 30, 370, width=300, height=300)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    #reponse to client with generated pdf
    response = HttpResponse(content_type='application/pdf') 
    response.write(buffer.getvalue())
    return response