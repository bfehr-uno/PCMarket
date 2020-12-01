from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db import IntegrityError

from Listings.models import *
import datetime

def current_listings(request):
    listings = CurrentListing.objects.all()
    return render(request, "CurrentListings.html", {'listings': listings})

def single_listing(request, listing_id):
    listing = CurrentListing.objects.get(pk=listing_id)
    return render(request, "SingleListing.html", {"listing": listing})

def easy_buy(request):
    return render(request, "EasyBuy.html")

def sell(request):
    return render(request, "Sell.html")

def sale_history(request):
    return render(request, "SaleHistory.html")

def follow(request):
    return render(request, "Follow.html")

def create_account(request):
    return render(request, "CreateAccount.html")

def login(request):
    return render(request, "Login.html")

def account(request):
    # check if the user is already logged in
    if request.user.is_anonymous == False:
        user = request.user
        print(user.email)
        for purchase in user.purchases.all():
            print(purchase.model_name)
        return render(request, 'Account.html')

    # check if is arriving from the login page or the create account page
    previous_page = request.META['HTTP_REFERER'][22:]
    print(previous_page)
    if (previous_page == "Login"):
        email = request.POST['email']
        password = request.POST['password']

        # check if there are any missing fields
        if email == "" or password == "":
            return render(request, previous_page, {'missing_fields': True})
        else:  
            try:
                user = User.objects.raw("select * from Listings_user where email = %s and password = %s", [email, password])[0]
                auth_login(request, user)
                return render(request, "Account.html")
            except IndexError:
                return render(request, previous_page  + ".html", {'invalid_user': True})
    else:  
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']  

        # check if there are any missing fields
        if name == "" or email == "" or password == "":
            return render(request, previous_page  + ".html", {'missing_fields': True})

        # check if email is already in use
        else: 
            try:
                user = User(email=email, name=name, password=password)
                User.save(user)
                auth_login(request, user)
                return render(request, "Account.html", {'user': user})
            except IntegrityError:
                return render(request, "CreateAccount.html", {'email_used': True})

def purchase(request, listing_id):
    # get listing
    current_listing = CurrentListing.objects.get(pk=listing_id)
    # get listing's user and user who is purchasing the part
    listings_user = current_listing.user_set.first()
    user = request.user
    # add to the user's purchases and the other users's sold listings and remove from current listings
    SoldListing.objects.create(part_type=current_listing.part_type, model_name=current_listing.model_name, price=current_listing.price)
    current_listing.delete()
    sold_listing = SoldListing.objects.last()
    user.purchases.add(sold_listing)
    listings_user.sold_listings.add(sold_listing)
    return render(request, "Purchase.html", {'listing': sold_listing})

def list_part(request, part_type):
    if part_type == "CPU":
        model_name = request.POST["model_name"]
        price = request.POST["price"]
        num_cores = request.POST["num_of_cores"]
        frequency = request.POST["frequency"]
        socket = request.POST["socket"]
        CurrentListing.objects.create(part_type="CPU", model_name=model_name, price=price, attrs={'number of cores': num_cores, 'frequency': frequency, 'socket': socket})
    elif (part_type == "GPU"):
        model_name = request.POST["model_name"]
        price = request.POST["price"]
        clock_speed = request.POST["clock_speed"]
        interface= request.POST["interface"]
        memory = request.POST["memory"]
        CurrentListing.objects.create(part_type="GPU", model_name=model_name, price=price, attrs={'clock speed': clock_speed, 'interface': interface, 'memory': memory})
    elif (part_type == "Hard Drive"):
        model_name = request.POST["model_name"]
        price = request.POST["price"]
        storage = request.POST["storage"]
        rpm = request.POST["rpm"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'storage': storage, 'rotations per minute': rpm})
    elif (part_type == "Motherboard"):
        model_name = request.POST["model_name"]
        price = request.POST["price"]
        socket = request.POST["socket"]
        expansion = request.POST["expansion_slots"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'socket type': socket, 'expansion slots': expansion})
    else:
        model_name = request.POST["model_name"]
        price = request.POST["price"]
        capacity = request.POST["capacity"]
        typ = request.POST["type"]
        speed = request.POST["speed"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'capacity': capacity, 'type': typ, 'speed': speed})
    listing = CurrentListing.objects.last()
    user = request.user
    user.current_listings.add(listing)
    return render(request, 'SingleListing.html', {'listing': listing, 'just_listed': True})

def find_cheapest(request, part_type):
    if part_type == "CPU":
        num_cores = request.POST["num_of_cores"]
        frequency = request.POST["frequency"]
        socket = request.POST["socket"]
        try: 
            matches = CurrentListing.objects.get(attrs__num_cores=num_cores, attrs__frequency=frequency, attrs__socket=socket)
        except ObjectDoesNotExist:
            return render(request, "EasyBuy.html", {'no_matches': true})
    elif (part_type == "GPU"):
        clock_speed = request.POST["clock_speed"]
        interface= request.POST["interface"]
        memory = request.POST["memory"]
        CurrentListing.objects.create(part_type="GPU", model_name=model_name, price=price, attrs={'clock speed': clock_speed, 'interface': interface, 'memory': memory})
    elif (part_type == "Hard Drive"):
        storage = request.POST["storage"]
        rpm = request.POST["rpm"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'storage': storage, 'rotations per minute': rpm})
    elif (part_type == "Motherboard"):
        socket = request.POST["socket"]
        expansion = request.POST["expansion_slots"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'socket type': socket, 'expansion slots': expansion})
    else:
        capacity = request.POST["capacity"]
        typ = request.POST["type"]
        speed = request.POST["speed"]
        CurrentListing.objects.create(part_type="Hard Drive", model_name=model_name, price=price, attrs={'capacity': capacity, 'type': typ, 'speed': speed})