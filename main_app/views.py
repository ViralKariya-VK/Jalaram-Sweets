import json
from urllib import request
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages



### View for Index Page Starts ###

def index(request):
    
    products = Products.objects.filter(is_exclusive = 'True')
    
    reviews = Review.objects.all()
    # Convert ratings to integers and add them to the context
    reviews_data = [
        {
            'user': review.user,
            'review_text': review.review,
            'rating': int(review.rating)  # Ensure the rating is an integer
        }
        for review in reviews
    ]
    
    return render (request, 'index.html', {'products': products, 'reviews': reviews_data})

### Index View Ends ###





### View for Login Page Starts ###

def login(request):
    if request.method == 'POST':
        login_username = request.POST.get('login_username')
        login_password = request.POST.get('login_password')
        
        #Authenticate the User
        user = authenticate(username=login_username, password=login_password)

        if user is not None:
            auth_login(request, user)
            return redirect(index)
            
        else:
            return render(request, 'Site_pages/login.html', {'error_message': "You have entered an invalid username or password!"})
    
    return render(request, 'Site_pages/login.html')

### Views for Login Page Ends ###






### View for SignUp Page Starts ###

def register(request):
    if request.method == 'POST':
        user_name = request.POST['name']
        user_email = request.POST['email']
        user_number = request.POST['number']
        user_password = request.POST['password']

        contact = str(user_number)

        if len(contact) != 10:
            return render(request, 'Site_pages/register.html', {'contact_error': "The phone number must be exactly 10 digits. Try Again."})
        else:
        # USER OBJECT
            user_obj = User.objects.create_user(username = user_name, email = user_email, password = user_password)

        # Object to redirect data into dummy table
            site_user = Site_Users.objects.create(user = user_obj, phone = contact, email = user_email)

            user_obj.save()
            site_user.save()

        return redirect(login)

    return render(request, 'Site_pages/register.html')

### Views for SignUp Page Ends ###





### View for Logout Functionality Starts ###

def logoutpage(request):
    logout(request)

    return redirect('/')

### View for Logout Functionality Ends ###





### View for Submitting Review Functionality Starts ###

def submit_review(request):
    if request.method == "POST":
        # Get the data from the form
        rating = request.POST.get("rating")
        review_text = request.POST.get("review")

        # Create and save the review instance
        review = Review.objects.create(
            user=request.user,
            review=review_text,
            rating=rating
        )
        review.save()

        # Redirect to a confirmation page or the page with reviews
        return redirect('index')  # Redirect to a relevant page or change as needed

    return render(request, 'index.html')

### View for Submitting Review Functionality Ends ###





### View for Product Page Starts ###

def products(request):
    sort_option = request.GET.get('sort', 'asc')
    category = request.GET.get('category', '')

    # Get all unique categories for filtering
    categories = Products.objects.values_list('category', flat=True).distinct()

    # Define the base queryset
    products = Products.objects.all()

    # Filter by category if provided
    if category:
        products = products.filter(category=category)

    # Apply sorting based on the chosen option
    if sort_option == 'asc':
        products = products.order_by('name')
    elif sort_option == 'desc':
        products = products.order_by('-name')
    elif sort_option == 'lowtohigh':
        products = products.order_by('price')
    elif sort_option == 'hightolow':
        products = products.order_by('-price')

    return render(request, 'Site_pages/products.html', {
        'products': products,
        'categories': categories,
    })

### View for Product Page Ends ###





### View for Detailed Product Page Starts ###

def product_details(request, id):

    product = get_object_or_404(Products, id=id)
    products = Products.objects.filter(category=product.category)
    
    ingredients_list = product.ingredients.split(',') if product.ingredients else []
    
    return render(request, 'Site_pages/product_details.html', {
        'product': product,
        'ingredients_list': ingredients_list,
        'products':products
    })

### View for Detailed Product Page Ends ###





### View for Adding Product Functionality Starts ###

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        picture = request.FILES.get('picture')
        short_desc = request.POST.get('short_desc')
        detailed_desc = request.POST.get('detailed_desc')
        category = request.POST.get('category')
        is_exclusive = request.POST.get('is_exclusive') == 'on'
        ingredients = request.POST.get('ingredients')

        # Create and save the new product
        Products.objects.create(
            name=name,
            price=price,
            picture=picture,
            short_desc=short_desc,
            detailed_desc=detailed_desc,
            category=category,
            is_exclusive=is_exclusive,
            ingredients=ingredients
        )

        return redirect('products')

    return render(request, 'Site_pages/add_product.html')

### View for Adding Product Functionality Ends ###





### View for Removing Product Functionality Ends ###

def remove_product(request, id):
    product = get_object_or_404(Products, id=id)

    # Delete the product
    product.delete()

    # Redirect to the products page after deletion
    return redirect(products)
### View for Removing Product Functionality Ends ###





### View for Cart Functionality Starts ###

#To Add Products to Cart 
def cart(request, id):
  
    product = get_object_or_404(Products, id=id)
    referer_url = request.META.get('HTTP_REFERER')

    # Get or create the cart item
    cart_item, created = Cart.objects.get_or_create(cart_user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, "Item added to Cart")
    
    return redirect(referer_url)
   


#View to Render Cart Page
def view_cart(request):
    cart_products = Cart.objects.filter(cart_user=request.user)

    # Calculate total for each product and overall cart total
    for cart_product in cart_products:
        cart_product.total_price = cart_product.product.price * cart_product.quantity
    
    # Calculate the cart total
    cart_total = sum(cart_product.total_price for cart_product in cart_products)

    return render(request, 'Site_pages/cart.html', {
        'cart_products': cart_products,
        'cart_total': cart_total
    })


#To Remove Product from Cart
def remove_cart(requst, id):
    
    cart_item = get_object_or_404(Cart, id = id, cart_user=requst.user)
    cart_item.delete()

    return redirect(view_cart)


#To Update Cart after Chnages
def update_cart(request):
    if request.method == "POST":
        cart_data = json.loads(request.body)  # Parse JSON data
        cart_total = 0
        updated_cart_products = []

        for item in cart_data:
            cart_item = Cart.objects.get(id=item["product_id"], cart_user=request.user)
            cart_item.quantity = item["quantity"]
            cart_item.save()
            
            # Calculate the total for each updated product
            product_total = cart_item.product.price * cart_item.quantity
            cart_total += product_total

            updated_cart_products.append({
                "id": cart_item.id,
                "total_price": product_total
            })

        return JsonResponse({
            "cart_total": cart_total,
            "cart_products": updated_cart_products
        })
    

### View for Cart Functionality Ends ###





### View for Checkout Functionality Starts ###

#To Render Checkout Page
def checkout(request):
    cart_products = Cart.objects.filter(cart_user=request.user)

    # Calculate total for each product and overall cart total
    for cart_product in cart_products:
        cart_product.total_price = cart_product.product.price * cart_product.quantity
    
    # Calculate the cart total
    cart_total = sum(cart_product.total_price for cart_product in cart_products)

    return render(request, 'Site_pages/checkout.html', {
        'cart_products': cart_products,
        'cart_total': cart_total
    })


#To Save Order Details
def order_details(request):
    cart_products = Cart.objects.filter(cart_user=request.user)

    # Calculate the overall cart total
    cart_total = sum(cart_product.product.price * cart_product.quantity for cart_product in cart_products)

    if request.method == 'POST':
        # Get the shipping information from the form
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']

        # Create a single Order entry
        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            email=request.user.email,
            phone=request.user.site_users.phone,
            total=cart_total
        )

        # Create OrderItems for each product in the cart
        for cart_item in cart_products:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                total_price=cart_item.product.price * cart_item.quantity
            )

        # Clear the cart after the order is placed
        cart_products.delete()

        # Redirect to a confirmation page (or login page)
        return redirect(reverse('confirmation', args=[order.id]))

    return render(request, 'index.html', {
        'cart_items': cart_products,
        'cart_total': cart_total
    })


#To Render Confirmation Page
def confirmation(request, id):
    order = get_object_or_404(Order, id=id)

    # Get the OrderItems related to this order
    order_items = order.items.all()

    return render(request, 'Site_pages/confirmation.html', {
        'order': order,
        'order_items': order_items
    })

### View for Checkout Functionality Ends ###





### View for Contact Us Page Starts ###

def contact(request):

    if request.method == 'POST':
        message = request.POST['message']

        msg = Contact.objects.create(
            user=request.user,
            email=request.user.email, 
            message=message
        )
        msg.save()

    return render (request, 'Site_pages/contact.html')

### View for Contact Us Page Ends ###





### View for About Us Page Starts ###

def about(request):

    reviews = Review.objects.all()
    
    # Convert ratings to integers and add them to the context
    reviews_data = [
        {
            'user': review.user,
            'review_text': review.review,
            'rating': int(review.rating)  # Ensure the rating is an integer
        }
        for review in reviews
    ]
    
    return render (request, 'Site_pages/about.html', {'reviews': reviews_data})

### View for About Us Page Ends ###
