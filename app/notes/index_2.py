from django.db.models import query
from django.db.models.fields import related
from django.http import HttpResponse, HttpResponseRedirect, request, response
from django.shortcuts import redirect, render, resolve_url
from django.urls.conf import path
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import  *
from TopDeals.models import *
import random
from .forms import RegistrationForm,LoginForm,AddressForm,CheckoutForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Instamojo imports
from instamojo_wrapper import Instamojo
API = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')


class IndexView(View):
    def get(self,request):
        context = {
            'sliders':Slider.objects.all(),
            'categories':Categories.objects.all(),
            'dealofday':DealOfDay.objects.all(),
            'trendingproduct':TrendingProduct.objects.all(),
            'menstopwear':MensTopWear.objects.all(),
            'womenstopwear':WomensTopWear.objects.all()
        }
        return render(self.request,template_name='index.html',context=context)


class RegistrationUser(View):
    def get(self,request):
        action = self.request.GET.get('action')
        if action is not None:
            # Creating OTP.
            user_otp = random.randint(100000,999999)
            
            user = self.request.session.get('user')
            user['user_otp'] = user_otp
            self.request.session['user'] = user
            
            # Sending OTP to Customer/User.
            msg = "Hello , {}  \n  Your OTP is {}  \n  Thanks".format(user['first_name'],user_otp)
            send_mail(
                'Welcome to Mystore',
                msg,
                settings.EMAIL_HOST_USER,
                [user.get('username')], # OR user['username']
                fail_silently=True,
            )
            messages.info(self.request,'OTP has send to your email account !')
            return render(self.request,template_name='registration/signup.html',context={'otp':True})
        else:
            context = {
                'form':RegistrationForm()
            }
            return render(self.request,template_name='registration/signup.html',context=context)    

    def post(self,request):
        # Checking for OTP 
        get_otp = self.request.POST.get('otp')
        data = self.request.session.get('user')
        if get_otp:
            if int(get_otp) == int(self.request.session.get('user')['user_otp']):
                data = self.request.session.get('user')
                x = User.objects.create(
                    first_name=data['first_name'],
                    last_name = data['last_name'],
                    username = data['username'],
                    email = data['username'],
                    password = data['password']
                )
                x.save()
                # self.request.session.pop('user')
                messages.success(self.request,'Account has been created successfully !')
                return render(self.request,template_name='registration/signup.html',context={'form':RegistrationForm()})
            else:
                messages.error(self.request,'You entered wrong OTP Please Resend OTP !')
                return render(self.request,template_name='registration/signup.html',context={'otp':True})
                
        
        # Registraiton Form

        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Creating OTP.
            user_otp = random.randint(100000,999999)

            self.request.session['user'] = {
                'first_name':user.first_name,
                'last_name':user.last_name,
                'username':user.username,
                'password':user.password,
                'user_otp':user_otp
            }

            # Sending OTP to Customer/User.

            msg = "Hello , {}  \n  Your OTP is {}  \n  Thanks".format(user.first_name,user_otp)
            is_mail_send = send_mail(
                'Welcome to Mystore',
                msg,
                settings.EMAIL_HOST_USER,
                [user.username], # OR user                                                                                                                                         # user here is email of user stored in user variable.i.e,user.first_name,user.last_name,user.username='xyz@gmail.com
                fail_silently=True,
            )
            if is_mail_send == 1:
                messages.info(self.request,'OTP has send to your email account !')
                return render(self.request,template_name='registration/signup.html',context={'otp':True})
            else:
                return HttpResponse('<h1>Something Went Wrong ! Check Your Connection.</h1>')
        else:
            context = {
                'form':RegistrationForm(data=self.request.POST)
            }
            return render(self.request,template_name='registration/signup.html',context=context)  



class MyLoginView(LoginView):
    authentication_form = LoginForm

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        profile = self.request.GET.get('profile')
        address = self.request.GET.get('address')
        delete_address = self.request.GET.get('delete-address')
        if profile:
            context = {
                'profile':User.objects.get(id=request.user.id),
                'profile_active':True
            }
            return render(self.request,'profile.html',context=context)
        elif address:
            context = {
                'address':Address.objects.filter(user=request.user),
                'address_active':True
            }
            return render(self.request,'profile.html',context=context)
        elif delete_address:
            Address.objects.get(id=delete_address).delete()
            return HttpResponseRedirect('/accounts/profile/?address=user')
        else:
            context = {
                'form':AddressForm(),
                'dashboard_active':True
            }
            return render(self.request,'profile.html',context=context)

    def post(self,request):
        form = AddressForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.save()
            messages.success(self.request,'Address added successfully ! check in address section.')
            return render(self.request,'profile.html',{'form':AddressForm()})
        else:
            context = {
            'form':AddressForm(request.POST)
            }
            return render(self.request,'profile.html',context=context)



class ProductListView(View):
    def get(self,request,*args,**kwargs):
        pk = kwargs['pk']
        
        # Category Filter
        sub_cat = SubCategoriesVariant.objects.get(id=pk).subcategory
        category_filter = SubCategories.objects.get(id=sub_cat.id)

        # Color Filter
        related_color_products = Product.objects.filter(subcategoryvariant=pk)
        result_color = []
        for related_color_product in related_color_products:
            if (related_color_product.color is not None) and (related_color_product.color.id not in result_color):
                result_color.append(related_color_product.color.id)
        color_filter = Color.objects.filter(id__in=result_color)

        # Size Filter
        related_size_products = Product.objects.filter(subcategoryvariant=pk)
        result_size = []
        for related_size_product in related_size_products:
            if (related_size_product.size is not None) and (related_size_product.size.id not in result_size):
                result_size.append(related_size_product.size.id)
        size_filter = Size.objects.filter(id__in=result_size)

        
        # Product according to subcategoryvariant
        product = Product.objects.filter(subcategoryvariant=pk)

        # Product according to category_filter
        category = request.GET.get('category')
        if category:
            product = product.filter(subcategoryvariant=category)
        
        # Product according to color_filter
        color = request.GET.get('color') 
        if color:
            product = product.filter(color=color)

        # Product according to size_filter
        size = request.GET.get('size') 
        if size:
            product = product.filter(size=size)

        context = {
            'categories':Categories.objects.all(),
            'products' : product,
            'category_filter':category_filter.subcategoriesvariant_set.all(),
            'color_filter':color_filter,
            'size_filter':size_filter,
            'active_category_filter':category,
            'active_color_filter':color,
            'active_size_filter':size
        }
        
        return render(self.request,template_name='product_list.html',context=context)


def SearchView(request):
    query = request.GET.get('search')
    if query is not None:
        request.session['query']=query
    # Category Filter
    related_category_products = Product.objects.filter(title__icontains=request.session.get('query'))
    result_category = []
    for related_category_product in related_category_products:
        if (related_category_product.subcategoryvariant.id not in result_category):
            result_category.append(related_category_product.subcategoryvariant.id)
    category_filter = SubCategoriesVariant.objects.filter(subcategory__id__in=result_category)

    # Color Filter
    related_color_products = Product.objects.filter(title__icontains=request.session.get('query'))
    result_color = []
    for related_color_product in related_color_products:
        if (related_color_product.color is not None) and (related_color_product.color.id not in result_color):
            result_color.append(related_color_product.color.id)
    color_filter = Color.objects.filter(id__in=result_color)

    # Size Filter
    related_size_products = Product.objects.filter(title__icontains=request.session.get('query'))
    result_size = []
    for related_size_product in related_size_products:
        if (related_size_product.size is not None) and (related_size_product.size.id not in result_size):
            result_size.append(related_size_product.size.id)
    size_filter = Size.objects.filter(id__in=result_size)

    product = Product.objects.filter(title__icontains=request.session.get('query'))


    # Product according to category_filter
    category = request.GET.get('category')
    if category:
        product = product.filter(subcategoryvariant=category)
        
    # Product according to color_filter
    color = request.GET.get('color') 
    if color:
        product = product.filter(color=color)

    # Product according to size_filter
    size = request.GET.get('size') 
    if size:
        product = product.filter(size=size)

    context = {
        'categories':Categories.objects.all(),
        'products':product,
        'query':query,
        'category_filter':category_filter,
        'color_filter':color_filter,
        'size_filter':size_filter,
        'active_category_filter':category,
        'active_color_filter':color,
        'active_size_filter':size
    }
    return render(request,'search.html',context=context)


def MainCategory(request,pk):
    product = Product.objects.filter(subcategoryvariant__subcategory__category__id=pk)
    return render(request,'category.html',{'products':product})



def ProductDetailView(request,id,slug):
    product = Product.objects.get(pk=id)
    context = {}
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = ProductVariant.objects.get(id=variant_id) #selected product by click color radio
            colors = ProductVariant.objects.filter(product_id=product.id,size_id=variant.size_id)
            sizes = ProductVariant.objects.raw('SELECT * FROM  Eshop_productvariant  WHERE product_id={} GROUP BY size_id'.format(product.id))
        else:
            variants = ProductVariant.objects.filter(product_id=product.id)
            colors = ProductVariant.objects.raw('SELECT * FROM  Eshop_productvariant  WHERE product_id={} GROUP BY color_id'.format(product.id))
            sizes = ProductVariant.objects.raw('SELECT * FROM  Eshop_productvariant  WHERE product_id={} GROUP BY size_id'.format(product.id))
            variant = ProductVariant.objects.get(id=variants[0].id)
        context = {
            'product': product,
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'relatedproduct':Product.objects.filter(subcategoryvariant=product.subcategoryvariant)
        }
        
        return render(request,'product_detail.html',context=context)
    else:
        context = {
            'product':product,
            'relatedproduct':Product.objects.filter(subcategoryvariant=product.subcategoryvariant)
        }
        return render(request,'product_detail.html',context=context)



def AjaxColor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = ProductVariant.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)


@login_required(login_url='/accounts/login/')
def AddToCart(request):
    if request.method == 'POST':
        path = request.POST.get('path')
        product_variant_id = request.POST.get('variant_id')
        product_id = request.POST.get('product_id')
        user = request.user
        if product_variant_id != None:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
            cart = Cart.objects.create(product=Product(product_variant.product.id),product_variant=ProductVariant(product_variant.id),user=User(user.id))
            cart.save()
        else:
            product = Product.objects.get(id=product_id)
            cart = Cart.objects.create(product=Product(product.id),user=User(user.id))
            cart.save()
        return HttpResponseRedirect(path)

    path = request.GET['path']
    return HttpResponseRedirect(path)
        
    
@login_required(login_url='/accounts/login/')     
def ShoppingCart(request):
    context = {
        'cart':Cart.objects.filter(user=User(request.user.id))
    }
    return render(request,'cart.html',context=context)


def IncreaseQuantity(request):
    print("dsfhsdkfl")
    product_variant = request.GET.get('product_variant')
    product = request.GET.get('product')

    if product_variant != None:
        cart = Cart.objects.get(id=product_variant)
        product_variant = ProductVariant.objects.get(id=cart.product_variant.id)
        if cart.quantity == product_variant.quantity:
            messages.info(request,'Only {} product available in stock.'.format(cart.quantity))
        else:
            cart.quantity += 1
            cart.save()
    else:
        cart = Cart.objects.get(id=product)
        product = Product.objects.get(id=cart.product.id)
        if cart.quantity == product.quantity:
            messages.info(request,'Only {} product available in stock.'.format(cart.quantity))
        else:
            cart.quantity += 1
            cart.save()

    return HttpResponseRedirect('/cart/')

def DecreaseQuantity(request):
    product_variant = request.GET.get('product_variant')
    product = request.GET.get('product')
    if product_variant != None:
        cart = Cart.objects.get(id=product_variant)
        if cart.quantity == 1:
            cart.delete()
        else:
            cart.quantity -= 1
            cart.save()
    else:
        cart = Cart.objects.get(id=product)
        if cart.quantity == 1:
            cart.delete()
        else:
            cart.quantity -= 1
            cart.save()

    return HttpResponseRedirect('/cart/')



def Checkout(request):
    context = {
        'form':CheckoutForm(),
        'address':Address.objects.filter(user=request.user),
        'cart':Cart.objects.filter(user=User(request.user.id))
        }
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            address = request.POST['address']
            total = Cart().cart_total(request.user)

            if payment_method == 'ONLINE':
                try:
                    # Creating Order
                    order = Order.objects.create(
                        order_status = 'PENDING',
                        address = Address(address),
                        payment_method = payment_method,
                        total = total
                    )

                    #Creating Order Item
                    for item in Cart.objects.filter(user=request.user):
                        if item.product_variant != None:
                            order_item = OrderItem.objects.create(
                                order = Order(order.id),
                                product = Product(item.product.id),
                                product_variant = ProductVariant(item.product_variant.id),
                                quantity = item.quantity,
                                price = (item.product_variant.price - (item.product_variant.price * item.product_variant.discount/100)),
                            )
                        else:
                            order_item = OrderItem.objects.create(
                                order = Order(order.id),
                                product = Product(item.product.id),
                                quantity = item.quantity,
                                price = (item.product.price - (item.product.price * item.product.discount/100)),
                            )
                    
                    # Creating Payment
                    response = API.payment_request_create(
                        amount=order.total,
                        purpose='Payment for shopping',
                        buyer_name='{} {}'.format(request.user.first_name,request.user.last_name),
                        send_email=True,
                        email=request.user.email,
                        redirect_url="http://127.0.0.1:8000/validate-payment/{}/".format(order.id)
                    )

                    payment_request_id = response['payment_request']['id']
                    url = response['payment_request']['longurl']

                    payment = Payment.objects.create(
                        order = Order(order.id),
                        payment_request_id = payment_request_id
                    )
                    return redirect(url)
                except:
                    print(order)
                    Order.objects.filter(order_status='PENDING').delete()
                    return render(request,'payment_failed.html')
            else:
                # Creating Order
                order = Order.objects.create(
                    order_status = 'PLACED',
                    address = Address(address),
                    payment_method = payment_method,
                    total = total
                )

                #Creating Order Item
                for item in Cart.objects.filter(user=request.user):
                    if item.product_variant != None:
                        order_item = OrderItem.objects.create(
                            order = Order(order.id),
                            product = Product(item.product.id),
                            product_variant = ProductVariant(item.product_variant.id),
                            quantity = item.quantity,
                            price = (item.product_variant.price - (item.product_variant.price * item.product_variant.discount/100)),
                        )
                    else:
                        order_item = OrderItem.objects.create(
                            order = Order(order.id),
                            product = Product(item.product.id),
                            quantity = item.quantity,
                            price = (item.product.price - (item.product.price * item.product.discount/100)),
                        )
                Cart.objects.filter(user=request.user).delete()
                messages.success(request,'Order Placed Successfully !')
                return redirect('myorders')
    return render(request,'checkout.html',context=context)

def ValidatePayment(request,pk):
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    response = API.payment_request_payment_status(payment_request_id,payment_id)
    status = response.get('payment_request').get('payment').get('status')

    if status != "Failed":
        try:
            payment = Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = "PLACED"
            order.save()

            Cart.objects.filter(user=request.user).delete()
            return redirect('myorders')
        except:
            return render(request,'payment_failed.html')
    else:
        order = Order.objects.get(id=pk)
        order.delete()
        return render(request,'payment_failed.html')


@login_required(login_url='/accounts/login/')
def Myorders(request):
    context = {
        'myorders':Order.objects.filter(address__user=request.user).order_by('-date').exclude(order_status='PENDING')
    }
    return render(request,'myorders.html',context=context)


'''

# Email Configs
EMAIL_HOST_USER = 'amazonstore295@gmail.com'
EMAIL_HOST_PASSWORD = 'amazonstore295s.t'

# Instamojo Configs
API_KEY = "test_00fdfd80a82bdae553372ec546b"
AUTH_TOKEN = "test_26343b0f40ae03f99bba48b3a58"


const submitForm = () => {
  const colors = document.querySelectorAll('.color-input')
  const categories = document.querySelectorAll('.category-input')
  const sizes = document.querySelectorAll('size-input')

  let categories_filter, colors_filter, sizes_filter = [];

  categories.forEach(element => element.checked ? categories_filter.push(element.value) : null)
  colors.forEach(element => element.checked ? colors_filter.push(element.value) : null)
  sizes.forEach(element => element.checked ? sizes_filter.push(element.value) : null)

  console.log(categories_filter, siz)
  window.location.assign(`${window.location.href}?categories=${categories.filter(element => element.checked)}`)

} 

'''