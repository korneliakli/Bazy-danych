from django import template
import decimal

register = template.Library()

@register.simple_tag
def multiply(quantity, unit_cost):
    return round(quantity * unit_cost, 2)

@register.simple_tag
def multiply_discount(quantity, unit_cost, discount):
    discount = decimal.Decimal(discount)
    return round(quantity * unit_cost * discount, 2)

@register.simple_tag
def substract(minuend, substrahend):
    return minuend - substrahend