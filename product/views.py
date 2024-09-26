from django.shortcuts import redirect, render
from .models import *
from accounts.models import Cart
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


# def get_product(request , slug):
#     try:
#         product = Product.objects.get(slug = slug)
#         return render(request , 'product/product.html' ,  context={'product' : product})

#     except Exception as e:
#         print(e)
        


# def get_product(request, slug):
#     try:
#         product = Product.objects.get(slug=slug)
#         return render(request, 'product/product.html', context={'product': product})

#     except Product.DoesNotExist:
#         # Return a 404 response if the product is not found
#         return HttpResponse("Product not found", status=404)

#     except Exception as e:
#         # Log the error and return a generic error message
#         print(e)
#         return HttpResponse("An error occurred", status=500)
   

def get_product(request, slug):
    try:
        product = Product.objects.get(slug=slug)
       
        return render(request, 'product/product.html', context={'product': product  })

    except Product.DoesNotExist:
        # Return a 404 response if the product is not found
        return HttpResponse("Product not found", status=404)

    except Exception as e:
        # Temporarily show the exception details for debugging
        return HttpResponse(f"An error occurred: {e}", status=500)

    