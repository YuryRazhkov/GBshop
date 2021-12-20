from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        sourse_path = '/static/img/no_foto.bmp'
    else:
        sourse_path = f'{settings.MEDIA_URL}{avatar}'

    return sourse_path


def media_for_products(image):
    if not image:
        sourse_path = '/static/img/no_foto.bmp'
    else:
        sourse_path = f'{settings.MEDIA_URL}{image}'

    return sourse_path

register.filter('media_for_products', media_for_products)