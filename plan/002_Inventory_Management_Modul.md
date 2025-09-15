# 002 - Inventory Management Modul

## Cél
Az Inventory Management modul célja a termékek, készletek, szállítók és kategóriák hatékony kezelése az ERP rendszerben.

## Követelmények
- **Termékek kezelése**: CRUD műveletek termékekre (név, leírás, nettó ár, ÁFA, bruttó ár, kategória, szállító, kép)
- **Egyedi azonosítók**: Cikkszám (SKU) és EAN-13 vonalkód egyedi azonosításhoz
- **Készletkövetés**: Automatikus készletszint követés, alacsony készlet figyelmeztetések
- **Képkezelés**: Termékképek feltöltése, tárolása és megjelenítése (max 5MB)
- **Kategóriák**: Termékek kategorizálása
- **Szállítók**: Szállítói információk kezelése
- **Admin felület**: Teljes adminisztrációs felület
- **API készenlét**: Későbbi API integrációhoz való felkészítés

## Technikai specifikáció
- **Modellek**:
  - Product (Termék) - frissítve: ean13, net_price, vat_rate, image, brutto_price property
  - Category (Kategória)
  - Supplier (Szállító)
  - StockMovement (Készletmozgás)
- **Validációk**: Pozitív árak, egyedi termékkódok (SKU, EAN-13), képfájl méret (max 5MB)
- **Képkezelés**: Pillow könyvtár használata, MEDIA_ROOT/MEDIA_URL konfiguráció
- **Jogosultságok**: Szerepkör alapú hozzáférés
- **UI**: Bootstrap alapú reszponzív design, keret nélküli modern layout

## Implementációs terv
1. Inventory app létrehozása ✅
2. Modellek definiálása és migrációk ✅
3. Admin felület konfigurálása ✅
4. CRUD nézetek implementálása ✅
5. Sablonok létrehozása ✅
6. UI/UX fejlesztések (keretek eltávolítása) ✅
7. **EAN-13 vonalkód mező hozzáadása** ✅ **Befejezve** - Egyedi EAN-13 vonalkód mező, opcionális
8. **Ár/ÁFA kezelés frissítése (net_price, vat_rate, brutto_price)** ✅ **Befejezve** - Nettó ár + ÁFA kulcs → automatikus bruttó ár számítás
9. **Képfeltöltés implementálása (ImageField, Pillow)** ✅ **Befejezve** - Termékképek feltöltése, tárolása
10. **Médiafájlok konfigurálása** ✅ **Befejezve** - MEDIA_ROOT/MEDIA_URL beállítása
11. **Képvalidáció (max 5MB)** ✅ **Befejezve** - Fájlméret ellenőrzés
12. **Űrlapok és sablonok frissítése** ✅ **Befejezve** - Új mezők hozzáadása az űrlapokhoz és sablonokhoz
13. Tesztelés és validáció ⏳

## Adatmodell
```
Product
├── id (PK)
├── name (CharField)
├── sku (CharField, unique)
├── ean13 (CharField, unique) - ÚJ: EAN-13 vonalkód
├── description (TextField)
├── net_price (DecimalField) - FRISSÍTVE: Nettó ár
├── vat_rate (DecimalField, default=27.00) - ÚJ: ÁFA kulcs
├── brutto_price (@property) - ÚJ: Számított bruttó ár
├── image (ImageField) - ÚJ: Termékkép
├── category (FK -> Category)
├── supplier (FK -> Supplier)
├── stock_quantity (IntegerField)
├── min_stock_level (IntegerField)
├── created_at (DateTimeField)
└── updated_at (DateTimeField)

Category
├── id (PK)
├── name (CharField, unique)
├── description (TextField)
└── parent (FK -> Category, self-referencing)

Supplier
├── id (PK)
├── name (CharField)
├── contact_person (CharField)
├── email (EmailField)
├── phone (CharField)
├── address (TextField)
└── created_at (DateTimeField)

StockMovement
├── id (PK)
├── product (FK -> Product)
├── movement_type (CharField: IN/OUT/ADJUSTMENT)
├── quantity (IntegerField)
├── reason (TextField)
├── created_by (FK -> User)
└── created_at (DateTimeField)
```

## API Endpoints (jövőbeli)
- GET /api/inventory/products/ - Termékek listája
- POST /api/inventory/products/ - Új termék létrehozása
- GET /api/inventory/products/{id}/ - Termék részletei
- PUT /api/inventory/products/{id}/ - Termék módosítása
- DELETE /api/inventory/products/{id}/ - Termék törlése
- GET /api/inventory/stock/ - Készlet információk

## Biztonság
- Csapat alapú jogosultságok
- Audit log készletmozgásokra
- Validációk adat integritás biztosítása

## Tesztelés
- Unit tesztek modellekre
- Integration tesztek CRUD műveletekre
- UI tesztek admin felületen

## Befejezett feladatok
- ✅ Inventory app létrehozása
- ✅ Modellek definiálása és migrációk (Product, Category, Supplier, StockMovement)
- ✅ Admin felület konfigurálása
- ✅ CRUD nézetek implementálása
- ✅ Sablonok létrehozása
- ✅ Mintaadatok létrehozása
- ✅ Navigáció frissítése
- ✅ UI/UX fejlesztések (keretek eltávolítása, teljes szélességű layout, modern design)
- ✅ Reszponzív Bootstrap alapú felület
- ✅ Készletkövetés és alacsony készlet figyelmeztetések
- ✅ Készletmozgás rögzítés
- ✅ EAN-13 vonalkód mező implementálása
- ✅ Nettó ár + ÁFA kulcs → bruttó ár automatikus számítás
- ✅ Termékkép feltöltés (ImageField, Pillow)
- ✅ Médiafájlok konfigurálása (MEDIA_ROOT/MEDIA_URL)
- ✅ Képvalidáció (max 5MB méretkorlátozás)
- ✅ Űrlapok frissítése új mezőkkel
- ✅ Sablonok frissítése új mezők megjelenítéséhez
- ✅ Adatbázis migrációk futtatása

## Funkciók
- **Termék lista**: Keresés, szűrés, alacsony készlet figyelmeztetés, keret nélküli modern design
- **Termék CRUD**: Teljes létrehozás, olvasás, módosítás, törlés
- **Készletmozgás**: Automatikus készletkövetés, mozgás rögzítés, audit log
- **Kategóriák kezelése**: CRUD műveletek kategóriákra
- **Szállítók kezelése**: CRUD műveletek szállítókra
- **Admin felület**: Teljes adminisztrációs felület minden modellhez
- **Reszponzív UI**: Bootstrap alapú modern felület, sidebar layout, teljes szélességű termékadatok

## Fejlesztési kérések és jövőbeli fejlesztések

### UI/UX fejlesztések
- **Kinézet módosítása**: ✅ **Befejezve** - Teljesen fehér háttér, sidebar layout, eltávolított fejléc
  - Sidebar: 250px széles, fehér háttér, szürke elválasztó vonal
  - Reszponzív design mobil eszközökre
  - Modern, clean megjelenés

### Keresési funkciók fejlesztése
- **Automatikus keresés**: Enter nélkül, 3 karaktertől kezdjen keresni
- **Keresési mezők**: Cikkszám, vonalkód, megnevezés
- **Fuzzy search**: Sorrendtől független keresés (pl. "A4 papír 500 lap" vagy "500 A4")
- **Megvalósítás**: Full-text search vagy trigram similarity használata PostgreSQL-ben
- **Prioritás**: Közepes - alap funkciók után implementálandó

### Implementációs ütemezés
1. **Azonnali (most)**: ✅ **Befejezve** - Kinézet alapvető módosításai, keretek eltávolítása
2. **Közepes távú**: ✅ **Befejezve** - EAN-13 vonalkód, ár/ÁFA kezelés, képfeltöltés implementálása
3. **Hosszú távú**: Fuzzy search, API fejlesztések, további modulok

### Következő fejlesztési lépések
- ✅ **EAN-13 vonalkód mező** - Befejezve: egyedi azonosításhoz
- ✅ **Árkezelés frissítése**: net_price + vat_rate → brutto_price property - Befejezve
- ✅ **Termékkép feltöltés** implementálása (ImageField, Pillow) - Befejezve
- ✅ **Médiafájlok konfigurálása** (MEDIA_ROOT, MEDIA_URL) - Befejezve
- ✅ **Képvalidáció** (max 5MB méretkorlátozás) - Befejezve
- ✅ **Űrlapok és sablonok frissítése** az új mezőkhöz - Befejezve

---
*2025. szeptember 15. - Utolsó frissítés - Inventory modul teljes implementáció befejezve*

------------------------------------------------------------------------------------
Rendben, köszönöm a pontosításokat\! Tökéletesen érthető minden, a visszajelzéseid alapján frissítettem és véglegesítettem a termékkezelési modul tervét. A megadott információk alapján nincs további kérdésem, minden tiszta.

Ahogy megbeszéltük, itt van a részletes terv a **Termékkezelés Modulról**, a kéréseidnek megfelelően, markdown formátumban.

-----

## ERP Rendszerterv: Termékkezelés Modul

Ez a dokumentum az AI asszisztens által generált kód alapjául szolgáló ERP rendszerterv második modulját, a termékkezelést részletezi.

### 2\. Termékkezelés

**Funkció neve:** Termékkezelés

**Funkció leírása:**
Ez a modul felelős a rendszerben található összes termék adatainak központi nyilvántartásáért. Lehetővé teszi új termékek felvitelét, a meglévő termékek adatainak módosítását és megtekintését. A termékekhez olyan alapvető attribútumok tartoznak, mint a név, egyedi azonosítók (cikkszám, vonalkód), leírás, árak és termékkép. Ez a modul képezi az alapját a készletkezelésnek, a rendeléseknek és a webshop integrációnak.

**Funkció technológiai leírása:**

  * **Modell (`Product`):** Egy központi `Product` Django modell fogja tárolni az összes termékinformációt. A modell a következő mezőket tartalmazza:

      * `name` (CharField): A termék neve.
      * `sku` (CharField, `unique=True`): Egyedi cikkszám (Stock Keeping Unit). Az adatbázis szintjén garantált az egyedisége.
      * `ean13` (CharField, `unique=True`): Egyedi EAN-13 vonalkód. Szintén egyedi az adatbázisban.
      * `description` (TextField): A termék részletes leírása.
      * `net_price` (DecimalField): A termék nettó ára. `DecimalField` használata a lebegőpontos számítási hibák elkerülése végett kritikus.
      * `vat_rate` (DecimalField): A termékre vonatkozó ÁFA kulcs (pl. 27.00 a 27%-hoz).
      * `image` (ImageField): A termék képe. A képek a szerver lokális fájlrendszerébe kerülnek mentésre.
      * `created_at`, `updated_at` (DateTimeField): Automatikusan frissülő időbélyegek a létrehozás és utolsó módosítás időpontjáról.
      * **Számított mező:**
          * `brutto_price` (`@property`): A modellben egy Python propertyként lesz definiálva, ami futásidőben számolja ki a bruttó árat a `net_price` és `vat_rate` alapján. Így nem kell külön tárolni az adatbázisban, és mindig konzisztens marad.

    <!-- end list -->

    ```python
    # models.py példa
    from django.db import models

    class Product(models.Model):
        name = models.CharField(max_length=255)
        sku = models.CharField(max_length=100, unique=True, verbose_name="Cikkszám")
        ean13 = models.CharField(max_length=13, unique=True, verbose_name="EAN-13 Vonalkód")
        description = models.TextField(blank=True, null=True)
        net_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Nettó ár")
        vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=27.00, verbose_name="ÁFA kulcs (%)")
        image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Termékkép")
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        @property
        def brutto_price(self):
            if self.net_price is None or self.vat_rate is None:
                return 0
            return self.net_price * (1 + (self.vat_rate / 100))

        def __str__(self):
            return f"{self.name} ({self.sku})"
    ```

  * **Adatbázis:** PostgreSQL adatbázisban a `product` tábla `sku` és `ean13` oszlopain `UNIQUE` constraint lesz beállítva.

  * **Nézetek és URL-ek (Views & URLs):** Standard CRUD (Create, Read, Update, Delete) funkcionalitás megvalósítása:

      * Terméklista (`ProductListView`): Az összes termék táblázatos megjelenítése keresési és szűrési lehetőséggel.
      * Termék részletei (`ProductDetailView`): Egy adott termék összes adatának megjelenítése.
      * Termék létrehozása (`ProductCreateView`): Űrlap új termék felviteléhez.
      * Termék módosítása (`ProductUpdateView`): Meglévő termék adatainak szerkesztése.

  * **Képkezelés:** A `Pillow` Python könyvtár lesz használva a képfeldolgozáshoz. A `settings.py`-ben be lesz állítva a `MEDIA_ROOT` és `MEDIA_URL` a feltöltött képek tárolására és kiszolgálására.

**Funkció implementálási terve:**

1.  **Django App Létrehozása:** Egy új Django alkalmazás (`inventory`) létrehozása a `python manage.py startapp inventory` paranccsal.
2.  **Modell Definiálása:** A fenti `Product` modell definiálása az `inventory/models.py` fájlban.
3.  **Adatbázis Migráció:** A `python manage.py makemigrations inventory` és `python manage.py migrate` parancsok futtatása a `Product` tábla létrehozásához az adatbázisban.
4.  **Médiafájlok Konfigurálása:** A `config/settings/base.py`-ben a `MEDIA_ROOT` és `MEDIA_URL` változók beállítása, hogy a Django tudja, hova mentse a feltöltött képeket. A `Pillow` könyvtár telepítése.
5.  **Admin Felület:** A `Product` modell regisztrálása az `inventory/admin.py`-ban, hogy a Django admin felületén is kezelhető legyen.
6.  **Űrlapok (Forms) Létrehozása:** Egy `ProductForm` létrehozása a `forms.py`-ban, ami a `Product` modellen alapul. Itt kerül implementálásra a képfájl méretének validációja (max. 5MB).
7.  **Nézetek (Views) és Sablonok (Templates) Implementálása:**
      * A terméklista, részletes nézet, létrehozás és módosítás nézeteinek megírása az `inventory/views.py`-ban (ajánlott a Class-Based Views használata).
      * A hozzájuk tartozó HTML sablonok elkészítése a `templates/inventory/` mappában, Bootstrap 5 stílusokkal.
8.  **URL Konfiguráció:** Az új nézetekhez tartozó URL útvonalak felvétele a projekt `urls.py` és az `inventory` app `urls.py` fájljaiba.

**Javaslatok és jövőbeli bővítési lehetőségek:**

  * **Előkészületek a jövőre:** Bár most nem kerülnek implementálásra, a groundwork (előkészületek) megtehetők a kapcsolódó termékek és értékelések számára. Ez egy `ManyToManyField` hozzáadását jelentené a `Product` modellhez önmagára (`related_products`) és egy új `Review` modell létrehozását `ForeignKey`-jel a `Product`-hoz.
  * **Partner API:** A termékadatok külső partnerek számára történő elérhetővé tétele egy külön, "API" vagy "Integrációk" elnevezésű modul keretein belül lesz kidolgozva, API kulcs alapú authentikációval és a megbeszélt, napi egyszeri adatszinkronizálási logikával.

**Funkció technológiai "buktatók" és megoldások:**

  * **Adatintegritás (SKU/EAN ismétlődés):**
      * **Probléma:** Két termék nem rendelkezhet ugyanazzal a cikkszámmal vagy vonalkóddal.
      * **Megoldás:** A modellben a `unique=True` paraméter a `sku` és `ean13` mezőkön adatbázis-szintű kényszert hoz létre. A Django `ModelForm` validációja ezt automatikusan lekezeli, és felhasználóbarát hibaüzenetet ad ("Ezzel a cikkszámmal már létezik termék."), mielőtt az adatbázis `IntegrityError`-t dobna.
  * **Árkezelés (pénzügyi pontosság):**
      * **Probléma:** A `float` típus használata pénzügyi számításoknál kerekítési hibákhoz vezethet.
      * **Megoldás:** A `DecimalField` használata kötelező minden pénzügyi adat (ár, ÁFA) tárolására, mivel ez pontosan kezeli a tizedesjegyeket.
  * **Képkezelés:**
      * **Probléma:** Túl nagy képfájlok feltöltése lassíthatja a rendszert és sok tárhelyet foglalhat. A feltöltés megszakadhat.
      * **Megoldás:** A `ProductForm`-ban egyedi validátorral ellenőrizzük a feltöltött fájl méretét (max. 5MB). Production környezetben az Nginx `client_max_body_size` direktívájának beállítása is szükséges lehet a nagyobb fájlok fogadásához.
  * **Adatbázis teljesítmény:**
      * **Probléma:** Nagyszámú termék esetén a keresés a nem indexelt mezőkben lassú lehet.
      * **Megoldás:** A `unique=True` constraint automatikusan létrehoz egy indexet a `sku` és `ean13` oszlopokon, ami villámgyors keresést tesz lehetővé ezekre az azonosítókra. A jövőben a terméknév (`name`) mezőre is érdemes lehet indexet helyezni.

-----

Készen állunk a következő modulra\! A logikus következő lépés a **Raktár- és Készletkezelés** lenne, ami szorosan épít a most definiált Termék modulra. Mit gondolsz, folytassuk ezzel?