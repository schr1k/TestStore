from django.contrib import admin

from .models import *


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class SubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category_id',)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subcategory_id',)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id',)


class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'user_id', 'name', 'description', 'amount',)


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(SubCategories, SubCategoriesAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(Basket, BasketAdmin)
admin.site.register(Users, UsersAdmin)
