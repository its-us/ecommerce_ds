from ecommerce.views import index, product_list_view, category_list_view, category_product_list_view, product_detail_view, tag_list
from django.urls import path
from django.urls import include

app_name = "ecommerce"

urlpatterns = [
    #Homepage
    path("" , index, name = "index"),
    path('user/', include('userauths.urls')),
    path("products/", product_list_view, name = "product-list"),
    path("products/<pid>/", product_detail_view, name = "product-detail"),


    #category
    path("category/", category_list_view, name = "category-list"),
    path("category/<cid>/", category_product_list_view, name = "category_product_list"),

    #tag
    path("products/tag/<slug:tag_slug>/", tag_list, name = "tags")
]


