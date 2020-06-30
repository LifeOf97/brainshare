from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@stringfilter
def listify(value):
    # returns the value turned into a list of words
    return value.replace(" ", "").rsplit(",")


@stringfilter
def distinct(values):
    # return a list value with no duplicate data
    return list(dict.fromkeys(value))


register.filter('listify', listify)
register.filter('distinct', distinct)
