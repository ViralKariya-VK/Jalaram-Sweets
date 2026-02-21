from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Products)
admin.site.register(Site_Users)
admin.site.register(Cart)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(OrderItem)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'created_at', 'order_items_summary')  # Include `order_items_summary` here
admin.site.register(Order, OrderAdmin)

