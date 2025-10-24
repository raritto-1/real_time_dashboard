"""
ASGI config for real_time_dashboard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# # myproject/asgi.py
# import os
# from django.core.asgi import get_asgi_application
# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# # Initialize both apps
# django_app = get_asgi_application()
# fastapi_app = FastAPI()

# @fastapi_app.get("/api/hello")
# def say_hello():
#     return {"message": "Hello from FastAPI"}

# # Mount Django inside FastAPI
# fastapi_app.mount("/", WSGIMiddleware(django_app))


import os 
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault("DJNANGO_SETTING_MODULE",'real_time_dashboard.setting')

django_app = get_asgi_application()

fastapi_app = FastAPI()

@fastapi_app.get('/api/hello')
def say_hello(): 
    return {'message' : 'hello from fastapi '}

fastapi_app.mount("/", WSGIMiddleware(django_app))