
from management_app.models import SalesStatistics
from django.utils.timezone import now

def calculate_year_sales(hostel, amount_paid):
    sales, created = SalesStatistics.objects.get_or_create(hostel=hostel, year=now().year)
    if not created:
        sales.amount_made = float(sales.amount_made) + float(amount_paid)
        sales.save()
    else:
        sales.amount_made = float(sales.amount_made) + float(amount_paid)
        sales.save()



