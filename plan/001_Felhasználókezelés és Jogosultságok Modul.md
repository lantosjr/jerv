# ERP Rendszerterv: Felhasználókezelés és Jogosultságok Modul

Ez a dokumentum az AI asszisztens által generált kód alapjául szolgáló ERP rendszerterv első modulját, a felhasználókezelést és jogosultságokat részletezi.

## 1. Felhasználókezelés és Jogosultságok

### Funkció neve: Felhasználókezelés és Jogosultságok

### Funkció leírása:
Ez a modul felelős a rendszerbe való bejelentkezésért, a felhasználói fiókok kezeléséért (létrehozás, módosítás, jelszókezelés, felfüggesztés/aktiválás), valamint a felhasználókhoz rendelt jogosultságok (szerepkörök) kezeléséért. Meghatározza, hogy melyik felhasználó milyen műveleteket végezhet el a rendszerben.

### Funkció technológiai leírása:
*   **Django Authentication System:** A Django beépített autentikációs rendszere (User modell, Group modell, Permission modell) lesz az alapja. Ez kezeli a felhasználók (username, password, email), jelszavak hashelését, munkameneteket (sessions) és alapvető jogosultságokat.
*   **Custom User Model:** Egy egyedi felhasználói modell kerül kialakításra (`AbstractUser` kiterjesztésével), hogy a jövőbeni igényeknek megfelelően bővíthető legyen (pl. telefonszám, cégnév, extra profil adatok).
*   **Django Admin:** A Django admin felületét használjuk a felhasználók és jogosultságok egyszerű kezelésére.
*   **Session Management:** Django beépített session mechanizmusát alkalmazzuk.
*   **Jogosultságkezelés (Roles):** A rendszer három definiált szerepkört (`felhasználó`, `admin`, `sysadmin`) használ, melyek Django `Group` modellekkel lesznek implementálva. Ezekhez a csoportokhoz egyedi Django `Permission` objektumokat rendelünk:
    *   **Felhasználó (User):** Bármit megtehet a rendszerben, kivéve a törlést. Alapértelmezetten minden `view`, `create`, `update` jogosultsággal rendelkezik az összes releváns modellen, kivéve a `delete` jogosultságot.
    *   **Admin:** Bármit megtehet, beleértve a törlést is. Rendelkezik minden `view`, `create`, `update`, `delete` jogosultsággal.
    *   **Sysadmin:** Minden jogosultság, plusz a rendszerbeállítások kezelése (pl. új API kulcsok hozzáadása, webshopok konfigurálása, felhasználók hozzárendelése szerepkörökhöz). Ezeket a specifikus műveleteket egyedi jogosultságok (`custom permissions`) formájában valósítjuk meg, amiket csak a `sysadmin` csoport kap meg.
*   **Jelszó házirend:** Lehetővé tesszük a jelszókomplexitási szabályok beállítását (minimum hossz, speciális karakterek, stb.).
*   **Munkamenet kezelés:** A felhasználó bejelentkezése után session token generálódik, ami meghatározott ideig érvényes.

### Funkció implementálási terve:
1.  **Projekt beállítások:**
    *   Konfiguráljuk a `settings.py` fájlt az `AUTH_USER_MODEL` beállítással, hogy az egyedi felhasználói modellünket használja.
    *   Készítsük elő a `docker-compose.yml` fájlt a Django app, PostgreSQL adatbázis és opcionálisan Nginx konténerekkel, biztosítva a fejlesztési környezet Dockerizálását.
    *   Inicializáljuk a PostgreSQL adatbázist a konténer indításakor.
2.  **Custom User Model Létrehozása:**
    *   Hozzuk létre az `accounts` (vagy `users`) Django app-et.
    *   Definiáljuk a `CustomUser` modellt, amely kiterjeszti a Django `AbstractUser` osztályát. Ebbe a modellbe felvehetünk további mezőket, mint pl. `phone_number`, `company_name`.
    *   Futtassuk a migrációkat (`python manage.py makemigrations accounts` és `python manage.py migrate`).
3.  **Szerepkörök (Groups) beállítása:**
    *   A Django admin felületén vagy egy adatbázis migráció (`data migration`) segítségével hozzuk létre a `felhasználó`, `admin`, `sysadmin` csoportokat.
    *   Ezekhez a csoportokhoz rendeljük hozzá a megfelelő alapértelmezett jogosultságokat (modellenkénti `add`, `change`, `view` a `felhasználó` csoportnak; `delete` jogosultságok is az `admin` csoportnak).
    *   Az egyedi (custom) jogosultságokat (pl. `can_manage_settings` a sysadmin számára) definiáljuk a modellek `Meta` osztályában.
4.  **Admin felület konfigurálása:**
    *   Regisztráljuk a `CustomUser` modellt és a `Group` modellt a Django admin felületén (`admin.py`), hogy könnyen kezelhetők legyenek.
    *   Készítsünk egy `UserAdmin` osztályt a `CustomUser` modellhez, ami lehetővé teszi a csoportokhoz való hozzárendelést az admin felületen.
5.  **Autentikációs nézetek (Views) és URL-ek:**
    *   Implementáljuk a bejelentkezés (`login`), kijelentkezés (`logout`), jelszóváltoztatás (`password_change`) és jelszó-visszaállítás (`password_reset`) funkciókat, a Django `auth.views` moduljának sablon alapú nézeteit felhasználva.
    *   Definiáljuk az URL-eket ezekhez a nézetekhez az `urls.py` fájlban.
6.  **Jogosultságkezelés a kód szintjén:**
    *   **Decoratorok:** Használjunk Django `permission_required` vagy `user_passes_test` decoratorokat a nézetek (views) tetején a jogosultság ellenőrzésére.
    *   **Template szintű ellenőrzések:** A sablonokban (templates) ellenőrizzük a felhasználó jogosultságait (pl. `{% if perms.app_name.can_delete_product %}`), hogy csak a releváns gombokat/linkeket jelenítsük meg.
    *   **Objektum szintű jogosultságok (opcionális):** Szükség esetén egy külső könyvtár (pl. `django-guardian`) vagy egy saját logika bevezetése a jövőben lehetséges.

### Funkció technológiai "buktatók" és megoldások:
*   **Névinkonzisztencia az adatbázisban:** A Django ORM és az egységes `snake_case` elnevezési konvenció alkalmazása a modell és mezőnevekben minimalizálja ezt a kockázatot. Az ORM automatikusan kezeli a táblázatneveket.
*   **Jelszóbiztonság:** A Django alapértelmezett jelszó hashelési mechanizmusát használjuk. Soha ne tároljunk jelszavakat titkosítatlan (plaintext) formában. Jelszó visszaállítása során e-mailben küldött, rövid érvényességű tokeneket alkalmazunk.
*   **Session hijack/CSRF:** A Django beépített CSRF védelme alapértelmezetten bekapcsolt, és minden formnál a `{% csrf_token %}` sabloncímke használata kötelező.
*   **Jogosultságok granularitása:** Az előre definiált három szerepkör (felhasználó, admin, sysadmin) jó kiindulási pont. A jövőbeli bővítéseknél figyelni kell az egyensúlyra a túl durva és túl finom jogosultságkezelés között.
*   **Alapértelmezett felhasználó és jogosultságok:** Az első `sysadmin` felhasználó (`createsuperuser` parancs futtatásával) létrehozása után manuálisan vagy egy init scripttel győződjünk meg róla, hogy a megfelelő jogosultságokkal rendelkezik.
*   **Docker és adatbázis persistencia:** A `docker-compose.yml` fájlban a PostgreSQL konténerhez egy `volume` konfigurációt állítunk be, hogy az adatbázis adatai tartósan megmaradjanak a konténer életciklusától függetlenül.


---
## Fejlesztési Haladás és TODO Lista

### Befejezett Feladatok:
- [x] Rendszerterv elemzése és validálása
- [x] Követelmények tisztázása (sysadmin jogosultságok, jelszó házirend, session időtartam)

### Folyamatban lévő Feladatok:
- [ ] Projekt inicializálás Django-val és Docker környezetben
- [ ] Custom User Model létrehozása
- [ ] Szerepkörök (Groups) beállítása
- [ ] Admin felület konfigurálása
- [ ] Autentikációs nézetek implementálása

### Eltérések a Tervtől:
- **Fejlesztési vs Production környezet**: A terv külön fejlesztési és production környezetet javasolt, de az egyszerűség és azonnali tesztelés érdekében ugyanazt a Docker setup-ot használjuk mindkét célra, environment variables-al különböztetve (DEBUG=True/False).
- **Jelszó házirend**: A terv konfigurálható jelszó házirendet javasolt, de egyszerűsítettük kód szintű validációra (min 8 karakter, kis/nagybetű, szám).


### Befejezett Feladatok:
- [x] Rendszerterv elemzése és validálása
- [x] Követelmények tisztázása (sysadmin jogosultságok, jelszó házirend, session időtartam)
- [x] Django projekt struktúra létrehozása
- [x] Docker környezet konfigurálása (fejlesztés = production)
- [x] Custom User Model implementálása
- [x] PostgreSQL adatbázis beállítása
- [x] Szerepkörök alapbeállítása (Groups)
- [x] Admin felület konfigurálása
- [x] Autentikációs nézetek és URL-ek beállítása
- [x] Jelszó validátor implementálása
- [x] Bootstrap alapú UI sablonok létrehozása

### Folyamatban lévő Feladatok:
- [ ] Szerepkörök és jogosultságok adatbázis inicializálása
- [ ] Első tesztelés Docker környezetben
- [ ] Sysadmin felhasználó létrehozása

### Eltérések a Tervtől:
- **Fejlesztési vs Production környezet**: A terv külön környezeteket javasolt, de az egyszerűség és azonnali tesztelés érdekében ugyanazt a Docker setup-ot használjuk mindkét célra, environment variables-al különböztetve (DEBUG=True/False).
- **Jelszó házirend**: A terv konfigurálható jelszó házirendet javasolt, de egyszerűsítettük kód szintű validációra (min 8 karakter, kis/nagybetű, szám).
- **Projekt struktúra**: A terv hagyományos Django struktúrát javasolt, de src/ mappát használtunk az alkalmazásoknak a jobb szervezettség érdekében.

### Következő Lépések:
1. Docker konténerek tesztelése és adatbázis migrációk futtatása
2. Szerepkörök és alap jogosultságok létrehozása
3. Sysadmin felhasználó létrehozása
4. Első bejelentkezés tesztelése

*Utolsó frissítés: 2025. szeptember 14.*

### Befejezett Feladatok:
- [x] Rendszerterv elemzése és validálása
- [x] Követelmények tisztázása (sysadmin jogosultságok, jelszó házirend, session időtartam)
- [x] Django projekt struktúra létrehozása
- [x] Docker környezet konfigurálása (fejlesztés = production)
- [x] Custom User Model implementálása
- [x] PostgreSQL adatbázis beállítása
- [x] Szerepkörök alapbeállítása (Groups)
- [x] Admin felület konfigurálása
- [x] Autentikációs nézetek és URL-ek beállítása
- [x] Jelszó validátor implementálása
- [x] Bootstrap alapú UI sablonok létrehozása
- [x] Adatbázis migrációk futtatása
- [x] Docker konténerek tesztelése
- [x] Sysadmin felhasználó létrehozása

### Folyamatban lévő Feladatok:
- [ ] Első bejelentkezés tesztelése

### Eltérések a Tervtől:
- **Fejlesztési vs Production környezet**: A terv külön környezeteket javasolt, de az egyszerűség és azonnali tesztelés érdekében ugyanazt a Docker setup-ot használjuk mindkét célra, environment variables-al különböztetve (DEBUG=True/False).
- **Jelszó házirend**: A terv konfigurálható jelszó házirendet javasolt, de egyszerűsítettük kód szintű validációra (min 8 karakter, kis/nagybetű, szám).
- **Projekt struktúra**: A terv hagyományos Django struktúrát javasolt, de src/ mappát használtunk az alkalmazásoknak a jobb szervezettség érdekében.

### Következő Lépések:
1. Bejelentkezés tesztelése a webes felületen (http://localhost:8000)
2. Admin felület tesztelése (/admin/)
3. Felhasználókezelés funkciók tesztelése

*Utolsó frissítés: 2025. szeptember 14.*

### Befejezett Feladatok:
- [x] Rendszerterv elemzése és validálása
- [x] Követelmények tisztázása (sysadmin jogosultságok, jelszó házirend, session időtartam)
- [x] Django projekt struktúra létrehozása
- [x] Docker környezet konfigurálása (fejlesztés = production)
- [x] Custom User Model implementálása
- [x] PostgreSQL adatbázis beállítása
- [x] Szerepkörök alapbeállítása (Groups)
- [x] Admin felület konfigurálása
- [x] Autentikációs nézetek és URL-ek beállítása
- [x] Jelszó validátor implementálása
- [x] Bootstrap alapú UI sablonok létrehozása
- [x] Szerepkörök és jogosultságok adatbázis inicializálása
- [x] Első tesztelés Docker környezetben
- [x] Sysadmin felhasználó létrehozása
- [x] Profil oldal implementálása

### Folyamatban lévő Feladatok:
- [ ] Inventory Management modul tervezése
- [ ] Inventory modellek létrehozása
- [ ] Inventory admin felület
- [ ] Inventory nézetek és URL-ek

### Eltérések a Tervtől:
- **Fejlesztési vs Production környezet**: A terv külön környezeteket javasolt, de az egyszerűség és azonnali tesztelés érdekében ugyanazt a Docker setup-ot használjuk mindkét célra, environment variables-al különböztetve (DEBUG=True/False).
- **Jelszó házirend**: A terv konfigurálható jelszó házirendet javasolt, de egyszerűsítettük kód szintű validációra (min 8 karakter, kis/nagybetű, szám).
- **Projekt struktúra**: A terv hagyományos Django struktúrát javasolt, de src/ mappát használtunk az alkalmazásoknak a jobb szervezettség érdekében.

### Következő Lépések:
1. Inventory Management modul megtervezése
2. Inventory modellek implementálása (Product, Category, Stock, Supplier)
3. Inventory admin felület konfigurálása
4. Inventory CRUD műveletek létrehozása
5. Inventory sablonok elkészítése

*Utolsó frissítés: 2025. szeptember 14.*
