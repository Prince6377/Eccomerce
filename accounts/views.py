from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import *


def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            messages.warning(request, 'Account not Found')
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your Account is not verified')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username=email, password=password)
        
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        
        messages.warning(request, "Invalid Credentials")
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/login.html')


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user_obj = User.objects.filter(username=email)
        if user_obj.exists():
            messages.warning(request, 'The Email is already taken')
            return HttpResponseRedirect(request.path_info)
        
        # Create user without password here
        user_obj = User.objects.create(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            username=email
        )
        # Use set_password to hash the password
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request, 'An email has been sent on your mail')
        return HttpResponseRedirect(request.path_info)
    
    return render(request, 'accounts/register.html')


def email_verified(request, email_token):
    try:
        user_profile = Profile.objects.get(email_token=email_token)
        user_profile.is_email_verified = True
        user_profile.save()
        return redirect('/')
    except Profile.DoesNotExist:
        return HttpResponse("Invalid Email Token")


def add_to_cart(request, uid):
    product = get_object_or_404(Product, uid=uid) 
    user = request.user
    
    cart, created = Cart.objects.get_or_create(user=user, is_paid=False)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('get_product', slug=product.slug)


def remove_cart(request, Cart_item_id):  # use id instead of uid
    try:
        cart_item = get_object_or_404(CartItem, id=Cart_item_id)  # look up by id instead of uid
        cart_item.delete()
    except Exception as e:
        print(f"Error removing cart item: {e}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def cart(request):
   
    user_cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        try:
            coupon_obj = Coupon.objects.get(coupon_code=coupon)
        except Coupon.DoesNotExist:
            messages.warning(request, 'Coupon code is invalid')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if user_cart.coupon:
            messages.warning(request , 'Already used by someone else.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if user_cart.get_cart_total() < coupon_obj.min_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj.min_amount} to apply the coupon.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        if coupon_obj.is_expire:
            messages.warning(request , 'Coupon is Expired.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        user_cart.coupon_obj = coupon_obj
        user_cart.save()
        messages.success(request , 'Coupon Applied Sucessfully!!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    
    context = {'cart': user_cart}
    return render(request, 'accounts/cart.html', context)