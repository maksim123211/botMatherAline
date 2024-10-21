from django.contrib import admin
from app.models import Account, Product, Category, AboutCompany, Order, OrderItem


admin.site.register(Account)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(AboutCompany)
admin.site.register(Order)
admin.site.register(OrderItem)

