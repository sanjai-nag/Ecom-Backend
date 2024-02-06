from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id","prouser")
admin.site.register(Profile,ProfileAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display=("id",'title','date')

class ProductAdmin(admin.ModelAdmin):
    list_display=("id","title","category","selling_price","date",)
admin.site.register(Product,ProductAdmin)

class Cos_CategoryAdmin(admin.ModelAdmin):
    list_display=("id",'title','date')
admin.site.register(Cos_Category,Cos_CategoryAdmin)

class Cos_ProductAdmin(admin.ModelAdmin):
    list_display=("id","title","category","selling_price","date")
admin.site.register(Cos_Product,Cos_ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=("id","customer","total","complit","date")
admin.site.register(Cart,CartAdmin)

# class CartProductAdmin(admin.ModelAdmin):
#     list_display = ("id","cart","price","quantity","subtotal")
admin.site.register(CartProduct)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","cart","date")
admin.site.register(Order,OrderAdmin)

admin.site.register(InstagramPost)
# Profile
# Category
# Product
# Cart
# CartProduct
# Order

admin.site.register(OTPVerifiaction)
admin.site.register(search)


admin.site.register(Post)

admin.site.register(Call)

admin.site.register(Filterpro)
admin.site.register(review)