from django.shortcuts import render
from django.http import HttpResponse

from ecommerce.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address



def index(request):
    products = Product.objects.all()
    context = {
        "products": products

    }


    return render(request, 'ecommerce/index.html', context)
    
