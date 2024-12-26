from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.inicio, name='inicio'),
    path('abouth/', views.abouth, name='nosotroa'),
    path('proyects/', views.proyectos, name="proyectos"),
]