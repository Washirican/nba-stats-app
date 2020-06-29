from django.shortcuts import render
from django.http import HttpResponse


players = [
    {
        'first_name': 'Kobe',
        'last_name': 'Bryant',
        'team_id': 50,
    },
    {
        'first_name': 'Michael',
        'last_name': 'Jordan',
        'team_id': 50,
    }
]
def home(request):
    context = {
    'players': players
    }

    return render(request, 'shotcharts/home.html', context)


def about(request):
    return render(request, 'shotcharts/about.html')
