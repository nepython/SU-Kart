from django.core.mail import send_mail
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, WebsiteUser
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, ComplainForm, UserRegisterForm
from django.urls import reverse
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from payments.models import Paytm_history


@transaction.atomic  #Rollsback all commits to the database when an exxception occurs
def signup(request):
    User = None
    request.session.flush()
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        additional_details = SignUpForm(data=request.POST)
        if form.is_valid() and additional_details.is_valid():
            print(1)
            username = request.POST.get('name')
            DOB = request.POST.get('DOB')
            User = form.save(commit=False)
            User.save()
            print(User.username)
            user_details = additional_details.save(commit=False)
            user_details.user = User
            user_details.currency = 0
            user_details.correspondent = None
            user_details.order = None

            #to be later done using one-to-one-field
            # User.websiteUser.Task = additional_details.cleaned_data.get('Task')
            # User.websiteUser.State = additional_details.cleaned_data.get('State')
            # User.websiteUser.City = additional_details.cleaned_data.get('City')
            # User.websiteUser.DOB = additional_details.cleaned_data.get('DOB')
            # User.websiteUser.UID = additional_details.cleaned_data.get('UID')
            #User = form.cleaned_data.get('DOB')
            #if(WebsiteUser.objects.get(name!=User.name)) :
            user_details.save()
                #new changed for email
            subject = 'SU Kart: Successfully Registered'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]
            to_user = [User.email]
            messsage = "Thanks for Registering in SU Kart. Your details submitted are:"
            registration_message = "{0}, Username {1} with Email {2}. HAPPY SHOPPING".format(messsage, User.username, User.email)
    ########        send_mail(subject, registration_message, from_email, to_user, fail_silently=True)
            #print(User)
            user = authenticate(username=User.username, password=User.password)
            #request.session['name'] = username
            login(request, User)
            return redirect('Kart:product_list')
            #else:
            #    return HttpResponse("Requested username already exists please enter a different name!")

        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
        additional_details = SignUpForm()
    return render(request, 'Kart/home.html', {'form': form,'additional_details': additional_details, 'user': User})


# def signin(request) :
#     #user = None
#     request.session.flush()
#     if request.method == 'POST':
#         form = SignInForm(data=request.POST)
#         if form.is_valid():
#             name = request.POST.get('name')
#             DOB = request.POST.get('DOB')
#             #print(DOB)
#             #user = authenticate(username=username, password=DOB)
#             try:
#                 user = WebsiteUser.objects.get(name=name)
#                 print(user.DOB, user.name)
#                 if user.name == request.POST['name']:
#                     request.session['order'] = user.order
#                     request.session['name'] = user.name
#                     #return HttpResponse("You are logged in")
#                     #login(request, user,backend='django.contrib.auth.backends.ModelBackend')
#                     #request.session['user'] = user
#                     return redirect('Kart:product_list')
#                 else:
#                     return HttpResponse("Name and DOB entered didn't match")
#             except WebsiteUser.DoesNotExist:
#                 return HttpResponse("Username and DOB entered didn't match")
#
#
#         else:
#             print(form.errors)
#     else:
#         form = SignInForm()
#     return render(request, 'Kart/signin.html', {'form': form})


def product_list(request) :
    products = Product.objects.all()
    return render(request, 'Kart/product/list.html',{'products': products})


def product_detail(request, title) :
    product = get_object_or_404(Product,
                                title=title)
    new_complain = None
    complain_form = ComplainForm(data=request.POST)
    try:
        user = request.session["name"]
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
    except KeyError:
        return redirect('/signin')
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
        #new changed for email
        subject = 'SU Kart: Successfully Placed order:'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_user = [User.Email]
        messsage = "Thanks for ordering in SU Kart. Your order placed is:"
        order_message = "{0}{1}, Delivery Boy: {2} with Email {3}. HAPPY SHOPPING".format(messsage, User.order, User.correspondent, correspondent.Email)
        send_mail(subject, order_message, from_email, to_user, fail_silently=False)

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
        correspondent = WebsiteUser.objects.get(name = User.correspondent)
        #new changed for email
        subject = 'SU Kart: Successfully removed order'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_user = [User.Email]
        messsage = "Thanks for shopping at SU Kart. Your order has been removed:"
        remove_message = "{0}{1}. HAPPY SHOPPING".format(messsage, User.order)
        send_mail(subject, remove_message, from_email, to_user, fail_silently=False)
     
        User.order = None

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
