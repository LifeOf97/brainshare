from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@stringfilter
def listify(value):
    # returns the value turned into a list of words
    return value.rsplit(",")


register.filter('listify', listify)
