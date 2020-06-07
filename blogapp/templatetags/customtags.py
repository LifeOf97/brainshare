from django import template
import datetime

register = template.Library()


@register.simple_tag
def get_date(value):
    # custom template tag to get a date in string format
    # and convert it to a python date type and assign to a
    # variable in the template it should be in the format
    # YYYY-MM-DD
    date = value.rsplit('-')
    return datetime.date(int(date[0]), int(date[1]), int(date[2]))
