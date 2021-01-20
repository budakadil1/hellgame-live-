from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache

@never_cache




def about(request):
    return HttpResponse('HellGAME is an account sales platform with %100 secure transactions: guaranteed.')

def homepage(request):
    # RETURN RENDER to index.html
    return render(request, 'index.html')

