from ecommerce.views import index
from django.urls import path

app_name = "ecommerce"

urlpatterns = [
    path("" , index)
]