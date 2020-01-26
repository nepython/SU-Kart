from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, WebsiteUser
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, SignInForm, ComplainForm
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend

def signup(request):
    User = None
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('name')
            DOB = request.POST.get('DOB')
            User = form.save(commit=False)
            User.currency = 0
            User.correspondent = None
            User.order = None
            #User = form.cleaned_data.get('DOB')
            User.save()
            print(User)
            user = authenticate(username=username, DOB=DOB)
            login(request, user)
            return redirect('Kart:product_list')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    #return render(request, 'Kart/home.html', {'form': form, 'user': User})


def signin(request) :
    #user = None
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            DOB = request.POST.get('DOB')
            print(DOB)
            #user = authenticate(username=username, password=DOB)
            try:
                user = WebsiteUser.objects.get(name=name)
                print(user.DOB, user.name)
                if user.name == request.POST['name']:
                    request.session['order'] = user.order
                    request.session['name'] = user.name
                    #return HttpResponse("You are logged in")
                    #login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                    #request.session['user'] = user
                    return redirect('Kart:product_list')
                else:
                    return HttpResponse("Name and DOB entered didn't match")
            except WebsiteUser.DoesNotExist:
                return HttpResponse("Username and DOB entered didn't match")


        else:
            print(form.errors)
    else:
        form = SignInForm()
    return render(request, 'Kart/signin.html', {'form': form})


def product_list(request) :
    products = Product.objects.all()
    return render(request, 'Kart/product/list.html',{'products': products})


def product_detail(request, title) :
    product = get_object_or_404(Product,
                                title=title)
    user = request.session["name"]
    new_complain = None
    complain_form = ComplainForm(data=request.POST)
    if (WebsiteUser.objects.filter(name=user)).exists():
        User = WebsiteUser.objects.get(name=user)

        if request.method == 'POST':
            # A complain was posted
            complain_form = ComplainForm(data=request.POST)
            if complain_form.is_valid():
                # Create Comment object but don't save to database yet
                new_complain = complain_form.save(commit=False)
                User.complain = new_complain.complain
                User.save()
    else:
        complain_form = ComplainForm()
    return render(request,
                  'Kart/product/detail.html',
                  {'product': product,
                   'complain_form': complain_form,
                   'new_complain': new_complain})


def searchposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(company__company__icontains=query)
            results = Product.objects.filter(lookups).distinct()
            context = {'results': results,
                       'submitbutton': submitbutton}
            return render(request, 'Kart/product/list.html', context)
        else:
            return render(request, 'Kart/product/list.html')
    else:
        return render(request, 'Kart/product/list.html')


def cart_order(request, title):
    user = request.session["name"]
    print(-1)
    if(WebsiteUser.objects.filter(name=user)).exists():
        product = (get_object_or_404(Product, title=title))
        User = WebsiteUser.objects.get(name=user)
        correspondent = WebsiteUser.objects.order_by('complain').get(Task = 'Delivery')
        if correspondent.complain == None:
            correspondent.complain=1
        else:
            n = int(correspondent.complain)
            correspondent.complain= n + 1
        correspondent.order = product
        correspondent.correspondent = User.name
        correspondent.save()
        User.correspondent = correspondent.name
        User.order = product
        User.save()
        request.session["order"] = "Placed"
        #context = {} #Need to add this
        return render(request, 'Kart/product/detail.html',{'product': product}, )
    else:
        return render(request, 'Kart/product/list.html',)

def cart_remove(request, title):
    user = request.session["name"]
    if(WebsiteUser.objects.filter(name=user)).exists():
        product = (get_object_or_404(Product, title=title))
        User = WebsiteUser.objects.get(name=user)
        User.order = None
        correspondent = WebsiteUser.objects.get(name = User.correspondent)

        #correspondent.complain-=1
        correspondent.order = None
        correspondent.correspondent = None
        n = int(correspondent.complain)
        correspondent.complain= n - 1
        if correspondent.complain == 0:
            correspondent.complain = None
        correspondent.save()
        User.correspondent = None
        User.save()
        del request.session["order"]
        #context = {} #Need to add this
        return render(request, 'Kart/product/detail.html', {'product': product})
    else:
        return render(request, 'Kart/product/list.html',)