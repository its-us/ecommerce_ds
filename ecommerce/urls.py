from ecommerce.views import index
from django.urls import path
from django.urls import include


app_name = "ecommerce"

urlpatterns = [
    #Homepage
    path("" , index, name = "index"),
    path('user/', include('userauths.urls')),
  
]
