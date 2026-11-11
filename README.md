# Semana 11 - Introduccion a Django (IS093A)

## Ejecutar
```bash
python -m venv venv
venv\Scripts\activate          # Windows   (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py poblar         # agrega 50 productos nuevos de ejemplo
python manage.py check
python manage.py runserver
```
- http://127.0.0.1:8000/          -> FBV (home)
- http://127.0.0.1:8000/catalogo/ -> CBV (ListView)
- http://127.0.0.1:8000/admin/    -> Admin (opcional: python manage.py createsuperuser)

Para producción, configura `DJANGO_SECRET_KEY` con una clave secreta segura
y desactiva `DEBUG`.
