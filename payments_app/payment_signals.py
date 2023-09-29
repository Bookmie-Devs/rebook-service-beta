from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from hostel_app.models import HostelProfile
from payments_app.models import PaystackSubAccount
from payments_app.payStack import create_subaccount

@receiver(post_save, sender=HostelProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:

        #save created hostel paystack subaccount
        sub_account = PaystackSubAccount.objects.create(hostel=instance, 
                                    bussiness_name=str(instance.hostel_name).upper(),
                                          account_number = instance.account_number,)
        sub_account.save()

        create_subaccount(hostel=instance)
        print(create_subaccount(hostel=instance).json())

        if (create_subaccount(hostel=instance).json().get('message') == 'Subaccount created'and 
            create_subaccount(hostel=instance).json().get('status') == 'true'):

            sub_account.subaccount_code = create_subaccount.json()['subaccount_code']

            sub_account.save()

        else:
            sub_account.subaccount_code = "Code was not recieved from paystack"

            sub_account.save()

        

