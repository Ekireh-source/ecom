from django.urls import path
from django.contrib import admin
from .views import( 
home_view,
ProductDetail,
OrderSummaryView,
add_to_cart, 
remove_from_cart, 
remove_single_item_from_cart,
search
)
app_name = "core"

urlpatterns = [
    # path('cat/', Category.as_view(), name="cat"),
   
    path('', home_view, name="home"),
    path('search/', search, name="search"),
    path('product/<slug>/', ProductDetail.as_view(), name="product"),
    path('order_summary/', OrderSummaryView.as_view(), name="order_summary"),
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<slug>/', remove_from_cart, name="remove_from_cart"),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name="remove_single_item_from_cart"),
    
    
]
