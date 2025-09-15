from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Category, Supplier, StockMovement, ProductImage
from decimal import Decimal


def validate_image_size(value):
    """Validate image file size (max 5MB)"""
    if value:
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if value.size > max_size:
            raise ValidationError('A kép mérete nem lehet nagyobb 5MB-nál.')


class ProductForm(forms.ModelForm):
    """Form for Product model with custom validation"""

    PRICE_INPUT_CHOICES = [
        ('net', 'Nettó ár megadása'),
        ('gross', 'Bruttó ár megadása'),
    ]

    price_input_type = forms.ChoiceField(
        choices=PRICE_INPUT_CHOICES,
        initial='net',
        label='Ár bevitel típusa',
        widget=forms.RadioSelect
    )

    gross_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        label='Bruttó ár',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'sku', 'ean13', 'net_price', 'vat_rate',
            'category', 'supplier', 'stock_quantity', 'min_stock_level'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'net_price': forms.NumberInput(attrs={'step': '0.01'}),
            'vat_rate': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional in form
        self.fields['ean13'].required = False
        self.fields['net_price'].required = False
        # Set initial values for price fields
        if self.instance and self.instance.pk:
            # Ensure gross initial value is rounded to 2 decimals so the
            # browser's number input (step) doesn't reject edits due to
            # an offset fractional part coming from Decimal arithmetic.
            try:
                self.fields['gross_price'].initial = Decimal(self.instance.brutto_price).quantize(Decimal('0.01'))
            except Exception:
                # Fallback to raw value if quantize fails for any reason
                self.fields['gross_price'].initial = self.instance.brutto_price
            try:
                self.fields['net_price'].initial = Decimal(self.instance.net_price).quantize(Decimal('0.01'))
            except Exception:
                self.fields['net_price'].initial = self.instance.net_price

        # Ensure consistent widget classes/attributes for styling
        for name, field in self.fields.items():
            widget = field.widget
            # add form-control class for bootstrap and our CSS
            existing_classes = widget.attrs.get('class', '')
            classes = (existing_classes + ' form-control').strip()
            widget.attrs['class'] = classes
            # add step for number inputs if not present
            if isinstance(widget, forms.NumberInput) and 'step' not in widget.attrs:
                widget.attrs['step'] = '0.01'
            # make textareas smaller by default
            if isinstance(widget, forms.Textarea) and 'rows' not in widget.attrs:
                widget.attrs['rows'] = 3

    def clean(self):
        cleaned_data = super().clean()
        price_input_type = cleaned_data.get('price_input_type')
        net_price = cleaned_data.get('net_price')
        gross_price = cleaned_data.get('gross_price')
        vat_rate = cleaned_data.get('vat_rate', 27.00)

        if price_input_type == 'gross':
            if not gross_price:
                raise forms.ValidationError("Bruttó ár megadása kötelező, ha bruttó bevitel van kiválasztva.")
            cleaned_data['net_price'] = (gross_price / (1 + (vat_rate / 100))).quantize(Decimal('0.01'))
            # Validate the calculated net_price against the field constraints
            net_price_field = self.fields['net_price']
            net_price_field.validate(cleaned_data['net_price'])
        elif price_input_type == 'net':
            if not net_price:
                raise forms.ValidationError("Nettó ár megadása kötelező, ha nettó bevitel van kiválasztva.")
            # Net price is already set

        return cleaned_data

    def clean_ean13(self):
        """Validate EAN-13 format if provided"""
        ean13 = self.cleaned_data.get('ean13')
        if ean13:
            # Basic EAN-13 validation (13 digits)
            if not ean13.isdigit() or len(ean13) != 13:
                raise forms.ValidationError('Az EAN-13 vonalkódnak 13 számjegyből kell állnia.')
        return ean13


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ProductImageForm(forms.ModelForm):
    """Form for ProductImage model"""

    class Meta:
        model = ProductImage
        fields = ['image', 'alt_text', 'is_main']
        widgets = {
            'alt_text': forms.TextInput(attrs={'placeholder': 'Kép leírása (opcionális)'}),
        }

    def clean_image(self):
        """Validate image file"""
        image = self.cleaned_data.get('image')
        if image:
            validate_image_size(image)
        return image
class StockMovementForm(forms.ModelForm):
    """Form for StockMovement model"""

    class Meta:
        model = StockMovement
        fields = ['movement_type', 'quantity', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.product:
            instance.product = self.product
        if commit:
            instance.save()
        return instance