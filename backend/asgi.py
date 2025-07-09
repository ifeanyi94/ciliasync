# One server where: Django REST API is under /api/. FastAPI prediction API is under /fastapi/ #
import django
import os
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_core.settings')
django.setup()

from django.core.wsgi import get_wsgi_application
from fastapi_core.main import app as fastapi_app

app = FastAPI()

# Mount Django under /api
app.mount("/api", WSGIMiddleware(get_wsgi_application()))

# Mount FastAPI directly
app.mount("/fastapi", fastapi_app)
