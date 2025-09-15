from django.contrib import admin
from .models import Category, Supplier, Product, StockMovement, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'get_product_count']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    ordering = ['name']

    def get_product_count(self, obj):
        return obj.product_set.count()
    get_product_count.short_description = "Termékek száma"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone']
    search_fields = ['name', 'contact_person', 'email']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'brutto_price', 'image_count', 'stock_quantity',
        'min_stock_level', 'category', 'supplier', 'stock_status'
    ]
    list_filter = ['category', 'supplier']
    search_fields = ['name', 'sku', 'ean13', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at', 'brutto_price']

    fieldsets = (
        ('Alapadatok', {
            'fields': ('name', 'description', 'sku', 'ean13')
        }),
        ('Árazás', {
            'fields': ('net_price', 'vat_rate', 'brutto_price')
        }),
        ('Kategorizálás', {
            'fields': ('category', 'supplier')
        }),
        ('Készlet', {
            'fields': ('stock_quantity', 'min_stock_level')
        }),
        ('Időbélyegek', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_count(self, obj):
        return obj.image_count
    image_count.short_description = "Képek száma"

    def brutto_price(self, obj):
        return f"{obj.brutto_price:.2f} Ft"
    brutto_price.short_description = "Bruttó ár"

    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return "❌ Kifogyott"
        elif obj.is_low_stock:
            return "⚠️ Alacsony készlet"
        else:
            return "✅ Elérhető"
    stock_status.short_description = "Készlet státusz"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'alt_text', 'is_main', 'order', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name', 'product__sku', 'alt_text']
    ordering = ['product', 'order']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Kapcsolat', {
            'fields': ('product',)
        }),
        ('Kép adatok', {
            'fields': ('image', 'alt_text', 'is_main', 'order')
        }),
        ('Időbélyeg', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
class StockMovementAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'movement_type', 'quantity',
        'created_by', 'created_at'
    ]
    list_filter = ['movement_type', 'created_at', 'created_by']
    search_fields = ['product__name', 'product__sku', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Mozgás adatok', {
            'fields': ('product', 'movement_type', 'quantity')
        }),
        ('Részletek', {
            'fields': ('reason', 'created_by')
        }),
        ('Időbélyeg', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Set created_by when creating new movement"""
        if not change:  # Only for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
