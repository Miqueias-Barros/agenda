from django.urls import path
from . import views

urlpatterns = [
    path('agenda/', views.lista_eventos),
]