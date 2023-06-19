from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from math import floor


# Categories , Subcategories and SubcategoreisVariant Model

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    slug = models.CharField(max_length=50, null=False,
                            blank=False, unique=True)
    thumbnail = models.ImageField(
        upload_to='categories/', null=False, blank=False)

    def __str__(self):
        return self.slug


class SubCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    slug = models.CharField(max_length=50, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.slug


class SubCategoriesVariant(models.Model):
    id = models.AutoField(primary_key=True)
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    slug = models.CharField(max_length=50, null=False,
                            blank=False, unique=True)

    def __str__(self):
        return self.subcategory.__str__() + ' - ' + self.slug


# Product , ProductMedia , ProductVariant and its related ProductVariantMediaModel etc Model.

class Color(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color')
    )
    id = models.AutoField(primary_key=True)
    subcategoryvariant = models.ForeignKey(
        SubCategoriesVariant, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    keywords = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    detail = RichTextField(null=False, blank=False)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True, default=None)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, null=True, blank=True, default=None)
    slug = models.SlugField(null=False, blank=False, unique=True)
    variant = models.CharField(max_length=20, choices=VARIANTS, default='None')
    status = models.CharField(max_length=10, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProductMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    @property
    def image_preview(self):
        if self.image:
            _image = get_thumbnail(self.image,
                                   '100x100',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            return mark_safe('<img src="{}" width="{}" height="{}">'.format(_image.url, _image.width, _image.height))
        return ""


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True)
    size = models.ForeignKey(
        Size, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ProductVariantMedia(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='products/variants/', null=True, blank=True)

    @property
    def image_preview(self):
        if self.image:
            _image = get_thumbnail(self.image,
                                   '100x100',
                                   upscale=False,
                                   crop=False,
                                   quality=100)
            return mark_safe('<img src="{}" width="{}" height="{}">'.format(_image.url, _image.width, _image.height))
        return ""


# Company info Model

class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    title = models.CharField(max_length=150)
    keyword = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=50)
    address = models.CharField(null=True, blank=True, max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    fax = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True, max_length=50)
    smtpserver = models.CharField(null=True, blank=True, max_length=50)
    smtpemail = models.EmailField(null=True, blank=True, max_length=50)
    smtppassword = models.CharField(null=True, blank=True, max_length=20)
    icon = models.ImageField(null=True, blank=True, upload_to='store/')
    facebook = models.CharField(null=True, blank=True, max_length=50)
    instagram = models.CharField(null=True, blank=True, max_length=50)
    twitter = models.CharField(null=True, blank=True, max_length=50)
    youtube = models.CharField(null=True, blank=True, max_length=50)
    aboutus = RichTextField(null=True, blank=True)
    contact = RichTextField(null=True, blank=True)
    references = RichTextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# Slider
class Slider(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='slider/')


# Managing Shopping Cart
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def cart_total(self, user):
        sum = 0
        for item in Cart.objects.filter(user=user):
            if item.product_variant != None:
                sum += (item.product_variant.price - (item.product_variant.price *
                        item.product_variant.discount/100)) * item.quantity
            else:
                sum += (item.product.price - (item.product.price *
                        item.product.discount/100)) * item.quantity
        return floor(sum)


# Address
class Address(models.Model):
    STATES = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Delhi', 'Delhi'),
        ('Goa', 'Goa'),
        ('Gujrat', 'Gujrat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharastra', 'Maharastra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    )
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=200)
    state = models.CharField(
        max_length=50, choices=STATES, null=False, blank=False)
    zipcode = models.IntegerField(default=None)
    phone_no = models.CharField(max_length=100, null=False, blank=False)

# Orders and Payments


class Order(models.Model):
    OrderStatus = (
        ('PENDING', 'Pending'),
        ('PLACED', 'Placed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    )
    Method = (
        ('ONLINE', 'Online'),
        ('COD', 'Cash Delivery')
    )
    id = models.AutoField(primary_key=True)
    order_status = models.CharField(max_length=15, choices=OrderStatus)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, default=None)
    payment_method = models.CharField(max_length=15, choices=Method)
    total = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=15, default='FAILED')
    payment_id = models.CharField(max_length=200)
    payment_request_id = models.CharField(
        max_length=200, unique=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)


# Trending Product & Deal of the Day
class DealOfDay(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.title
