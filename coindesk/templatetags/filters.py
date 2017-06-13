from django import template

from urlparse import urlparse
from datetime import datetime
from babel.dates import format_timedelta

register = template.Library()

@register.filter(name='domain')
def domain(url):
    return '.'.join(urlparse(url).netloc.split('.')[-2:])

@register.filter(name='ago')
def ago(date):
    delta = datetime.utcnow() - date
    return format_timedelta(delta, locale='en_US')
