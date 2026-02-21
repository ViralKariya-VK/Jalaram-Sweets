from django.db import models
from django.contrib.auth.models import User

### Model for Products Starts ###

class Products(models.Model):
    #Name of the Product
    name = models.CharField(max_length=255)

    #Price of the Product
    price = models.DecimalField(max_digits=10, decimal_places=2)

    #Picture of the Product
    picture = models.ImageField(upload_to='products/')

    #Short Description of the Product
    short_desc = models.CharField(max_length=500)

    #Detailed Description of the Product
    detailed_desc = models.TextField()


    #Categories for Products

    TRADITIONAL_CLASSICS = 'Traditional Classics'
    BARFIS = 'Barfis'
    CHOCOLATE_SPECIALTIES = 'Chocolate Specialties' 
    KHEER_KADAM = 'Kheer and Kheer Kadam'
    NAMKEEN_SNACKS = 'Namkeen and Snacks'
    CHIKKIS = 'Chikkis'

    CATEGORY_CHOICE = [
        (TRADITIONAL_CLASSICS, 'Traditional Classics'),
        (BARFIS, 'Barfis'),
        (CHOCOLATE_SPECIALTIES, 'Chocolate Specialties'),
        (KHEER_KADAM, 'Kheer Kadam'),
        (NAMKEEN_SNACKS, 'Namkeen and Snacks'),
        (CHIKKIS, 'Chikkis')
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)


    #Boolean Field for Exclusive Product
    is_exclusive = models.BooleanField(default=False)

    #Ingredients
    ingredients = models.TextField(default=None)

    def __str__(self):
        return self.name
    
### Model for Products Ends ###





### Model for Site Users Starts ###

class Site_Users(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)

### Model for Site Users Ends ###





### Model for Cart Starts ###

class Cart(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

### Model for Cart Ends ###






### Model for Review Starts ###

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    rating = models.CharField(max_length=10)

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rating}"
    
### Model for Review Ends ###





### Model for Order Starts ###

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def get_order_items(self):
        return self.items.all()

    def order_items_summary(self):
        """Generate a summary of all related OrderItems."""
        items_summary = [f"{item.quantity} x {item.product.name} (₹{item.total_price})" for item in self.get_order_items()]
        return ", ".join(items_summary)  # Join each item detail into a single string

    order_items_summary.short_description = "Order Items"  # Optional: sets display name in Django Admin

### Model for Order Ends ###





### Model for Order Items Starts ###

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
### Model for Order Items Ends ###





### Model for Contact Starts ###

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    message = models.CharField(max_length=255)

### Model for Order Contact Ends ###