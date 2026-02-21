from django.urls import path
from .import views

urlpatterns = [


### Index Page & Functionalities ###
    
    #Index Page Path
    path('', views.index, name='index'),
    
    #To Submit Review
    path('submit_review', views.submit_review, name = 'submit_review'),

## -------------------------------------- ##
    




### About and Contact Us Page Path ###
    
    #About Us Page Path
    path('about', views.about, name = 'about'),
    
    #Contact Us Page Path
    path('contact', views.contact, name = 'contact'),

## -------------------------------------- ##





### Products Module ###

    #Products Page Path
    path('products', views.products, name='products'),

    #Details of Product Page Path
    path('product_details/<int:id>', views.product_details, name = 'product_details'),

    #To Add New Product
    path('add_product', views.add_product, name = 'add_product'),

    #To Remove Any Product
    path('remove_product/<int:id>', views.remove_product, name='remove_product'),


## -------------------------------------- ##





### Login Module  ###

    #Login Page Path
    path('login', views.login, name='login'),
    
    #Register Page Path
    path('register', views.register, name='register'),

    #Logout 
    path('logout', views.logoutpage, name = 'logout'),

## -------------------------------------- ##






### Cart Module ###

    #Cart Page Path
    path('view_cart', views.view_cart, name='view_cart'),
    
    #To Add Product to Cart
    path('cart/<int:id>', views.cart, name='cart'),

    #To Remove Product from Cart
    path('remove_cart/<int:id>', views.remove_cart, name='remove_cart'),

    #To Update Cart
    path('update_cart/', views.update_cart, name='update_cart'),

## -------------------------------------- ##





### Order Module ###
    
    #Checkout Page Path
    path('checkout', views.checkout, name="checkout"),

    #To Save Order Details
    path('order_details', views.order_details, name='order_details'),
    
    #Confirmation Page Path
    path('confirmation/<int:id>/', views.confirmation, name = 'confirmation'),

## -------------------------------------- ##





]