from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Category(models.Model):
    """Product categories with hierarchical structure"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Név")
    description = models.TextField(blank=True, verbose_name="Leírás")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Szülő kategória"
    )

    class Meta:
        verbose_name = "Kategória"
        verbose_name_plural = "Kategóriák"
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent} > {self.name}"
        return self.name

    def get_full_path(self):
        """Get the full category path"""
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Supplier(models.Model):
    """Product suppliers"""
    name = models.CharField(max_length=200, verbose_name="Név")
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Kapcsolattartó")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    address = models.TextField(blank=True, verbose_name="Cím")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Létrehozva")

    class Meta:
        verbose_name = "Szállító"
        verbose_name_plural = "Szállítók"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model with inventory tracking"""
    name = models.CharField(max_length=200, verbose_name="Név")
    description = models.TextField(blank=True, verbose_name="Leírás")
    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Cikkszám",
        help_text="Egyedi cikkszám"
    )
    ean13 = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        null=True,
        verbose_name="EAN-13 Vonalkód",
        help_text="Egyedi EAN-13 vonalkód"
    )
    net_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Nettó ár"
    )
    vat_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=27.00,
        validators=[MinValueValidator(0)],
        verbose_name="ÁFA kulcs (%)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kategória"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Szállító"
    )
    stock_quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Készlet mennyiség"
    )
    min_stock_level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Minimum készlet szint",
        help_text="Figyelmeztetés alatt ez a szint"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Létrehozva")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Módosítva")

    class Meta:
        verbose_name = "Termék"
        verbose_name_plural = "Termékek"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def brutto_price(self):
        """Calculate brutto price from net price and VAT rate"""
        from decimal import Decimal, ROUND_HALF_UP
        if self.net_price is None or self.vat_rate is None:
            return Decimal('0.00')

        # Ensure Decimal math and round to 2 decimal places for display/storage
        net = Decimal(self.net_price)
        vat_mult = Decimal(1) + (Decimal(self.vat_rate) / Decimal(100))
        brutto = (net * vat_mult).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return brutto

    @property
    def main_image(self):
        """Get the main product image"""
        return self.images.filter(is_main=True).first() or self.images.first()

    @property
    def image_count(self):
        """Get the number of images for this product"""
        return self.images.count()

    @property
    def is_low_stock(self):
        """Check if product is below minimum stock level"""
        return self.stock_quantity <= self.min_stock_level

    @property
    def stock_status(self):
        """Get stock status as string"""
        if self.stock_quantity == 0:
            return "Kifogyott"
        elif self.is_low_stock:
            return "Alacsony készlet"
        else:
            return "Elérhető"


class ProductImage(models.Model):
    """Product images - multiple images per product (max 5)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Termék"
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name="Kép"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Alternatív szöveg"
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Fő kép"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sorrend"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Feltöltve")

    class Meta:
        verbose_name = "Termékkép"
        verbose_name_plural = "Termékképek"
        ordering = ['order', 'created_at']
        # unique_together = ['product', 'is_main']  # Removed, handled in save()

    def __str__(self):
        return f"{self.product.name} - Kép {self.order + 1}"

    def save(self, *args, **kwargs):
        """Ensure only one main image per product"""
        if self.is_main:
            # Set all other images for this product to not main
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
class StockMovement(models.Model):
    """Stock movement tracking"""
    MOVEMENT_TYPES = [
        ('IN', 'Beérkezés'),
        ('OUT', 'Kivétel'),
        ('ADJUSTMENT', 'Korrekció'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Termék"
    )
    movement_type = models.CharField(
        max_length=10,
        choices=MOVEMENT_TYPES,
        verbose_name="Mozgás típusa"
    )
    quantity = models.IntegerField(verbose_name="Mennyiség")
    reason = models.TextField(blank=True, verbose_name="Indok")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Létrehozó"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Létrehozva")

    class Meta:
        verbose_name = "Készletmozgás"
        verbose_name_plural = "Készletmozgások"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"

    def save(self, *args, **kwargs):
        """Update product stock when movement is saved"""
        super().save(*args, **kwargs)

        # Update product stock quantity
        if self.movement_type == 'IN':
            self.product.stock_quantity += self.quantity
        elif self.movement_type == 'OUT':
            self.product.stock_quantity -= self.quantity
        elif self.movement_type == 'ADJUSTMENT':
            # For adjustments, quantity can be positive or negative
            self.product.stock_quantity += self.quantity

        # Ensure stock doesn't go below 0
        if self.product.stock_quantity < 0:
            self.product.stock_quantity = 0

        self.product.save()
