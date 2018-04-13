import requests

from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='load_book')
def load_book(google_id):
    return requests.get(settings.GOOGLE_BOOKS_API + str(google_id) + '?fields=volumeInfo/title,volumeInfo/imageLinks/thumbnail').json
    