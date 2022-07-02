from django import template


register = template.Library()


@register.filter(name='list_product')
def list_product(value):
    return ', '.join(value)

