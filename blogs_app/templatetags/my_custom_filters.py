from django import template

register = template.Library()


@register.filter(name='my_media')
def my_media(values):
    if values:
        return f'/media/{values}'

    return '#'
