from django.template import Library
from utils import priceformatter, cart_tools

register = Library()

@register.filter
def formatted_price(val):
    return priceformatter.format_price(val)


@register.filter
def cart_total_qnt(cart):
    return cart_tools.cart_total_qnt(cart)


@register.filter
def cart_totals(cart):
    return cart_tools.cart_totals(cart)