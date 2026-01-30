from django.urls import path
from core import views

urlpatterns = [
    path('agenda/', views.lista_eventos)
]