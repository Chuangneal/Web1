import os.path

from django import template
from django.utils import timezone


register = template.Library()


@register.simple_tag
def add_str(str1, str2):
    return str(str1) + str(str2)


@register.simple_tag
def path_join(str1, str2):
    return os.path.join(str1, str2)


@register.simple_tag
def lower_str(str1):
    return str1.lower()


@register.simple_tag
def upper_str(str1):
    return str1.upper()


@register.simple_tag
def get_pub_time(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")

