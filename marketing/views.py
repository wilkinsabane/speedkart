from django.http import HttpResponse
from skart.settings import BASE_DIR
import os


ROBOTS_PATH = os.path.join(BASE_DIR, 'marketing/robots.txt')


def robots(request):
    return HttpResponse(open(ROBOTS_PATH).read(), 'text/plain')