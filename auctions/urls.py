from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("create_listing", views.create_listing, name="create_listing"), #to create a new listing
    path("listing/<int:listing_id>", views.show_listing, name='listing'), #to display individual listing
    path("create_bid/<int:listing_id>", views.create_bid, name="create_bid"),  #to create bid for listing
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"), #close the listing
    path("comment/<int:listing_id>", views.comment, name="comment"), #to leave a comment on a listing

    path("watchlist", views.watchlist, name="watchlist"), #watchlist page of the listings the user likes
    path("watchlist_edit/<int:listing_id>", views.watchlist_edit, name="edit watchlist"), #edit the watchlist

    path("categories", views.category_page, name="listing categories"), #categories of all listing
    path("categories/<str:category>", views.filter_category, name="filter category")
]
