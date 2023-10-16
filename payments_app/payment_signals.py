from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from hostel_app.models import HostelProfile
from payments_app.models import PaystackSubAccount
from payments_app.payStack import create_subaccount

@receiver(post_save, sender=HostelProfile)
def create_sub_account(sender, instance, created, **kwargs):
    if created:

        if PaystackSubAccount.objects.filter(hostel=instance).exists():
            pass

        else:
            #save created hostel paystack subaccount
            sub_account = PaystackSubAccount.objects.create(hostel=instance, 
                                        bussiness_name=str(instance.hostel_name).upper(),
                                        bank_code = instance.bank_code,
                                            account_number = instance.account_number,)
            sub_account.save()

            #create paystack sub account for hostel
            paystack_auth = create_subaccount(hostel=instance)

            if paystack_auth.status_code == 201:

                sub_account.subaccount_code = paystack_auth.json()['data'].get('subaccount_code')

                sub_account.percentage_charge = paystack_auth.json()['data'].get('percentage_charge')

                sub_account.settlement_bank = paystack_auth.json()['data'].get('settlement_bank')

                sub_account.account_verified =True

                sub_account.save()

            else:   
                sub_account.subaccount_code = "Code was not recieved from paystack"

                sub_account.save()

            

