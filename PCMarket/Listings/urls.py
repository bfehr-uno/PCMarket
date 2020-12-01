from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.current_listings, name="current_listings"),
    path("Listing/<int:listing_id>", views.single_listing, name="single_listing"),
    path("EasyBuy", views.easy_buy, name="easy_buy"),
    path("Sell", views.sell, name="sell"),
    path("SaleHistory", views.sale_history, name="sale_history"),
    path("Follow", views.follow, name="follow"),
    path("CreateAccount", views.create_account, name="create_account"),
    path("Login", views.login, name="login"),
    path("Account", views.account, name="account"),
    path("Purchase/<int:listing_id>", views.purchase, name="purchase"),
    path("List/<part_type>", views.list_part, name="list_part"),
    path("EasyBuy/<part_type>", views.find_cheapest, name="find_cheapest"),
]