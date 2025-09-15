#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from inventory.models import Category, Supplier, Product

def create_sample_data():
    print("Creating sample inventory data...")

    # Create categories
    categories_data = [
        {"name": "Elektronika", "description": "Elektronikai termékek"},
        {"name": "Irodaszer", "description": "Irodai eszközök és kellékek"},
        {"name": "Bútor", "description": "Irodai és otthoni bútorok"},
        {"name": "Számítástechnika", "description": "Számítógépek és kiegészítők"},
    ]

    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories[cat_data["name"]] = cat
        if created:
            print(f"Created category: {cat.name}")

    # Create suppliers
    suppliers_data = [
        {
            "name": "TechCorp Kft.",
            "contact_person": "Kovács János",
            "email": "kovacs.janos@techcorp.hu",
            "phone": "+36 1 234 5678",
            "address": "Budapest, Kossuth Lajos utca 1."
        },
        {
            "name": "OfficePlus Zrt.",
            "contact_person": "Nagy Anna",
            "email": "nagy.anna@officeplus.hu",
            "phone": "+36 1 876 5432",
            "address": "Debrecen, Piac utca 15."
        },
        {
            "name": "FurnitureMax Kft.",
            "contact_person": "Szabó Péter",
            "email": "szabo.peter@furnituremax.hu",
            "phone": "+36 1 345 6789",
            "address": "Szeged, Fő utca 25."
        },
    ]

    suppliers = {}
    for supp_data in suppliers_data:
        supp, created = Supplier.objects.get_or_create(
            name=supp_data["name"],
            defaults={
                "contact_person": supp_data["contact_person"],
                "email": supp_data["email"],
                "phone": supp_data["phone"],
                "address": supp_data["address"]
            }
        )
        suppliers[supp_data["name"]] = supp
        if created:
            print(f"Created supplier: {supp.name}")

    # Create products
    products_data = [
        {
            "name": "Dell Laptop Inspiron 15",
            "sku": "DELL-INSP-15-001",
            "price": 250000,
            "category": categories["Számítástechnika"],
            "supplier": suppliers["TechCorp Kft."],
            "stock_quantity": 5,
            "min_stock_level": 2,
            "description": "15.6\" Full HD laptop, Intel Core i5, 8GB RAM, 256GB SSD"
        },
        {
            "name": "HP LaserJet Pro nyomtató",
            "sku": "HP-LJP-PRO-001",
            "price": 45000,
            "category": categories["Elektronika"],
            "supplier": suppliers["TechCorp Kft."],
            "stock_quantity": 3,
            "min_stock_level": 1,
            "description": "Lézer nyomtató, fekete-fehér, USB és hálózati csatlakozás"
        },
        {
            "name": "Office szék ergonomikus",
            "sku": "OFFICE-CHAIR-ERG-001",
            "price": 35000,
            "category": categories["Bútor"],
            "supplier": suppliers["FurnitureMax Kft."],
            "stock_quantity": 8,
            "min_stock_level": 3,
            "description": "Fekete ergonomikus irodai szék, állítható magasság"
        },
        {
            "name": "A4 papír 500 lap",
            "sku": "PAPER-A4-500-001",
            "price": 1200,
            "category": categories["Irodaszer"],
            "supplier": suppliers["OfficePlus Zrt."],
            "stock_quantity": 50,
            "min_stock_level": 10,
            "description": "80g/m² A4 fehér papír, 500 lapos csomag"
        },
        {
            "name": "Logitech vezeték nélküli egér",
            "sku": "LOGI-MOUSE-WL-001",
            "price": 8500,
            "category": categories["Számítástechnika"],
            "supplier": suppliers["TechCorp Kft."],
            "stock_quantity": 12,
            "min_stock_level": 5,
            "description": "Vezeték nélküli optikai egér, USB receiver"
        },
        {
            "name": "Pilot toll kék",
            "sku": "PILOT-PEN-BLUE-001",
            "price": 250,
            "category": categories["Irodaszer"],
            "supplier": suppliers["OfficePlus Zrt."],
            "stock_quantity": 100,
            "min_stock_level": 20,
            "description": "Kék golyóstoll, 0.7mm, dobozban 12 db"
        },
    ]

    for prod_data in products_data:
        prod, created = Product.objects.get_or_create(
            sku=prod_data["sku"],
            defaults={
                "name": prod_data["name"],
                "price": prod_data["price"],
                "category": prod_data["category"],
                "supplier": prod_data["supplier"],
                "stock_quantity": prod_data["stock_quantity"],
                "min_stock_level": prod_data["min_stock_level"],
                "description": prod_data["description"]
            }
        )
        if created:
            print(f"Created product: {prod.name} ({prod.sku})")

    print("Sample data creation completed!")

if __name__ == "__main__":
    create_sample_data()