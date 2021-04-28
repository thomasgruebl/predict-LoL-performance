from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hi, you are at the predict-LoL-performance main page.")

