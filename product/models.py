from django.db import models
from Base.models import Basemodel
from django.utils.text import slugify



class Category(Basemodel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories')
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it doesn't exist
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name
    
class ColorVarient(Basemodel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField()
    
class SizeVarient(Basemodel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField()

class Product(Basemodel):
    name = models.CharField(max_length=100)  # Change 'product_name' to 'name'
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    description = models.TextField()  # Also, renaming 'product_description' to 'description' for simplicity
    color_varient = models.ManyToManyField(ColorVarient)
    size_varient = models.ManyToManyField(SizeVarient)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name



class ProductImage(Basemodel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product')

   
class Coupon(Basemodel):
    coupon_code = models.CharField(max_length=50)
    is_expire = models.BooleanField(default=False)
    discount = models.IntegerField(default=500)
    min_amount = models.IntegerField(default=1000)
