from django.contrib import admin
from ecommerce.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address



# Register your models here.


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'price', 'category', 'featured', 'product_status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']
    
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user','price', 'paid_status', 'order_date', 'product_status']


class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no', 'item', 'image', 'qty', 'price', 'total']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'review', 'rating']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address', 'status']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
