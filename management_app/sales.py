# Fuction to convert sales into one json instaed of list of jsons
def convert_sales(sales):
    sale_dict = {}
    for sale in sales:
        sale_dict.update({int(sale.year): float(sale.amount_made)}) 
    return sale_dict