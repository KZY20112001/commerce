from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User, Auction_listing, Bid, Comment
from .forms import ListingForm, BidForm

def index(request):
    return render(request, "auctions/index.html", {
        'title' : "Active Listings",
        'listings': Auction_listing.objects.filter(closed=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        try:
            new_listing = form.save(commit=False)
            assert request.user.is_authenticated
            new_listing.owner = request.user
            new_listing.save()
            messages.success(request, "Your listing has been saved")
            return HttpResponseRedirect(reverse("index")) #redirect back to index
        except ValueError:
            pass

    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def show_listing(request, listing_id, bid_form = None):
    listing = Auction_listing.objects.get(pk=listing_id)
    if request.user.is_authenticated:
        is_watchlist = request.user.watchlist_listings.filter(pk = listing_id).exists()
        if not bid_form:
            bid_form = BidForm()
        is_owner = (request.user == listing.owner)
    else:
        is_watchlist = None
        is_owner = None
        bid_form = None

    return render(request, "auctions/listing.html",{
        "listing" : listing,
        "is_watchlist": is_watchlist,
        "is_owner" : is_owner,
        "form" : bid_form
    })


@login_required
def create_bid(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        listing = Auction_listing.objects.get(pk=listing_id)
        bid= Bid(user=request.user,listing=listing)
        bid_form = BidForm(request.POST, instance = bid)
        if bid_form.is_valid():
            bid_form.save()
            messages.success(request,"Your bid has been successfully made")
        else:
            return show_listing(request,listing_id, bid_form= bid_form)

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def close_bid(request, listing_id):
    if request.method == "POST":

        assert request.user.is_authenticated
        listing = Auction_listing.objects.get(pk=listing_id)
        if listing.owner == request.user:
            listing.closed = True
            listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def comment(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        listing = Auction_listing.objects.get(pk=listing_id)
        comment= Comment(user=request.user, listing=listing, content=request.POST["comment"])
        comment.save()

    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(reqeust):
    assert request.user.is_authenticated
    return render(request, "auctions/index.html",{
        "title":"Watchlist Items",
        "listings" : request.user.watchlist_listings.all()
    })

@login_required
def watchlist_edit(request, listing_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        listing = Auction_listing.objects.get(pk = listing_id)
        user = request.user
        if user.watchlist_listings.filter(pk=listing_id).exists():
            user.watchlist_listings.remove(listing)
        else:
            user.watchlist_listings.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def category_page(request):
    categories = [listing.category for listing in Auction_listing.objects.all() if listing.category ]
    return render(request, "auctions/category.html",{
        "categories" : categories
    })

def filter_category(request, category):
    return render(request, "auctions/index.html",{
        "title": f"Active Listings under '{category}'",
        "listings" : Auction_listing.objects.filter(closed=False, category=category)
    })
