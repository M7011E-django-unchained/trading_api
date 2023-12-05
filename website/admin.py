from django.contrib import admin
from .models import Member, Shipment, Auction, Category, Subcategory

admin.site.register(Member)
admin.site.register(Shipment)
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Subcategory)
