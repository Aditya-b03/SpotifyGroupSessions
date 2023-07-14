from django.shortcuts import render

# Create your views here.
def index(request , *args , **kwargs ):
    #render takes request and takes a template in side templates
    return render(request , 'frontend/index.html')