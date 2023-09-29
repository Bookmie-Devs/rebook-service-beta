from django.shortcuts import render, redirect
from .models import PaymentHistory
from rooms_app.models import RoomProfile
from core.models import Tenant
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from django.template.loader import render_to_string
from django.conf import settings
from core.models import Booking

from .tenant_auth import (tenant_auth_details, 
                          tenant_auth_message)

from reportlab.lib.pagesizes import letter
from core import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.conf import settings
from reportlab.lib import colors
from core.qrcode import generate_qrcode
from .payStack import (paystack_verification, 
                       redirect_payment)


# stripe.
@login_required(login_url="accounts:login")
def initiate_payment(request, room_id):
    get_room = RoomProfile.objects.get(room_id=room_id)

    if request.method == 'POST':
        if PaymentHistory.objects.filter(user=request.user).exists():
            return redirect('payments:make-payment', get_room.room_id)
        
        else:
            #save payment deatails
            payment = PaymentHistory.objects.create(user=request.user,email=request.user.email,
                                                    amount=get_room.room_price,
                                                    account_payed_to=get_room.hostel.account_number,
                                                    room=get_room,
                                                    hostel=get_room.hostel,
                                                    ).save()
            return redirect('payments:make-payment', get_room.room_id)
    # return redirect
    return render(request, 'payments/initiate_payment.html',
                                    {'room':get_room, 'form':forms.PaymentForm,  
                                    'user':request.user,})

@login_required(login_url="accounts:login")
def make_payment(request, room_id):
    get_room = RoomProfile.objects.get(room_id=room_id)
    payment = PaymentHistory.objects.get(user=request.user)
    
    return render(request, 'payments/make_payment.html', 
                            {'room':get_room,
                             'reference':payment.payment_id, 
                            'user':request.user, 
                            'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY })


@login_required(login_url='accounts:login')
def verify_payment(request, reference):   
    payment = get_object_or_404(PaymentHistory, payment_id=reference)

    account = redirect_payment(customer=request.user, 
                                        room=payment.room,
                                        hostel=payment.hostel)
    print(payment)

    # checkout validation from api response
    verify = paystack_verification(reference)

    if (verify.status_code==200 and 
        verify.json().get('message')=='Verification successful' and
        verify.json()['data']['amount']==payment.room.room_price*100):

    # check if payment was redirected to hostel account
            if (redirect_payment(account.status_code == 200
                                 and account.json()['status']==True)):
            
    # create tenent object if reponse is positive
                tenant = Tenant.objects.create(user=request.user, room=payment.room,
                                            hostel=payment.hostel, payed=True,
                                            ).save()
        
                # SET BOOKING STATUS TO PAYED
                booking = Booking.objects.get(user=request.user)
                booking.payed =True
                booking.save()

                #DECLARE SUCCESSFULL TRUE if PAYMENT WAS A SUCCESS
                payment.successfull = True
                payment.save()
                pass
            else:
                payment.delete()
                messages.info(request, "payment was not successfull")
                return redirect('payments:init-payment', payment.room.room_id)
    else:
        payment.delete()
        messages.info(request, "payment was not successfull")
        return redirect('payments:init-payment', payment.room.room_id)

    #send email
    subject = f'Congratulations'
    send_mail(from_email=settings.EMAIL_HOST_USER, fail_silently=True,
    recipient_list=[request.user.email], subject=subject, 
    message=render_to_string('emails/tenant_email.html',{"user":request.user}))

    return redirect('payments:tenant-authentication')

            
@login_required(login_url='accounts:login')
def tenant_auth(request):
    tenant_id = Tenant.objects.get(user=request.user).tenant_id
    get_tenant = Tenant.objects.get(tenant_id=tenant_id)
    room = get_tenant.room

    #qrcode name for user after payments
    qrcode_name = f'VerificationFiles/Ver_Qrcodes/{request.user.username} qrcode.png'

    #tittle of pdf page to be generated
    title = f"{request.user.username} Authentication details"

    #subtittle of the pdf 
    subtitle = 'www.GuudNyt.com'

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
    pdf.drawString(145, 730, title)

    #Subtitle of auth pdf
    pdf.setFont('Helvetica', 15)
    pdf.drawString(250, 699, subtitle)

    #tenant_details
    details = pdf.beginText(290, 660)
    details.setFont('Helvetica', 18)
    details.setFillColor(colors.black)
    ##############################
    #looping over a list of strings
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
    qr_code_image = generate_qrcode(get_tenant.tenant_id)
    qr_code_image.save(qrcode_name)  # Save the QR code image
    pdf.drawImage(qrcode_name, 50, 490, width=200, height=200)
    pdf.showPage()
    pdf.save()
    buffer.seek(0)

    #reponse to client with generated pdf
    response = HttpResponse(content_type='application/pdf') 
    response.write(buffer.getvalue())
    return response

