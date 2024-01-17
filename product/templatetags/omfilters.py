from django.template import Library
from utils import priceformatter

register = Library()

@register.filter
def formatted_price(val):
    return priceformatter.format_price(val)