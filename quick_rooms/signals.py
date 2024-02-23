
from django.dispatch import receiver
from django.db.models.signals import post_save

from payments_app.payStack import create_guest_house_subaccount
from .models import GuestHouse, PaystackGuestHouseSubAccount

@receiver(post_save, sender=GuestHouse)
def create_sub_account(sender, instance: GuestHouse, created, **kwargs):
    if created:
        if PaystackGuestHouseSubAccount.objects.filter(hostel=instance).exists():
            pass

        else:
            #save created hostel paystack subaccount
            sub_account = PaystackGuestHouseSubAccount.objects.create(hostel=instance, 
                                        bussiness_name=str(instance.name).upper(),
                                        bank_code = instance.bank_code,
                                        primary_contact_name=instance.phone,
                                        account_number = instance.account_number,)
            sub_account.save()

            #create paystack sub account for hostel
            paystack_auth = create_guest_house_subaccount(hostel=instance)
            
            # if sub_account is created(201)
            if paystack_auth.status_code == 201:
                sub_account.subaccount_code = paystack_auth.json()['data'].get('subaccount_code')

                sub_account.percentage_charge = paystack_auth.json()['data'].get('percentage_charge')

                sub_account.settlement_bank = paystack_auth.json()['data'].get('settlement_bank')

                sub_account.account_verified =True

                sub_account.save()

            else:   
                sub_account.subaccount_code = "Code was not recieved from paystack"

                sub_account.save()