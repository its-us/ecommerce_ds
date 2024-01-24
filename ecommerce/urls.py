from ecommerce.views import index, category_list_view, product_list_view, vendor_list_view , vendor_detail_view
from django.urls import path
from django.urls import include 


app_name = "ecommerce"

urlpatterns = [
    #Homepage
    path("" , index, name = "index"),
    path('user/', include('userauths.urls')),
    path('categories/', category_list_view, name='category-list'),
    path('products/', product_list_view, name='product-list'),
    path('vendors/', vendor_list_view, name='vendor-list'),
     path('vendor/<vid>/', vendor_detail_view, name='vendor-detail'),



]
