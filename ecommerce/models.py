from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = models.UUIDField(unique = True, length = 10, max_Length = 20, Prefix = "cat", alphabet = "abcdefgh12345")
    title = models.CharField(maxL_Length = 100)
    image = models.ImageField(upload_to = "category")

    class Meta:
        verbose_name_plural = "Categories"


    def category_image(self):
        return mark_safe('<img src= "%s" width="50" height="50 />' % (self.image.url))
    
    def __str__(self):
        return self.title
    
class Vendor(models.Model):
    vid = models.UUIDField(unique = True, length = 10, max_Length = 20, Prefix = "ven", alphabet = "abcdefgh12345")
    title = models.CharField(maxL_Length = 100)
    image = models.ImageField(upload_to = user_directory_path)
    description = models.TextField(null = True, blank = True)

    adress = models.CharField(maxL_Length = 100, default = "123 casabarata")
    contact = models.CharField(maxL_Length = 100, default = "+212 65447xx120")
    chat_resp_time = models.CharField(maxL_Length = 100, default = "100")
    shipping_on_time = models.CharField(maxL_Length = 100)
    athentic_rating = models.CharField(maxL_Length = 100)
    days_return = models.CharField(maxL_Length = 100)
    warranty_period = models.CharField(maxL_Length = 100)


    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)

