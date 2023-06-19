from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.conf import path
from django.views import View
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import *
from django.contrib.auth import login
from djStore.settings import API_KEY, AUTH_TOKEN, BASE_URL
from .forms import RegistrationForm, LoginForm, AddressForm, CheckoutForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from app.templatetags.customfilters import total_payable_amount
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from instamojo_wrapper import Instamojo
from django.contrib.auth import authenticate


API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN,
                endpoint='https://test.instamojo.com/api/1.1/')


class IndexView(View):
    def get(self, request):
        context = {
            'sliders': Slider.objects.all(),
            'categories': Categories.objects.all(),
            'dealofday': DealOfDay.objects.all()
        }
        return render(self.request, template_name='index.html', context=context)


class RegistrationUser(View):
    def get(self, request):
        context = {
            'form': RegistrationForm()
        }
        return render(self.request, template_name='registration/signup.html', context=context)

    def post(self, request):
        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            context = {
                'form': RegistrationForm(data=self.request.POST)
            }
            return render(self.request, template_name='registration/signup.html', context=context)


class MyLoginView(LoginView):
    authentication_form = LoginForm


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        tab = self.request.GET.get('tab')
        delete_address = self.request.GET.get('delete-address')

        if tab == 'address':
            if delete_address:
                Address.objects.get(id=delete_address).delete()
            context = {
                'address': Address.objects.filter(user=request.user),
                'address_form': AddressForm(),
                'tab': 'address'
            }
            return render(self.request, 'profile.html', context=context)
        else:
            context = {
                'profile': User.objects.get(id=request.user.id),
            }
            return render(self.request, 'profile.html', context=context)

    def post(self, request):
        form = AddressForm(request.POST)
        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.save()
        return HttpResponseRedirect(self.request.GET.get('next') if self.request.GET.get('next') else '/accounts/profile/?tab=address')


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(View):
    def post(self, request):
        try:
            first_name = self.request.POST['first_name']
            last_name = self.request.POST['last_name']
            email = self.request.POST['email']

            user = User.objects.get(id=self.request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email

            user.save()
            messages.success(request, 'Profile Updated Successfully')
            return HttpResponseRedirect('/accounts/profile/')
        except Exception as e:
            messages.success(request, 'User with this email already exist')
            return HttpResponseRedirect('/accounts/profile/')


class ProductListView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']

        # Category Filter
        sub_cat = SubCategoriesVariant.objects.get(id=pk).subcategory
        category_filter = SubCategories.objects.get(id=sub_cat.id)

        # query params
        category = request.GET.getlist('category')
        color = request.GET.getlist('color')
        size = request.GET.getlist('size')

        # Making new color filter lists
        related_color_products = Product.objects.filter(
            subcategoryvariant__in=category)
        result_color = []
        for related_color_product in related_color_products:
            if (related_color_product.color is not None) and (related_color_product.color.id not in result_color):
                result_color.append(related_color_product.color.id)
        color_filter = Color.objects.filter(id__in=result_color)

        # Making new size filter lists
        related_size_products = Product.objects.filter(
            subcategoryvariant__in=category)
        result_size = []
        for related_size_product in related_size_products:
            if (related_size_product.size is not None) and (related_size_product.size.id not in result_size):
                result_size.append(related_size_product.size.id)
        size_filter = Size.objects.filter(id__in=result_size)

        # In case no filters applied
        product = Product.objects.filter(subcategoryvariant=pk)

        # Product according to category_filter
        if category:
            product = Product.objects.filter(subcategoryvariant__in=category)

        # Product according to color_filter
        if color:
            product = product.filter(color__in=color)

        # Product according to size_filter
        if size:
            product = product.filter(size__in=size)

        # print(category_filter)
        context = {
            'categories': Categories.objects.all(),
            'products': product,
            'category_filter': category_filter.subcategoriesvariant_set.all(),
            'color_filter': color_filter,
            'size_filter': size_filter,
            'active_category_filter': category,
            'active_color_filter': color,
            'active_size_filter': size
        }

        return render(self.request, template_name='product_list.html', context=context)


def SearchView(request):
    query = request.GET.get('search')
    if query is not None:
        request.session['query'] = query
    # Category Filter
    related_category_products = Product.objects.filter(
        title__icontains=request.session.get('query'))
    result_category = []
    for related_category_product in related_category_products:
        if (related_category_product.subcategoryvariant.id not in result_category):
            result_category.append(
                related_category_product.subcategoryvariant.id)
    category_filter = SubCategoriesVariant.objects.filter(
        subcategory__id__in=result_category)

    # Color Filter
    related_color_products = Product.objects.filter(
        title__icontains=request.session.get('query'))
    result_color = []
    for related_color_product in related_color_products:
        if (related_color_product.color is not None) and (related_color_product.color.id not in result_color):
            result_color.append(related_color_product.color.id)
    color_filter = Color.objects.filter(id__in=result_color)

    # Size Filter
    related_size_products = Product.objects.filter(
        title__icontains=request.session.get('query'))
    result_size = []
    for related_size_product in related_size_products:
        if (related_size_product.size is not None) and (related_size_product.size.id not in result_size):
            result_size.append(related_size_product.size.id)
    size_filter = Size.objects.filter(id__in=result_size)

    product = Product.objects.filter(
        title__icontains=request.session.get('query'))

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
        'categories': Categories.objects.all(),
        'products': product,
        'query': query,
        'category_filter': category_filter,
        'color_filter': color_filter,
        'size_filter': size_filter,
        'active_category_filter': category,
        'active_color_filter': color,
        'active_size_filter': size
    }
    return render(request, 'search.html', context=context)


def MainCategory(request, pk):
    product = Product.objects.filter(
        subcategoryvariant__subcategory__category__id=pk)
    return render(request, 'category.html', {'products': product})


def ProductDetailView(request, id, slug):
    product = Product.objects.get(pk=id)
    context = {}
    if product.variant != "None":
        # Post request on selecting the color
        if request.method == 'POST':
            variant_id = request.POST.get('variantid')

            # Post request for adding product to cart
            if request.POST.get('add-to-cart'):
                if request.user.is_authenticated:
                    if variant_id != None:
                        product_variant = ProductVariant.objects.get(id=variant_id)
                        cart = Cart.objects.create(product=Product(
                            product_variant.product.id), product_variant=ProductVariant(product_variant.id), user=User(request.user.id))
                        cart.save()
                    else:
                        product = Product.objects.get(id=product.id)
                        cart = Cart.objects.create(
                            product=Product(product.id), user=User(request.user.id))
                        cart.save()
                else:
                    return HttpResponseRedirect(f'/accounts/login?next={request.path}')

            # Processing
            variant = ProductVariant.objects.get(id=variant_id)
            colors = ProductVariant.objects.filter(
                product_id=product.id, size_id=variant.size_id)
            sizes = ProductVariant.objects.raw(
                'SELECT * FROM  app_productvariant  WHERE product_id={} GROUP BY size_id'.format(product.id))
        else:
            variants = ProductVariant.objects.filter(product_id=product.id)
            colors = ProductVariant.objects.raw(
                'SELECT * FROM  app_productvariant  WHERE product_id={} GROUP BY color_id'.format(product.id))
            sizes = ProductVariant.objects.raw(
                'SELECT * FROM  app_productvariant  WHERE product_id={} GROUP BY size_id'.format(product.id))
            variant = ProductVariant.objects.get(id=variants[0].id)

        context = {
            'categories': Categories.objects.all(),
            'product': product,
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
            'relatedproduct': Product.objects.filter(subcategoryvariant=product.subcategoryvariant)
        }

        return render(request, 'product_detail.html', context=context)
    else:
        context = {
            'categories': Categories.objects.all(),
            'product': product,
            'relatedproduct': Product.objects.filter(subcategoryvariant=product.subcategoryvariant)
        }
        return render(request, 'product_detail.html', context=context)


def AjaxColor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = ProductVariant.objects.filter(
            product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string(
            'color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)



@login_required(login_url='/accounts/login/')
def ShoppingCart(request):
    context = {
        'cart': Cart.objects.filter(user=User(request.user.id))
    }
    return render(request, 'cart.html', context=context)


def IncreaseQuantity(request):
    if request.POST.get('action') == 'post':

        product_variant = request.POST.get('variantId')
        product = request.POST.get('productId')

        cart = None
        if product_variant != None:
            cart = Cart.objects.get(id=product_variant)
            product_variant = ProductVariant.objects.get(
                id=cart.product_variant.id)
            if cart.quantity == product_variant.quantity:
                return JsonResponse({
                    "success": False,
                    "message": 'Only {} product available in stock.'.format(cart.quantity)
                })
            else:
                cart.quantity += 1
                cart.save()
        else:
            cart = Cart.objects.get(id=product)
            product = Product.objects.get(id=cart.product.id)
            if cart.quantity == product.quantity:
                return JsonResponse({
                    "success": False,
                    "message": 'Only {} product available in stock.'.format(cart.quantity)
                })
            else:
                cart.quantity += 1
                cart.save()
        return JsonResponse({
            "success": True,
            "quantity": cart.quantity if cart else 0,
            "total": total_payable_amount(Cart.objects.filter(user=request.user)) if cart else 0
        })

    return JsonResponse({
        "success": False,
        "message": 'Method Not Allowed'
    })


def DecreaseQuantity(request):
    if request.POST.get('action') == 'post':

        product_variant = request.POST.get('variantId')
        product = request.POST.get('productId')

        if product_variant != None:
            cart = Cart.objects.get(id=product_variant)
            if cart.quantity == 1:
                cart.delete()
                cart = None
            else:
                cart.quantity -= 1
                cart.save()
        else:
            cart = Cart.objects.get(id=product)
            if cart.quantity == 1:
                cart.delete()
                cart = None
            else:
                cart.quantity -= 1
                cart.save()
        return JsonResponse({
            "success": True,
            "quantity": cart.quantity if cart else 0,
            "total": total_payable_amount(Cart.objects.filter(user=request.user)) if cart else 0
        })

    return JsonResponse({
        "success": False,
        "message": 'Method Not Allowed'
    })


def Checkout(request):
    context = {
        'form': CheckoutForm(),
        'address': Address.objects.filter(user=request.user),
        'cart': Cart.objects.filter(user=User(request.user.id))
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
                        order_status='PENDING',
                        address=Address(address),
                        payment_method=payment_method,
                        total=total
                    )

                    # Creating Order Item
                    for item in Cart.objects.filter(user=request.user):
                        if item.product_variant != None:
                            order_item = OrderItem.objects.create(
                                order=Order(order.id),
                                product=Product(item.product.id),
                                product_variant=ProductVariant(
                                    item.product_variant.id),
                                quantity=item.quantity,
                                price=(item.product_variant.price - (
                                    item.product_variant.price * item.product_variant.discount/100)),
                            )
                        else:
                            order_item = OrderItem.objects.create(
                                order=Order(order.id),
                                product=Product(item.product.id),
                                quantity=item.quantity,
                                price=(
                                    item.product.price - (item.product.price * item.product.discount/100)),
                            )

                    # Creating Payment
                    response = API.payment_request_create(
                        amount=order.total,
                        purpose='Payment for shopping',
                        buyer_name='{} {}'.format(
                            request.user.first_name, request.user.last_name),
                        send_email=True,
                        email=request.user.email,
                        redirect_url= BASE_URL + "/validate-payment/{}/".format(order.id)
                    )

                    payment_request_id = response['payment_request']['id']
                    url = response['payment_request']['longurl']

                    payment = Payment.objects.create(
                        order=Order(order.id),
                        payment_request_id=payment_request_id
                    )
                    return redirect(url)
                except Exception as e:
                    messages.warning(
                        request, 'Cart empty or Something went wrong !')
                    return HttpResponseRedirect('/')
            else:
                if not len(Cart.objects.filter(user=request.user)):
                    messages.warning(
                        request, 'Cart empty or Something went wrong !')
                    return HttpResponseRedirect('/')
                # Creating Order
                order = Order.objects.create(
                    order_status='PLACED',
                    address=Address(address),
                    payment_method=payment_method,
                    total=total
                )

                # Creating Order Item
                for item in Cart.objects.filter(user=request.user):
                    if item.product_variant != None:
                        order_item = OrderItem.objects.create(
                            order=Order(order.id),
                            product=Product(item.product.id),
                            product_variant=ProductVariant(
                                item.product_variant.id),
                            quantity=item.quantity,
                            price=(item.product_variant.price -
                                   (item.product_variant.price * item.product_variant.discount/100)),
                        )
                    else:
                        order_item = OrderItem.objects.create(
                            order=Order(order.id),
                            product=Product(item.product.id),
                            quantity=item.quantity,
                            price=(
                                item.product.price - (item.product.price * item.product.discount/100)),
                        )
                Cart.objects.filter(user=request.user).delete()
                return redirect('myorders')
    return render(request, 'checkout.html', context=context)


def ValidatePayment(request, pk):
    payment_request_id = request.GET.get('payment_request_id')
    payment_id = request.GET.get('payment_id')
    response = API.payment_request_payment_status(
        payment_request_id, payment_id)
    status = response.get('payment_request').get('payment').get('status')
    if status != "Failed":
        try:
            payment = Payment.objects.get(
                payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()

            order = payment.order
            order.order_status = "PLACED"
            order.save()

            Cart.objects.filter(user=request.user).delete()
            return redirect('myorders')
        except:
            return render(request, 'payment_failed.html')
    else:
        order = Order.objects.get(id=pk)
        order.delete()
        return render(request, 'payment_failed.html')


@login_required(login_url='/accounts/login/')
def Myorders(request):
    context = {
        'myorders': Order.objects.filter(address__user=request.user).order_by('-date').exclude(order_status='PENDING')
    }
    return render(request, 'myorders.html', context=context)


def Favicon(request):
    return HttpResponse("Nothing")
