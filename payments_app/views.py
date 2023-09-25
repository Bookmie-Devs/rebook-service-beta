from django.shortcuts import render, redirect
from .models import PaymentHistory
from rooms_app.models import RoomProfile
from core.models import Tenant
from django.conf import settings
import requests
# from Core.froms import PaymentForm
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
from core.qrcode import generate_qrcode


# stripe.
paystack_endpoint = ''
PaymentHistory.amount
def initiate_payment(request, room_id):
    get_room = RoomProfile.objects.get(room_id=room_id)
    if request.method == 'POST': 
        # if request.POST.get('amount') == str(get_room.Room_Price):
        Payment = PaymentHistory.objects.create(user=request.user, amount=get_room.Room_Price, 
        room=get_room, hostel=get_room.Hostel, email=request.user.email)
        Payment.save()
        return render(request, 'make_payment.html', 
                              {'room':get_room, 'form':forms.PaymentForm, 
                               'payment':Payment, 'user':request.user, 
                               'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY })
    
    return render(request, 'initiate_payment.html',{'room':get_room, 'form':forms.PaymentForm,  'user':request.user })

def make_payment(request, reference):
    pass


@login_required(login_url='accounts:login')
def verify_payment_success(request, reference):
    get_response = requests.get(paystack_endpoint)
    # status = requests.get
    
    if get_response.status_code == 200:
        pass

    subject=f'Congratulation {request.user.username}'
    body = render_to_string('text_templates/tenant_email.html', {'name':request.user.username})
    send_mail(subject=subject, message=body,from_email=settings.EMAIL_HOST_USER,recipient_list=['request.user.email'])
    pass

    subject = f''
    send_mail(from_email=settings.EMAIL_HOST_USER, 
    recipient_list=[request.user.email], subject=subject, 
    message=render_to_string('TextTemplates/TenantEamil.html',{"user":request.user}))

            
     
def tenat_auth(request):
    tenant_id = Tenant.objects.get(user=request.user).tenant_id
    get_tenant = Tenant.objects.get(tenant_id=tenant_id)
    room = get_tenant.Room

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

