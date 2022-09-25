
from django.http import HttpResponse
from django.shortcuts import redirect


def index(request):
    return HttpResponse("Welcome to Alpha's project... Please go to /polls")
