from django.shortcuts import render


def index(request):
    return render(request, 'peace/index.html', {'title': 'Home'})