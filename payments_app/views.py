"""Custom imports"""
from django.http import HttpRequest
from .models import PaymentHistory, PaystackSubAccount
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
from .tenant_auth import (tenant_auth_details, 
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
def initiate_payment(request: HttpRequest, room_id):
    student = Student.objects.get(user=request.user)
    booking = Booking.objects.get(student=student)
    room = RoomProfile.objects.get(room_id=room_id)
    if booking._has_expired():
        booking.delete()
        messages.info(request, 'Sorry, Booking has expired please book another room', extra_tags="danger")
        return redirect('accounts:booking-and-payments')

    if request.method == 'POST':
        """
        Check if booking is for upadting vcode
        and create a new payment history and skip the
        check for if room is occupied (beacuse at the time of update it will surely be occcupied)
        """
        if booking.is_updating_vcode:
            #save payment details
            payment = PaymentHistory.objects.create(student=student,
                                email=request.POST.get('email'),
                                amount=room.ptf_room_price,
                                account_payed_to=room.hostel.account_number,
                                room=room,
                                hostel=room.hostel,)
            payment.save()            
            return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)

        elif room.occupied:
            messages.info(request, 'Sorry, room has just been occupied by someone, please select new one')
            booking.delete()
            return redirect('accounts:booking-and-payments')

        else:
            if PaymentHistory.objects.filter(student=student, successful=False).exists():
                # check if there is an unsuccessful payment
                PaymentHistory.objects.filter(student=student, successful=False).delete()
                    #save payment details
                payment = PaymentHistory.objects.create(student=student,
                                    email=request.POST.get('email'),amount=room.ptf_room_price,
                                    account_payed_to=room.hostel.account_number,
                                    room=room,hostel=room.hostel,)
                payment.save()
                return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)
            else:
                #save payment details
                payment = PaymentHistory.objects.create(student=student,
                                    email=request.POST.get('email'),
                                    amount=room.ptf_room_price,
                                    account_payed_to=room.hostel.account_number,
                                    room=room,
                                    hostel=room.hostel,
                                    )
                payment.save()            
                return redirect('payments:make-payment', reference_id=payment.reference_id, room_id=room.room_id)
            
    # return redirect
    is_part_payment = False
    return render(request, 'payments/initiate_payment.html',{'room':room, 'student':student,'is_part_payment': is_part_payment})

@login_required()
def make_payment(request: HttpRequest, reference_id,  room_id):
    student = Student.objects.get(user=request.user)
    room = RoomProfile.objects.get(room_id=room_id)
    payment = get_object_or_404(PaymentHistory, student=student, reference_id=reference_id)
    subaccount = PaystackSubAccount.objects.get(hostel=room.hostel)
    # make payment ot subaccount
    return render(request=request,template_name='payments/make_payment.html', 
                  context={'amount':payment.amount,'reference_id': reference_id, 
                           'subaccount':subaccount.subaccount_code,
                           'student':student, 'is_completing_payment':False,
                           'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY })

@login_required()
def verify_payment(request: HttpRequest, reference_id, paystack_reference):  
    student = Student.objects.get(user=request.user)
    """
    To prevent more than one payament history being query use user
    and referene_id to query history after payment is made
    """
    payment = get_object_or_404(PaymentHistory, student=student, reference_id=reference_id)

    # room payed for    
    acquired_room = RoomProfile.objects.get(room_id=payment.room.room_id)

    # checkout validation from api response after passing paystack_reference
    response_data = paystack_verification(paystack_reference)
    # confrim payment
    if payment_is_confirm(data=response_data, amount=payment.amount):
        # create tenent object if reponse is positive
        if payment.is_half_payment:
            tenant = Tenant.objects.create(student=student, room=payment.room,
                                        hostel=payment.hostel, payed=True, made_part_payment=True,
                                        amount_left_to_pay=payment.amount)
            tenant.save()
        else:
            tenant = Tenant.objects.create(student=student, room=payment.room, hostel=payment.hostel, payed=True, completed_payment=True)
            tenant.save()
        # calculate sales on each payment
        calculate_year_sales(hostel=payment.hostel,amount_paid=payment.room.room_price)
        # agent sales
        calculate_agent_year_sales(hostel=payment.hostel, amount_paid=payment.room.room_price)

        #DECLARE SUCCESSFULL TRUE if PAYMENT WAS A SUCCESS
        payment.paystack_reference = paystack_reference
        payment.successful = True
        payment.completed_full_payment =True
        payment.save()
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
        return redirect('core:success')
    
    else:
        payment.delete()
        messages.info(request, "payment was not successfull, try again")
        return redirect('accounts:booking-and-payments')

            
@login_required()
def tenant_auth(request):
    student = Student.objects.get(user=request.user)
    try:
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
                                            room=room, tenant=get_tenant)

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
    
    except Tenant.DoesNotExist:
        messages.info(request, "You are not a tenant to get verification")
        return redirect('accounts:booking-and-payments')

  

