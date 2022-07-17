from django import template
import datetime
date = datetime.datetime.now()
register = template.Library()

@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return date.strftime("%b. %d, %Y")
