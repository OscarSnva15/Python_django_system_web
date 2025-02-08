from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('abouth/', views.abouth, name='abouth'),
    path('proyect/', views.proyect, name='proyect'),
    path('contacs/', views.contacs, name="contacs"),
    path('show-predictions/', views.show_predictions, name="show_predictions"),
    path('edit_article/<int:id>', views.edit_article, name="edit_article"),
    path('show_predictions/', views.show_predictions, name="show_article"), 
    path('delete_article/<int:id>', views.delete_article, name="delete_article"),
    path('save-article/', views.save_article, name="save"),
    path('create_article/', views.create_article, name="create"),
]