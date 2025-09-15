from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from .models import Product, Category, Supplier, StockMovement, ProductImage
from .forms import ProductForm, CategoryForm, SupplierForm, StockMovementForm, ProductImageForm


@login_required
def product_list(request):
    """List all products with search and filtering"""
    products = Product.objects.all()
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    low_stock_products = products.filter(stock_quantity__lte=F('min_stock_level'))

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'inventory/product_list.html', context)


@login_required
def product_warnings(request):
    """List products with warnings (low stock, negative stock)"""
    products = Product.objects.filter(
        Q(stock_quantity__lte=F('min_stock_level')) | Q(stock_quantity__lt=0)
    ).order_by('stock_quantity')  # Negative first, then low stock

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    }
    return render(request, 'inventory/product_warnings.html', context)


@login_required
def product_detail(request, pk):
    """Show product details"""
    product = get_object_or_404(Product, pk=pk)
    stock_movements = StockMovement.objects.filter(product=product).order_by('-created_at')[:10]

    context = {
        'product': product,
        'stock_movements': stock_movements,
    }
    return render(request, 'inventory/product_detail.html', context)


@login_required
def product_create(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Use commit=False so we can ensure computed fields from the form
            product = form.save(commit=False)
            # Ensure net_price from cleaned_data (clean() may have calculated it from gross)
            net_price = form.cleaned_data['net_price']
            product.net_price = net_price
            product.save()

            # Handle image uploads (no deletions on create)
            images = request.FILES.getlist('images')
            # Only allow up to 5 images total
            current_image_count = product.images.count()
            max_new = max(0, 5 - current_image_count)
            for image in images[:max_new]:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, f'Termék "{product.name}" sikeresen létrehozva.')
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'title': 'Új termék létrehozása'
    })
@login_required
def product_update(request, pk):
    """Update an existing product"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Save form but allow us to enforce computed fields
            product = form.save(commit=False)
            net_price = form.cleaned_data['net_price']
            product.net_price = net_price
            product.save()

            # Handle image deletions first so we free up slots for new uploads
            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                ProductImage.objects.filter(id__in=delete_image_ids, product=product).delete()

            # Handle image uploads (respect max 5 images total)
            images = request.FILES.getlist('images')
            current_image_count = product.images.count()
            max_new_images = max(0, 5 - current_image_count)
            for image in images[:max_new_images]:
                ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, f'Termék "{product.name}" sikeresen módosítva. Nettó ár: {product.net_price}, Bruttó ár: {product.brutto_price}')
            return redirect('inventory:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Termék módosítása: {product.name}'
    })
@login_required
def product_delete(request, pk):
    """Delete a product"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Termék "{product_name}" sikeresen törölve.')
        return redirect('inventory:product_list')

    return render(request, 'inventory/product_confirm_delete.html', {
        'product': product
    })


@login_required
def category_list(request):
    """List all categories"""
    categories = Category.objects.all()
    return render(request, 'inventory/category_list.html', {
        'categories': categories
    })


@login_required
def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Kategória "{category.name}" sikeresen létrehozva.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()

    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': 'Új kategória létrehozása'
    })


@login_required
def category_update(request, pk):
    """Update an existing category"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Kategória "{category.name}" sikeresen módosítva.')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'inventory/category_form.html', {
        'form': form,
        'category': category,
        'title': f'Kategória módosítása: {category.name}'
    })


@login_required
def category_delete(request, pk):
    """Delete a category"""
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Kategória "{category_name}" sikeresen törölve.')
        return redirect('inventory:category_list')

    return render(request, 'inventory/category_confirm_delete.html', {
        'category': category
    })


@login_required
def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {
        'suppliers': suppliers
    })


@login_required
def supplier_create(request):
    """Create a new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Szállító "{supplier.name}" sikeresen létrehozva.')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Új szállító létrehozása'
    })


@login_required
def supplier_update(request, pk):
    """Update an existing supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Szállító "{supplier.name}" sikeresen módosítva.')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'supplier': supplier,
        'title': f'Szállító módosítása: {supplier.name}'
    })


@login_required
def supplier_delete(request, pk):
    """Delete a supplier"""
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Szállító "{supplier_name}" sikeresen törölve.')
        return redirect('inventory:supplier_list')

    return render(request, 'inventory/supplier_confirm_delete.html', {
        'supplier': supplier
    })


@login_required
def stock_movement_list(request):
    """List stock movements"""
    movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')
    return render(request, 'inventory/stock_movement_list.html', {
        'movements': movements
    })


@login_required
def stock_movement_create(request):
    """Create a new stock movement"""
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.created_by = request.user
            movement.save()
            messages.success(request, 'Készletmozgás sikeresen rögzítve.')
            return redirect('inventory:stock_movement_list')
    else:
        form = StockMovementForm()

    return render(request, 'inventory/stock_movement_form.html', {
        'form': form,
        'title': 'Új készletmozgás'
    })


@login_required
def add_to_order(request, pk):
    """Add a product to a simple session-based cart (placeholder for future order module)"""
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        # increment quantity for this product in session cart
        cart_item = cart.get(str(product.pk), {'quantity': 0})
        cart_item['quantity'] = cart_item.get('quantity', 0) + 1
        cart[str(product.pk)] = cart_item
        request.session['cart'] = cart
        messages.success(request, f'"{product.name}" hozzáadva a rendeléshez.')
        return redirect('inventory:product_detail', pk=product.pk)

    # For non-POST fallback, redirect back
    return redirect('inventory:product_detail', pk=product.pk)
