from django.db import models
from django.contrib.auth.models import User
from Base.models import Basemodel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from Base.email import send_account_activation_email
import logging
from Ecommerce import settings
from product.models import Coupon, Product

logger = logging.getLogger(__name__)

# Create your models here.
class Profile(Basemodel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid = False , cart__user = self.user ).count()

class Cart(Basemodel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon , on_delete=models.SET_NULL , null=True , blank=True)
    is_paid = models.BooleanField(default=False)
    
    def get_cart_total(self):
        cart_items = self.items.all()  
        total_price = 0 
        for cart_item in cart_items:
            item_total = cart_item.product.price 
            if hasattr(cart_item, 'color_variant') and cart_item.color_variant:
                item_total += cart_item.color_variant.price

            # Add size variant price if it exists
            if hasattr(cart_item, 'size_variant') and cart_item.size_variant:
                item_total += cart_item.size_variant.price

            # Add the item total to the overall total price
            total_price += item_total * cart_item.quantity  # Multiply by quantity
            
        if self.coupon:
            return total_price - self.coupon.discount

        return total_price  # Return the total price of the cart

    
    def __str__(self):
        return f"Cart of {self.user.username}"

 
 
class CartItem(Basemodel):  
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in cart of {self.cart.user.username}"


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            email = instance.email
            send_account_activation_email(email, email_token)
    except Exception as e:
        logger.error(f"Error in sending account activation email: {e}")
