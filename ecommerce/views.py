from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from taggit.models import Tag
from ecommerce.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address



def index(request):
    #products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status = "published", featured = True)
    context = {
        "products": products

    }


    return render(request, 'ecommerce/index.html', context)
    


def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    context = {
        "products": products

    }

    return render(request, 'ecommerce/product-list.html', context)
    

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories

    }

    return render(request, 'ecommerce/category-list.html', context)
    


def category_product_list_view(request, cid):
    category = Category.objects.get(cid = cid)
    products = Product.objects.filter(product_status = "published", category = category)

    context = {
        "category":category,
        "products": products,
    }
    return render(request, "ecommerce/category_product_list.html", context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid = pid)
    #product = get_object_or_404(Product, pid = pid)

    products = Product.objects.filter(category = product.category).exclude(pid = pid)[:8]


    p_image = product.p_images.all()

    context = {
        "product":product,
        "p_image":p_image,
        "products":products,
    }

    return render(request, "ecommerce/product-detail.html", context)



def tag_list(request, tag_slug = None):
    products = Product.objects.filter(product_status = "published").order_by("-id")

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug = tag_slug)
        products = products.filter(tags__in=[tag])


    context = {
        "products":products,
        "tag":tag
    }

    return render(request, "ecommerce/tag.html", context)