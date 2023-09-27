from django.shortcuts import render, redirect
from .models import PaymentHistory
from rooms_app.models import RoomProfile
from core.models import Tenant
from django.conf import settings
from django.shortcuts import get_object_or_404
import requests
from django.template.loader import render_to_string
from django.conf import settings
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
from config.qrcode import generate_qrcode


# stripe.
@login_required(login_url="accounts:login")
def initiate_payment(request, room_id):
    get_room = RoomProfile.objects.get(room_id=room_id)

    if request.method == 'POST':
        #save payment deatails
        payment = PaymentHistory.objects.create(user=request.user,email=request.user.email,
                                                amount=get_room.room_price,
                                                account_payed_to=get_room.hostel.bank_details,
                                                room=get_room,
                                                hostel=get_room.hostel,
                                                ).save()
        return redirect('payments:make-payment', get_room.room_id )
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
def verify_payment_success(request, reference):   
    get_response = requests.get()
    # status = requests.get
    PaymentHistory.reference
    payment = get_object_or_404(PaymentHistory, reference=reference)
    if get_response.status_code == 200:
        tenant = Tenant.objects.create(user=request.user, room=payment.room,
                                       hostel=payment.hostel, payed=True,
                                       ).save()

        subject=f'Congratulation {request.user.username}'
        body = render_to_string('text_templates/tenant_email.html', {'name':request.user.username})
        send_mail(subject=subject, message=body,from_email=settings.EMAIL_HOST_USER,recipient_list=['request.user.email'])
    pass

    subject = f''
    send_mail(from_email=settings.EMAIL_HOST_USER, 
    recipient_list=[request.user.email], subject=subject, 
    message=render_to_string('TextTemplates/TenantEamil.html',{"user":request.user}))

            
     
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

