from django.contrib import admin
from .models import *
import nested_admin


admin.site.register(Categories)
admin.site.register(SubCategories)
admin.site.register(SubCategoriesVariant)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Setting)
admin.site.register(Slider)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(DealOfDay)

# Managing Product and its related media and Product Variant and its related media.


class ProductMediaAdmin(nested_admin.NestedTabularInline):
    model = ProductMedia
    extra = 1
    readonly_fields = ('image_preview',)


class ProductVariantMediaAdmin(nested_admin.NestedTabularInline):
    model = ProductVariantMedia
    extra = 1
    readonly_fields = ('image_preview',)


class ProductVariantAdmin(nested_admin.NestedTabularInline):
    model = ProductVariant
    inlines = [ProductVariantMediaAdmin]
    extra = 1


class ProductAdmin(nested_admin.NestedModelAdmin):
    model = Product
    inlines = [ProductMediaAdmin, ProductVariantAdmin]
    list_display = ['title']


admin.site.register(Product, ProductAdmin)
