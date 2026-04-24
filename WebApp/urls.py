from django.urls import path
from WebApp import views

urlpatterns=[
    path('home_page/',views.home_page,name="home_page"),
    path('about_page/', views.about_page, name="about_page"),
    path('product_page/', views.product_page, name="product_page"),
    path('contact_page/',views.contact_page,name="contact_page"),
    path('filtered_page/<cat_name>',views.filtered_page,name="filtered_page"),
    path('single_items/<int:item_id>/', views.single_items, name="single_items"),
    path('save_contact/', views.save_contact, name="save_contact"),
    path('', views.sign_in, name="sign_in"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('save_sign_up/',views.save_sign_up,name="save_sign_up"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('save_cart/',views.save_cart,name="save_cart"),
    path('cart_page/',views.cart_page,name="cart_page"),
    path('checkout_page/',views.checkout_page,name="checkout_page"),
    path('save_checkout/',views.save_checkout,name="save_checkout"),
    path('payment_page/', views.payment_page, name="payment_page"),
    path('delete_cart/<int:cart_id>/',views.delete_cart,name="delete_cart"),
    path('api/recommendations/<int:item_id>/', views.product_recommendations_api, name="product_recommendations_api"),
]
