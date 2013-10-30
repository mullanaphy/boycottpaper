from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def site(name):
    if name in settings.SITE:
        return settings.SITE[name]
    else:
        return ""
