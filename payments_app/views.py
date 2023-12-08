"""Custom imports"""
from django.http import HttpRequest
from .models import PaymentHistory, PaystackSubAccount
from rooms_app.models import RoomProfile
from core.qrcode import generate_qrcode
from config.sms import send_sms_message
from .payStack import (paystack_verification, 
                    #    redirect_payment
                       )
from core import forms
from core.models import Tenant
from core.models import Booking
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
    get_room = RoomProfile.objects.get(room_id=room_id)

    if request.method == 'POST':
        if get_room.occupied:
            messages.info(request, 'Sorry, room has just been occupied by someone, please select new one')
            # print(request.META.get(''))    
            # return redirect(request.META.get('HTTP_REFERER'))
            Booking.objects.get(user=request.user).delete()
            return redirect('accounts:booking-and-payments')
        else:
            if PaymentHistory.objects.filter(user=request.user, successful=False).exists():
                # check if there is an unsuccessful payment
                PaymentHistory.objects.get(user=request.user, successful=False).delete()
                    #save payment details
                payment = PaymentHistory.objects.create(user=request.user,
                                    email=request.POST.get('email'),amount=get_room.room_price,
                                    account_payed_to=get_room.hostel.account_number,
                                    room=get_room,hostel=get_room.hostel,)
                payment.save()
                return redirect('payments:make-payment', get_room.room_id)
            
            else:
                #save payment details
                payment = PaymentHistory.objects.create(user=request.user,
                                    email=request.POST.get('email'),
                                    amount=get_room.room_price,
                                    account_payed_to=get_room.hostel.account_number,
                                    room=get_room,
                                    hostel=get_room.hostel,
                                    )
                payment.save()
                            
                return redirect('payments:make-payment', get_room.room_id)
    # return redirect
    return render(request, 'payments/initiate_payment.html',
                                    {'room':get_room, 'form':forms.PaymentForm,  
                                    'user':request.user,})

@login_required()
def make_payment(request, room_id):
    get_room = RoomProfile.objects.get(room_id=room_id)
    subaccount = PaystackSubAccount.objects.get(hostel=get_room.hostel)
    payment = PaymentHistory.objects.get(user=request.user)

    # make payment ot subaccount
    return render(request=request,template_name='payments/make_payment.html', 
                  context={'room':get_room,'reference':payment.reference, 
                           'subaccount':subaccount.subaccount_code,
                           'user':request.user, 
                           'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY })

@login_required()
def verify_payment(request, reference):  
    payment = get_object_or_404(PaymentHistory, reference=reference)

    # room payed for 
    acquired_room = RoomProfile.objects.get(room_id=payment.room.room_id)

    # checkout validation from api response
    verify = paystack_verification(reference)
    if (verify.status_code==200 and 
        verify.json().get('message')=='Verification successful' and
        verify.json()['data'].get('status')=="success" and
        verify.json()['data'].get('amount')==payment.room.room_price*100):
        
    # create tenent object if reponse is positive
        tenant = Tenant.objects.create(user=request.user, room=payment.room,
                                            hostel=payment.hostel, payed=True,
                                            )
        tenant.save()

        #DECLARE SUCCESSFULL TRUE if PAYMENT WAS A SUCCESS
        payment.successful = True
        payment.save()
 
        # count active tenants in th room after user book
        count_members = Tenant.objects.filter(room=payment.room, end_date__lt=timezone.now()).count()

        # SET ROOM TO FULL IF CAPACITY HAS BEEN FIELED & REDUCE BED SPACE LEFT
        acquired_room.check_bed_spaces(count_members=count_members)

        # DELETE BOOKING FOR USER
        booking = Booking.objects.get(user=request.user)
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
    try:
        tenant_id = Tenant.objects.get(user=request.user).tenant_id
        get_tenant = Tenant.objects.get(tenant_id=tenant_id)

        # room of tenant
        room = get_tenant.room

        #qrcode name for user after payments
        qrcode_name = f'media/auth_qrcodes/{request.user.username} qrcode.png'

        #tittle of pdf page to be generated
        title = f"{request.user.username} Authentication details@Bookmie.com"

        #subtittle of the pdf 
        subtitle = f"Congratulation On Securing A Room @{get_tenant.hostel.hostel_name.capitalize()}"

        """Fucntions to generate a list strings containing booking details for every user"""
        booker_details= tenant_auth_details(user=request.user, 
                                            room=room, tenant=get_tenant)

        text_template = tenant_auth_message(user=request.user, 
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

  

