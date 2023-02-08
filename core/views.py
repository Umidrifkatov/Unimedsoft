from django.shortcuts import render


def mainpage(request):
    return render(request, 'other/index.html')