from django.shortcuts import render

def phantom_check(request):
    return render(request, 'phantom_check.html')
