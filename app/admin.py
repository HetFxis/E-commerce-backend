from django.contrib import admin
# from django.contrib.auth.models import User, Group

from .models import CustomUser,Product,Category,Cart,Order,ProductImage
# admin.site.register(User)
# admin.site.register(Group)
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display=['id','username','email','password','mobile_number','is_customer','is_admin']
@admin.register(Product)
class product(admin.ModelAdmin):
    list_display=['name','description','sizes','image','stock','Category','brand','price','review']
@admin.register(ProductImage)
class productimage(admin.ModelAdmin):
    list_display=['image']
@admin.register(Category)
class category(admin.ModelAdmin):
    list_display=['id','name','description']

@admin.register(Cart)
class cart(admin.ModelAdmin):

    list_display=['id', 'user','product', 'product_id','quantity', 'number_of_items', 'total', 'created_at', 'updated_at', ]
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id',"user","full_name","email","address","city","state","zip_code"]
# @admin.register(Cartitem)
# class cartitem(admin.ModelAdmin):
#         list_display=[        'id', 'Cart', 'Product', 'created_at', 'updated_at'
# ]
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'price', 'category')
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display=['user','product','quantity','added_at']
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'get_items', 'total_price', 'status', 'placed_at')  # Use a method for many-to-many

#     def get_items(self, obj):
#         # Return a string representation of the items
#         return ", ".join([str(item) for item in obj.items.all()])
#     get_items.short_description = 'Items'  