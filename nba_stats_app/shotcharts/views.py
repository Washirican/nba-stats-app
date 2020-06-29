from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Welcome to NBA Shotcharts</h1>')


def about(request):
    return HttpResponse('<h1>About NBA Shotcharts</h1>')
