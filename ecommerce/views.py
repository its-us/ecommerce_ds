from django.shortcuts import render
from django.http import HttpResponse

from ecommerce.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address



def index(request):
    products = Product.objects.all()
    context = {
        "products": products
    }

    return render(request, 'ecommerce/index.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors" : vendors,
    }
    return render(request , "ecommerce/vendor-list.html", context)
    
    
 
def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    
    context = {
        "vendor": vendor,
        "products": products,  
    }

    return render(request, "ecommerce/vendor-detail.html", context)
  
    
