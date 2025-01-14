from django.urls import path
from . import views

urlpatterns = [
    # --------shop-------------------
    path('',views.cosmetic_login),
    path('logout',views.cosmetic_logout),
    path('shop_home',views.shop_home),
    path('add_pro',views.add_pro),
    path('details',views.details),
    path('category',views.category),
    path('view_category',views.view_category),
    path('delete_category/<id>',views.delete_category),
    path('view_products/<id>',views.view_products),
    path('edit_pro/<id>',views.edit_pro),
    path('delete_pro/<pid>',views.delete_pro),
    path('bookings',views.bookings),
 
    


    

    # -----------user-----------------------
    path('register/',views.register),
    path('otp',views.otp_confirmation),
    path('user_home',views.user_home),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart',views.view_cart),
    # path('remove_item/<id>',views.remove_item),
    path('quantity_inc/<cid>',views.quantity_inc),
    path('quantity_dec/<cid>',views.quantity_dec),
    path('view_details/<id>',views.view_details),
    path('buy_pro/<pid>',views.buy_pro),
    path('user_bookings',views.user_bookings),
    path('cart_buy', views.cart_buy),
    path('view_filtered/<id>',views.view_filtered),
    

]