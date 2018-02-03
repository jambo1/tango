from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.http import HttpResponse

def index(request):
    #Query the database for a list of categories used and order the categroies
    #by likes in ascending order and choose the top 5. The list is then put in the context dict
    #Dictionary to pass the template engine as it's context

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}


    #Return a rendered response making use of the shortcut function
    #First parameter is the template
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict= {'boldmessage' : "This tutorial has been put together by Jamie Gunn"}
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    #COntext Dictionary to pass to the template rendering ENGINE
    context_dict = {}

    try:
        #Look for category name which matches the slug. If it doesnt exit the .get()
        #method will raise a DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)

        #Return associated pages, filter() will return a list of page objects or an
        #empty list
        pages = Page.objects.filter(category=category)

        #Add results list to a template context under name pages
        context_dict['pages'] = pages
        #Add the category object from the database
        #to context dict. Used in the template to verify the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        #If category does not exist do nothing
        context_dict['category'] = None
        context_dict['pages'] = None
    #render response and return to the client
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    #A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Is the form valid?
        if form.is_valid():
            #Save category to database.
            form.save(commit=True)
            #Redirecting user to the index page confirms category is added as it appears there
            return index(request)
        else:
            print(form.errors)
    #Handles bad form, new form or no form supplied cases and renders messages
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
            return show_category(request, category_name_slug)
        else:
            print(forms.errors)
    else:
        form = PageForm()

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)
