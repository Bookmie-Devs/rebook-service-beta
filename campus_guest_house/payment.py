
from core.qrcode import generate_qrcode
"""Custom imports"""
from django.http import HttpRequest
from .models import GuestHouseRooms, PaymentHistory, PaystackSubAccount
from rooms_app.models import RoomProfile
from core.qrcode import generate_qrcode
from config.sms import send_sms_message
from payments_app.payStack import (paystack_verification, 
                    #    redirect_payment
                       )
from core import forms
from .models import GuestBooking
from hostel_app.models import HostelProfile
from payments_app.tenant_auth import (tenant_auth_details, 
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
    room = RoomProfile.objects.get(room_id=room_id)

    if request.method == 'POST':
        if room.occupied:
            messages.info(request, 'Sorry, room has just been occupied by someone, please select new one')
            # print(request.META.get(''))    
            # return redirect(request.META.get('HTTP_REFERER'))
            GuestBooking.objects.get(user=request.user).delete()
            return redirect('accounts:booking-and-payments')
        else:
            if PaymentHistory.objects.filter(user=request.user, successful=False).exists():
                # check if there is an unsuccessful payment
                PaymentHistory.objects.get(user=request.user, successful=False).delete()
                    #save payment details
                payment = PaymentHistory.objects.create(user=request.user,
                                    email=request.POST.get('email'),amount=room.ptf_room_price,
                                    account_payed_to=room.hostel.account_number,
                                    room=room,hostel=room.hostel,)
                payment.save()
                return redirect('payments:make-payment', room.room_id)
            
            else:
                #save payment details
                payment = PaymentHistory.objects.create(user=request.user,
                                    email=request.POST.get('email'),
                                    amount=room.ptf_room_price,
                                    account_payed_to=room.hostel.account_number,
                                    room=room,
                                    hostel=room.hostel,
                                    )
                payment.save()
                            
                return redirect('payments:make-payment', room.room_id)
    # return redirect
    return render(request, 'payments/initiate_payment.html',
                                    {'room':room, 'user':request.user,})

@login_required()
def make_payment(request, room_id):
    room = RoomProfile.objects.get(room_id=room_id)
    subaccount = PaystackSubAccount.objects.get(hostel=room.hostel)
    payment = PaymentHistory.objects.get(user=request.user)

    # make payment ot subaccount
    return render(request=request,template_name='payments/make_payment.html', 
                  context={'room':room,'reference':payment.reference, 
                           'subaccount':subaccount.subaccount_code,
                           'user':request.user, 
                           'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY })

@login_required()
def verify_payment(request, reference):  
    payment = get_object_or_404(PaymentHistory, reference=reference)

    # room payed for 
    acquired_room = GuestHouseRooms.objects.get(room_id=payment.room.room_id)

    # checkout validation from api response
    verify = paystack_verification(reference)
    if (verify.status_code==200 and 
        verify.json().get('message')=='Verification successful' and
        verify.json()['data'].get('status')=="success" and
        verify.json()['data'].get('amount')==payment.room.ptf_room_price*100):
        
        # create tenent object if reponse is positive
        guest_booking = GuestBooking.objects.get(user=request.user)
        guest_booking.payed = True
        guest_booking.save()

        #DECLARE SUCCESSFULL TRUE if PAYMENT WAS A SUCCESS
        payment.successful = True
        payment.save()

        current_domain = request.META.get('HTTP_X_FORWARDED_HOST', request.META['HTTP_HOST'])
        # send sms
        msg = render_to_string('emails/tenant_sms.html',{"user":request.user,"tenant":guest_booking,"amount":payment.amount,"domain":current_domain})
        send_sms_message(user_contact=request.user.phone, msg=msg)
        # send sms to manager
        manager_msg = render_to_string('emails/hostel_manager_msg.html',{'manager':guest_booking.guest_house.manager,
                                                                         'tenant':guest_booking})
        send_sms_message(user_contact=guest_booking.guest_user.phone,msg=manager_msg)

    else:
        payment.delete()
        messages.info(request, "payment was not successfull, try again")
        return redirect('accounts:booking-and-payments')

            
@login_required()
def tenant_auth(request):
    try:
        tenant_id = GuestBooking.objects.get(user=request.user).tenant_id
        get_tenant = GuestBooking.objects.get(tenant_id=tenant_id)

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
    
    except GuestBooking.DoesNotExist:
        messages.info(request, "You are not a tenant to get verification")
        return redirect('accounts:booking-and-payments')

  

