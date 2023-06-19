from django import template
from django.contrib.auth.models import User
from app.models import Cart,ProductVariant,Product
from math import floor

register = template.Library()

@register.filter(name='cart')
def cart(user):
    return Cart.objects.filter(user=User(user.id))

@register.filter(name='sale_price')
def sale_price(original_price,discount):
    return floor(original_price - (original_price*discount/100))


@register.filter(name='is_variant_in_cart')
def is_variant_in_cart(product_variant_id,user):
    product_variant = ProductVariant.objects.get(id=product_variant_id)
    try:
        Cart.objects.get(product=Product(product_variant.product.id),product_variant=ProductVariant(product_variant.id),user=User(user.id))
        return True
    except:
        return False
    
@register.filter(name='is_product_in_cart')
def is_product_in_cart(product_id,user):
    product = Product.objects.get(id=product_id)
    try:
        Cart.objects.get(product=Product(product.id),user=User(user.id))
        return True
    except:
        return False


@register.filter(name='total_amount')
def total_amount(price,qty):
    return floor(price*qty)


@register.filter(name='total_payable_amount')
def total_payable_amount(cart):
    sum = 0
    for item in cart:
        if item.product_variant != None:
            sum += (item.product_variant.price - (item.product_variant.price * item.product_variant.discount/100)) * item.quantity
        else:
            sum += (item.product.price - (item.product.price * item.product.discount/100)) * item.quantity
    return floor(sum)


@register.filter(name='filter_active')
def filter_active(val1,val2):
    try:
        if str(val1) in val2:
            return True
        else:
            return False
    except:
        return False