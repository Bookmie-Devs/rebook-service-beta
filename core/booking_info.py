

def booking_email(user=None, booking_id=None, EMAIL_HOST_USER=None):

    #IMPORTS
    from.models import Booking
    from django.template.loader import render_to_string
    from django.core.mail import send_mail

    get_booking = Booking.objects.get(user =user)
    template = render_to_string('emails/booking_email.html', {'name':user.username, 'booking':get_booking})
    subject = f'Booking was successfull Mr. {user.username}'
    message = template
    from_email = EMAIL_HOST_USER
    
    return send_mail(fail_silently=True ,subject=subject, message=message,
                                                from_email=from_email, 
                                                recipient_list=[user.email])