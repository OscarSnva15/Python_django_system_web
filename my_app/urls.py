from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abouth/', views.abouth, name='abouth'),
    path('proyect/', views.proyect, name='proyect'),
    path('contacs/', views.contacs, name="contacs"),
    #path('contactos-dos/', views.contactos, name="contacto"),
    #path('contactos-dos/<str:nombre>', views.contactos, name="contacto"),
    #path('contactos-dos/<str:nombre>/<str:apellidos>', views.contactos, name="contacto"),
]