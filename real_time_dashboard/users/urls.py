from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.log_out, name='log_out'),
]