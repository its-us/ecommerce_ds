from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.db.models import Count, Avg
from django.http import  JsonResponse
from taggit.models import Tag
from ecommerce.models import Product, Category, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from ecommerce.forms import ProductReviewForm
from  django.template.loader import render_to_string
from django.contrib import messages
from django.urls  import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required



def index(request):
    #products = Product.objects.all().order_by("-id")
    products = Product.objects.filter(product_status = "published", featured = True)
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
  
    


def product_list_view(request):
    products = Product.objects.filter(product_status = "published")
    vendors = [product.vendor for product in products]

    # Now 'vendors' is a list containing the 'vendor' attribute for each product
    
    context = {
        "products": products,
        'vendors': vendors

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
    vendor = product.vendor

    products = Product.objects.filter(category = product.category).exclude(pid = pid)[:8]

    reviews = ProductReview.objects.filter(product = product)

    average_rating = ProductReview.objects.filter(product = product).aggregate(rating = Avg('rating'))
    
    # Product Review form
    review_form = ProductReviewForm()
    make_review = True 

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user = request.user, product = product).count()

        if user_review_count > 0:
            make_review = True

    p_image = product.p_images.all()

    context = {
        "product":product,
        "review_form":review_form,
        "p_image":p_image,
        "reviews":reviews,
        "average_rating":average_rating,
        "products":products,
        "vendor":vendor,
        "make_review":make_review,
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





def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user = user,
        product =product,
        review = request.POST['review'],
        rating= request.POST['rating'],
    )
    
    context = {
        'user': user.username,
        'review' : request.POST['review'],
        'rating' : request.POST['rating'],
        
        
    }
    
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))
    
    return JsonResponse(
        {
        'bool' : True,
        'context' :  context,
        'average_reviews' : average_reviews,
        }
    )



def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains = query).order_by("-date")

    context = {
        "products":products,
        "query":query,
    }

    return render(request, "ecommerce/search.html", context)



def filter_product(request):
    categories = request.GET.getlist('category[]') 
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']


    products = Product.objects.filter(product_status = "published").order_by("-id").distinct()
    
    products =products.filter(price__gte=min_price)
    products =products.filter(price__lte=max_price)
    
    if len(categories) > 0: 
        
        products = products.filter(category__id__in=categories).distinct()
        
    if len(vendors) > 0: 
        products = products.filter(vendor__id__in=vendors).distinct()
    
       
        
    data = render_to_string("ecommerce/async/product-list.html",{"products":products})
    
    return JsonResponse({"data":data})
    


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image':request.GET['image'],
        'pid':request.GET['pid'],

    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
             cart_data = request.session['cart_data_obj']
             cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
             cart_data.update(cart_data)
             request.session['cart_data_obj'] = cart_data

        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})
    
    

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "ecommerce/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("ecommerce:index")
    

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("ecommerce/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})



def update_cart(request):
    cart_total_amount = 0 
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty 
            request.session['cart_data_obj'] = cart_data

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("ecommerce/async/cart-list.html",{"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context, 'totalcartitems': len(request.session['cart_data_obj'])})
        

@login_required
def checkout_view(request):
    cart_total_amount = 0
    total_amount = 0
    # Checking if cart_data_obj session exists
    if 'cart_data_obj' in request.session:
        #Getting total amount for Paypal Amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
        # create order object  
        order = CartOrder.objects.create(
            user = request.user,
            price = total_amount
        )
        
        #Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderItems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-" + str(order.id), #INVOICE_NO-4,
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item[ 'qty']) * float(item[ 'price'])

            )  
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': "Order-Item-No-" + str(order.id),
        'invoice':"INV_NO-" + str(order.id),
        'currency_code':"USD",
        'notify_url':'http://{}{}'.format(host, reverse("paypal-ipn")),
        'return_url':'http://{}{}'.format(host, reverse("ecommerce:payment-completed")),
        'cancel_url':'http://{}{}'.format(host, reverse("ecommerce:payment-failed")),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    #cart_total_amount = 0
    #if 'cart_data_obj' in request.session:
    #    for p_id, item in request.session['cart_data_obj'].items():
    #       cart_total_amount += int(item['qty']) * float(item['price'])
    
    return render(request, "ecommerce/checkout.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button})


@login_required
def payment_completed_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
           cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'ecommerce/payment-completed.html', {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount})

@login_required
def payment_failed_view(request):
    return render(request,'ecommerce/payment-failed.html')
    




