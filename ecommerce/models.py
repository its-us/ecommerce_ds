from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField



STATUS_CHOICE = (
    ("published", "Published"),
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("published", "Published"),
)

RETURN = (
    ("No Return Policy", "No Return Policy"),
    ("7 Days Return Policy", "7 Days Return Policy"),
)

COD = (
    ("Cash on Delivery Available", "Cash on Delivery Available"),
    ("Cash on Delivery is not Available", "Cash on Delivery is not Available")
)

COLOR_CHOICES = (
    ('black', 'Black'),
    ('blue', 'Blue'),
    ('red', 'Red'),
    ('white', 'White'),
    ('purple', 'Purple'),
    ("green","Green"),
    ("orange", "Orange"),
    ("cyan", "Cyan")
)

PACKAGE_CHOICES = (
    ("Rigid Boxes", "Rigid Boxes"),
    ("Paperboard", "Paperboard"),
    ("Chipboard", "Chipboard"),
    ("Corrugated Cardboard", "Corrugated Cardboard"),
    ("Cotton", "Cotton"),
    ("Plastics", "Plastics"),
    ("Foil Sealed Bags", "Foil Sealed Bags"),
    ("Jute (Hessian/Burlap)", "Jute (Hessian/Burlap)"),
    ("Envelopes / Bubble Mailers", "Envelopes / Bubble Mailers"),
)


STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)

RATING = (
    (1, "⭐✰✰✰✰"),
    (2, "⭐⭐✰✰✰"),
    (3, "⭐⭐⭐✰✰"),
    (4, "⭐⭐⭐⭐✰"),
    (5, "⭐⭐⭐⭐⭐"),
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix="cat", alphabet = "abcdefgh12345")
    title = models.CharField(max_length=100, default="")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


class Tags(models.Model):
    pass


class Vendor(models.Model):

    vid = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix="ven", alphabet = "abcdefgh12345")
    title = models.CharField(max_length=100, default="Vendor")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg") 
    description = RichTextUploadingField(null=True, blank=True, default="I am an Amazing Vendor")
    

    address = models.CharField(max_length=100, default="123 casabarata")
    contact = models.CharField(max_length=100, default="+212 65447xx120")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100)
    authentic_rating = models.CharField(max_length=100)
    days_return = models.CharField(max_length=100)
    warranty_period = models.CharField(max_length=100)
    
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    
    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title
    
    def has_facebook(self):
        return bool(self.facebook)

    def has_instagram(self):
        return bool(self.instagram)

    def has_linkedin(self):
        return bool(self.linkedin)


class Product(models.Model):

    pid = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix="pro", alphabet = "abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name ="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="products")    


    title = models.CharField(max_length=100, default="Product")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    small_description = RichTextUploadingField(null=True, blank=True, default="small description")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="0.99")
    old_price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="2.99")
 
 

    specifications = RichTextUploadingField(null=True, blank = True)
    type = models.CharField(max_length=100, default="Organic", null=True, blank = True)
    stock_count = models.CharField(max_length=100, default="12", null=True, blank = True)
    waranty = models.CharField(max_length=100, default="1", null=True, blank = True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank = True)
    p_quantity = models.CharField(max_length=100, default="2 shoes")
    frame = models.CharField(max_length=10, default="Iron")
    weight_wo_wheels = models.CharField(max_length=10, default="20LBS")
    weight_capacity = models.CharField(max_length=10, default="80LBS")
    size = models.CharField(max_length=10, default="All Sizes")


    tags = TaggableManager(blank = True)
    #tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="in_review")
    p_return = models.CharField(choices=RETURN, max_length=50, default="7 Days Return Policy")
    cod = models.CharField(choices=COD, max_length=50, default="Cash on Delivery Available")
    color = models.CharField(choices=COLOR_CHOICES, max_length=50, blank=True, null=True)
    Type_of_packing = models.CharField(choices=PACKAGE_CHOICES, max_length=50, blank=True, null=True, default="Foil Sealed Bags")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length = 10, max_length = 20, prefix="SKU", alphabet = "ABCD1234")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price


class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(Product, related_name = "p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products Images"


class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="0.99")
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    is_delivered = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length = 200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="0.99")
    total = models.DecimalField(max_digits=99999999999999, decimal_places=2, default="0.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def category_image(self):
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50"/>' % (self.image))


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name = "reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        return self.product.title

    def get_rating(self):
        return self.rating


class Wishlist_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Wishlists"

    def __str__(self):
        if self.product:
            return self.product.title
        else:
            return "Product Not Available"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"



class Address(models.Model):
     user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
     mobile = models.CharField(max_length = 300, null = True)
     address = models.CharField(max_length = 100, null = True)
     status = models.BooleanField(default = False)

     class Meta:
         pass
         #verbose_name_plural = "Product Reviews"
     

