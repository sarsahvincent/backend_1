from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Product, Review, Order, OrderItem, ShippingAddress


# admin.site.register(CustomUser, UserAdmin)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
