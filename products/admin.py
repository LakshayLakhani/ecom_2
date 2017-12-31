from django.contrib import admin

from .models import Product, Variation, ProductImage, Category, ProductFeatured

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','price',]
    inlines = [
        ProductImageInline,
        VariationInline
    ]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(Category)

# admin.site.register(Product, ProductAdmin)

# admin.site.register(Variation)

admin.site.register(ProductImage)

admin.site.register(ProductFeatured)
