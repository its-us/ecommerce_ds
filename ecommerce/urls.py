from ecommerce.views import index,checkout_view, payment_failed_view, payment_completed_view, cart_view, update_cart, search_view, category_list_view, product_list_view, vendor_list_view , vendor_detail_view, category_product_list_view, product_detail_view, tag_list , filter_product, ajax_add_review, add_to_cart, delete_item_from_cart
from django.urls import path
from django.urls import include 
from django.conf import settings
from django.conf.urls.static import static


app_name = "ecommerce"

urlpatterns = [
    #Homepage
    path("" , index, name = "index"),
    path('user/', include('userauths.urls')),
    path('categories/', category_list_view, name='category-list'),
    path('products/', product_list_view, name='product-list'),
    path('products/<pid>/', product_detail_view, name='product-detail'),    
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),
    path('category_product_list/<cid>/', category_product_list_view, name='category_product_list'),
    path('tags/<slug:tag_slug>/', tag_list, name='tags'),
    
    #Add Review 
    path('ajax-add-review/<pid>/', ajax_add_review, name="ajax-add-review"),

    path("search/", search_view, name = "search"),
    path('filter-products/', filter_product , name="filter-products"),
    
    
    
    path("add-to-cart/", add_to_cart, name = "add-to-cart"),

    #cart page
    path("cart/", cart_view, name = "cart"),

    #delete item from cart
    path("delete-from-cart/", delete_item_from_cart, name = "delete-from-cart"),
    #Update cart
    path("update-cart/", update_cart, name = "update-cart"),
    
    #checkout url
    path("checkout/", checkout_view, name = "checkout"),

    #Paypal
    path("paypal/", include('paypal.standard.ipn.urls')),
    
    #Payment Successful
    path("payment-completed/", payment_completed_view, name = "payment-completed"),
    #Payment Failed
    path("payment-failed/", payment_failed_view, name = "payment-failed"),
]



