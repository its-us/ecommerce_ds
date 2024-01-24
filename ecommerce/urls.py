from ecommerce.views import index ,  vendor_list_view , vendor_detail_view
from django.urls import path
from django.urls import include


app_name = "ecommerce"

urlpatterns = [
    path("" , index, name = "index"),
    path('user/', include('userauths.urls')),
  
  
  
  #vendor
    path('vendors/', vendor_list_view, name="vendor-list"),
    path('vendor/<vid>/', vendor_detail_view, name="vendor-detail"),
    path('vendor/<int:vid>/', vendor_detail_view, name='vendor_detail')

]
