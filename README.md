# JERV ERP

Egy egyszerű, célzott vállalatirányítási rendszer Python/Django alapokon.

## Funkciók

- **Felhasználókezelés és Jogosultságok**: Bejelentkezés, szerepkörök (felhasználó, admin, sysadmin)
- **Raktárkezelés**: Termékek, készletek, mozgások kezelése
- **Vevőkezelés**: Ügyfelek és rendelések kezelése
- **API Integrációk**: Webshopok és külső rendszerek összekapcsolása
- **Statisztikák**: Dashboard és riportok

## Telepítés és Futtatás

### Előfeltételek
- Docker és Docker Compose
- Python 3.11+

### Fejlesztési Környezet
```bash
# Klónozás és könyvtárba lépés
cd /path/to/jerv

# Environment fájl létrehozása
cp .env.example .env
# Szerkeszd a .env fájlt a helyi beállításokkal

# Konténerek indítása
docker-compose up --build

# Migrációk futtatása (első alkalommal)
docker-compose exec web python manage.py migrate

# Szuperuser létrehozása
docker-compose exec web python manage.py createsuperuser
```

### Production Környezet
```bash
# Production profil használata
docker-compose --profile production up --build -d
```

## Projekt Struktúra

```
JERV/
├── config/                 # Django projekt konfiguráció
│   ├── settings.py        # Fő settings
│   ├── settings/
│   │   ├── development.py # Fejlesztési beállítások
│   │   └── production.py  # Production beállítások
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── src/                   # Django alkalmazások
│   ├── accounts/         # Felhasználókezelés
│   ├── core/            # Fő alkalmazás
│   └── ...              # További modulok
├── templates/            # HTML sablonok
├── requirements/         # Python függőségek
├── static/               # Statikus fájlok
├── media/                # Feltöltött fájlok
├── docker-compose.yml    # Docker konfiguráció
├── Dockerfile           # Konténer definíció
├── manage.py            # Django management script
└── .env                 # Környezeti változók
```

## API Dokumentáció

A rendszer REST API-val rendelkezik külső integrációkhoz.

## Licensz

Ez a projekt saját fejlesztés, szabadon használható.