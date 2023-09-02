from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


# Register your models here.

class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('pk', 'title', 'parent', 'get_products_count')
    list_display_links = ('title',)

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_products_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category',
                    'created_at', 'size', 'color',
                    'material', 'quantity', 'price',
                    'get_photo')
    prepopulated_fields = {'slug': ('title',)}
    list_display_links = ('title',)
    list_editable = ('size', 'quantity', 'color', 'material', 'price')
    list_filter = ('title', 'size', 'color', 'material', 'category')
    inlines = [GalleryInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="50">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'created_at')
    readonly_fields = ('author', 'text', 'created_at')


admin.site.register(Gallery)
