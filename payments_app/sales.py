from agents_app.models import AgentSale
from hostel_app.models import SalesStatistics
from hostel_app.models import HostelProfile
from django.utils.timezone import now

def calculate_year_sales(hostel: HostelProfile, amount_paid):
    sales, created = SalesStatistics.objects.get_or_create(hostel=hostel, year=now().year)
    if not created:
        sales.amount_made = float(sales.amount_made) + float(amount_paid)
        sales.save()
    else:
        sales.amount_made = float(sales.amount_made) + float(amount_paid)
        sales.save()



def calculate_agent_year_sales(hostel: HostelProfile):
    try:
        sales, created = AgentSale.objects.get_or_create(agent=hostel.agent_affiliate, year=now().year)
        if not created:
            sales.number_of_sales = int(sales.number_of_sales) + 1
            sales.save()
        else:
            sales.number_of_sales = int(sales.number_of_sales) + 1
            sales.save()
    except:
        pass