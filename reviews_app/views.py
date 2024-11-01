from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from accounts.task import send_email_task
from hostel_app.models import HostelProfile
from .models import FeedBackMessage, CustomerCare, HostelLike
from core.decorators import login_required_htmx
from django.http import HttpRequest
from .notify import NotifyMe
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods


def feedback_message(request: HttpRequest):
    message = FeedBackMessage.objects.create(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                message=request.POST.get("message")
                )
    message.save()

    # send nofification
    notify = NotifyMe(name=request.POST.get("name"),
                    phone=request.POST.get("phone"),
                    subject="Feedback/Issues",
                    message=request.POST.get("message"),
                    date=message.date_sent
                    )
    notify.notify_by_email()

    return render(request, 'htmx_message_templates/feedback_message.html', {"message":"Message dilivered"})


"""Customer issues"""
def customer_care(request: HttpRequest):
    message = CustomerCare.objects.create(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                problem=request.POST.get("message")
                )
    message.save()
    send_email_task('The Bookmie Support Team', 
    render_to_string('emails/customer_care_reponse.html'), 
    settings.EMAIL_HOST_USER, 
    [message.email,]
    )

    # send nofification
    notify = NotifyMe(name=request.POST.get("name"),
                      phone=request.POST.get("phone"),
                      subject="Customer Care",
                      message=request.POST.get("message"),
                      date=message.date_sent
                      )
    notify.notify_by_email()

    return render(request, 'htmx_message_templates/feedback_message.html', {"message":"Issue Reported"})


@login_required_htmx
@require_http_methods(['POST'])
def like_hostel(request: HttpRequest):
    hostel = HostelProfile.objects.get(hostel_code=request.POST.get('hostel_code'))
    if HostelLike.objects.filter(user=request.user, hostel=hostel).exists():
        hostel.no_of_likes-=1
        hostel.save()
        HostelLike.objects.get(user=request.user, hostel=hostel).delete()
        return render(request, 'htmx_message_templates/like_htmx.html', {'hostel':hostel,'decreasing':True})
    else:
        liked = HostelLike.objects.create(hostel=hostel, user=request.user)
        liked.save()
        hostel.no_of_likes+=1
        hostel.save() 
        return render(request, 'htmx_message_templates/like_htmx.html', {'hostel':hostel,'decreasing':False})



@require_http_methods(['POST'])
def news_letter(request: HttpRequest):
    from .models import NewsletterEmails
    news_letter = NewsletterEmails.objects.create(email=request.POST.get('email'))
    news_letter.save()
    return render(request, 'htmx_message_templates/feedback_message.html', {"message":"Email Submitted"})


class ContactView(TemplateView):
    
    template_name = 'home/contact.html'
