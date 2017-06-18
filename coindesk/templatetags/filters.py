from django import template

from datetime import datetime
from babel.dates import format_timedelta

register = template.Library()

@register.filter(name='ago')
def ago(date):
    delta = datetime.utcnow() - date
    return format_timedelta(delta, locale='en_US')
