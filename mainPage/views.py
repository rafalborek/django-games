from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
# Create your views here.

def index(request):
    """
    home page
    """
    return render(request, 'mainPage/index.html',{ })





  