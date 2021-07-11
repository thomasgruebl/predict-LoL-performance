from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'lol/index.html')


def about(request):
    return render(request, 'lol/about.html')
