from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    #Dictionary to pass the template engine as it's context
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    #Return a rendered response making use of the shortcut function
    #First parameter is the template
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict= {'boldmessage' : "This tutorial has been put together by Jamie Gunn"}
    return render(request, 'rango/about.html', context=context_dict)
