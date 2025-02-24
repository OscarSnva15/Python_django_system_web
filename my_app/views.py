#django tiene mucho modulos, que podemos utilizar
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from my_app.models import Article,Category
from django.db.models import Q
#import librerias para sistema recomendader
from .dataclasses import Collector
import pandas as pd
import os
import json
import numpy as np
from collections import Counter

# Create your views here. send files html
def index(request):
    nombre_autor = 'Oscar Suarez Nava'
    nombre_coautor = 'Heriberto Casarrubias Vargas'

    #en lugar de generar a1ui la vista o rederizarla se hace el llamado de un template
    return render(request, 'index.html', {
        'title':'Recommender Bussines System',
        'nombre_autor':nombre_autor,
        'nombre_coautor':nombre_coautor
        })#pasar el nombre de la template que queremos cargar

def abouth(request):
    return render(request,'abouth.html')

def recomender(request):
    return render(request,'recomender.html')

def contacs(request):
    return render(request,'contacs.html')

def predict(request,title,content,public):
    #print(title,content,public)
    #crear un objeto de tipo articulo en la base de datos
    article = Article(
        title = title,
        content = content,
        public = public
    )
    article.save()
    
    return HttpResponse(f"article_made: {article.title} - {article.content} - {article.public} - {article.image} - {article.created_at} - {article.update_at}")

def save_article(request):
    if request.method == 'GET':
        # diccionario de coordenadas
        coords = request.GET['coordenadas']
        json_coords = json.loads(coords)

        path = os.path.join(os.path.dirname(__file__), 'data', 'crecimientoNicolasRomero.csv')
        df = pd.read_csv(path)
        # coordinates_point_get
        time_window = 3
        point_interest = Collector(df, json_coords, time_window)
        point_interest.find_business_into_radius()
        vdlc = point_interest.report_accumulated_business_support()
        #print(vdlc)
        #llamamos al kkn
        X_train = np.array([
            [3.1, 4, 7.6, 2.8, 2.6, 1.4, 4.3, 2, 1.8, 1.8, 2.1, 3.1, 1.8, 1.5, 1.2, 1.4, 0, 1.6, 1.6, 1.3, 1.4, 0, 0.9, 0, 0.9, 0, 0, 0, 0.9, 0], 
            [1.7, 3, 22.2, 5.1, 6.9, 1, 10.6, 1.6, 1.5, 1.4, 2.7, 6.5, 1.1, 1.8, 0, 2.9, 0, 2.7, 2.5, 1.2, 1.8, 0, 0, 0, 1.8, 0, 0, 0, 2.3, 0], 
            [3.1, 4.2, 1.5, 1.5, 1.6, 1.8, 1.3, 1.6, 1.6, 1.5, 1.7, 1.2, 1.3, 1.5, 1.1, 1, 1.5, 1.4, 1, 1.1, 1, 1, 0.9, 0, 0, 0.9, 1.2, 0, 0, 0], 
            [2.9, 3.2, 1.8, 1.3, 1.3, 1, 1.4, 1.2, 1.2, 1.2, 1.2, 1.4, 1.2, 0.9, 1, 0.9, 0.9, 1, 0.9, 0.9, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1.3, 0.9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [3.6, 5.1, 2.3, 2, 1.7, 1.8, 1.9, 1.8, 1.9, 1.8, 2, 1.8, 1.8, 1.9, 1.3, 1.2, 1.2, 1.6, 1.1, 1.7, 1.4, 0, 1, 0, 0.9, 0, 0.9, 0, 0, 0], 
            [1.4, 2.8, 5.2, 1.8, 1.6, 1.1, 2.4, 1.1, 1, 1.3, 1.7, 1.7, 1.3, 1.2, 0, 0, 0, 1, 1, 0, 1.2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [4.2, 7.9, 19.4, 5.6, 5.3, 2.1, 9.2, 3.4, 3, 3.6, 4.1, 5.8, 3.7, 3.1, 1.8, 2.6, 1.1, 2.9, 2.8, 2.1, 3.6, 0, 1.4, 1, 2.1, 1.2, 0, 0, 2.4, 0], 
            [2.3, 4, 2.1, 1.2, 1.5, 1.3, 1.5, 1.3, 1, 1.2, 1.6, 1.6, 1.5, 1.2, 0.9, 0, 0, 1.3, 1.2, 1.2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [3.6, 4.4, 1.9, 1.5, 1.7, 1.5, 1.4, 1.5, 1.6, 1.5, 1.7, 1.4, 1.3, 1.3, 1.2, 1.2, 1.5, 1.1, 1.1, 1.3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [2.6, 3.9, 2.7, 1.5, 1.6, 1.5, 1.7, 1.3, 1.4, 1.6, 2.1, 1.6, 1.8, 1.5, 1.1, 0, 0, 1.5, 1, 1.4, 1.3, 0, 1, 0, 0, 0, 0, 0, 0, 0], 
            [5.6, 7.7, 16.1, 5.6, 5.6, 2.6, 9, 3.9, 3.5, 3.8, 3.7, 6, 3.3, 2.9, 1.9, 3.1, 1.5, 2.8, 2.7, 2.3, 3.3, 1, 1.9, 1.1, 2, 1.2, 0, 0, 2.2, 0], 
            [3.2, 6.2, 6.9, 2.7, 2, 1.7, 2.4, 1.9, 1.5, 2.5, 3.1, 2.4, 2.7, 2.1, 1.4, 1, 0, 1.9, 1.6, 1.9, 2.7, 0, 1.1, 0, 1.3, 0, 0, 0, 1.1, 0], 
            [2.5, 4.7, 5.2, 2.1, 2.3, 1.6, 3.1, 1.6, 1.5, 1.4, 2.1, 2.4, 1.7, 1.8, 1, 0.9, 1.2, 1.8, 1.3, 1.4, 1.4, 0.9, 0.9, 0, 1, 0, 1.1, 0, 0, 0], 
            [3.1, 5.8, 7.2, 2.9, 2.2, 1.7, 3.6, 2.1, 2, 2.1, 2.5, 3.1, 2.4, 1.9, 1.2, 1.2, 0, 1.6, 1.6, 1.6, 2.1, 0, 1.2, 0, 1.1, 0, 0, 0, 1, 0], 
            [4.8, 6.8, 2.2, 2.3, 2.1, 2.4, 1.9, 2.2, 2, 1.8, 2.7, 2, 2.3, 2.1, 1.4, 1.5, 1.9, 2.1, 1.5, 1.9, 1.7, 1.1, 1.5, 0, 1, 0.9, 1.4, 1, 0, 1], 
            [3, 4.2, 1.6, 1.4, 1.4, 1.4, 1.1, 1.3, 1.2, 1.5, 1.9, 1.3, 1.5, 1.7, 1.1, 0, 1.5, 1.5, 1.3, 1.3, 1.2, 0, 1.3, 0, 0, 0, 1.2, 0, 0, 0.9], 
            [6.1, 6.2, 2.5, 2.7, 2.5, 2.6, 2.4, 2.7, 2.7, 2.7, 2.3, 2.1, 2.4, 2.1, 2, 2, 2.1, 1.9, 1.8, 1.8, 1.5, 1.5, 1.4, 1.1, 1.2, 1.1, 0.9, 1, 0, 0], 
            [1.1, 2.3, 6.8, 1.8, 2, 0, 3, 1.3, 0.9, 1.2, 1.5, 2.1, 1.1, 1.5, 0, 0, 0, 1, 0.9, 0, 1.3, 0, 0, 0, 0, 0, 0, 0, 0.9, 0], 
            [6.8, 7.5, 5.5, 3.5, 3.4, 2.8, 3.9, 3.6, 3, 2.6, 2.5, 3, 2.9, 2.3, 2, 2.3, 1.8, 2.3, 2.3, 2.4, 2, 1.3, 1.5, 1.3, 1.7, 1.1, 0, 1.1, 1.1, 0], 
            [6.3, 8.8, 9.6, 4.4, 3.9, 3.1, 5.3, 3.7, 3.3, 3.6, 4.2, 4.2, 3.4, 3.2, 2.2, 2.5, 2, 3, 2.5, 2.5, 3.3, 1.1, 1.7, 1.2, 1.9, 1.1, 1.1, 1, 1.5, 0], 
            [3.9, 7.3, 8.2, 3.3, 2.7, 2.1, 3.9, 2.3, 2.2, 2.5, 2.9, 3, 2.5, 2.1, 1.6, 1.8, 1.4, 2.3, 1.7, 1.8, 3, 0, 1.1, 0, 1.5, 0, 1.2, 0, 1.2, 0], 
            [2.7, 4.8, 10.3, 3.3, 3.5, 1.5, 5.2, 2.1, 1.9, 2.2, 2.5, 3.8, 2, 1.9, 1.1, 1.6, 0, 1.8, 1.8, 1.4, 1.8, 0, 1.1, 0, 1.4, 0, 0, 0, 1.4, 0], 
            [4.9, 6.2, 4.6, 2.8, 2.6, 2.2, 3.3, 2.6, 2.6, 2.5, 2.8, 2.7, 2.3, 2.4, 1.8, 1.5, 1.3, 1.8, 2.1, 1.9, 2, 0.9, 1.4, 0, 1.2, 1.1, 1.1, 0, 1.1, 0], 
            [2.8, 3.2, 1.1, 1.4, 1.4, 1.5, 1.5, 1.3, 1.5, 1.2, 1.6, 1.4, 1, 1.4, 1, 1, 1.1, 1.1, 1, 1.1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
            [5.5, 9.1, 18.9, 6.2, 6.7, 2.9, 10.3, 4.7, 3.8, 4.1, 4.4, 7.2, 4, 3.6, 2, 3.2, 1.6, 3.4, 3.3, 3.3, 4, 1.2, 2.3, 1.2, 2.4, 1.4, 0, 0, 2.5, 0], 
            [5.8, 9.5, 7.4, 3.7, 3.2, 3.5, 3.3, 3.3, 3, 3.7, 3.7, 2.8, 4.1, 3.6, 2.5, 2.1, 1.7, 2.8, 2.6, 2.2, 2.8, 1.4, 1.5, 1.3, 1.7, 1.6, 1.6, 0.9, 1.5, 1], 
            [6.8, 9.2, 7, 4.1, 4.1, 3.2, 4.3, 4.2, 3.2, 3.6, 3.4, 3.2, 3.1, 2.8, 2.2, 2.4, 2.1, 2.6, 2.2, 2.7, 3, 1.4, 1.8, 1.4, 2, 1.4, 1.2, 1.3, 1.3, 1], 
            [1.9, 4.1, 10, 2.5, 2.3, 1.2, 3.5, 1.3, 1.2, 1.6, 3.5, 2.8, 2.6, 2.9, 1, 1.1, 0, 2.5, 1.6, 1.3, 2.6, 0, 0, 0, 0, 0, 0.9, 0, 1.2, 0], 
            [5.9, 9.3, 7.9, 3.9, 4.1, 3.3, 5.2, 3.4, 2.9, 3.3, 3.3, 3.8, 2.9, 2.7, 2.1, 2.1, 2.5, 3, 2.7, 2.7, 2.7, 1.3, 1.6, 1.3, 1.7, 1, 2, 1.2, 1.2, 1.2], 
            [4.5, 8.9, 13.8, 4.8, 4.9, 2.7, 7.9, 3.9, 2.9, 3.9, 3.7, 5.1, 2.9, 2.7, 1.8, 2.3, 1.7, 3.1, 2.8, 2.3, 3.2, 0.9, 1.9, 0, 2.2, 1.2, 0.9, 0, 1.9, 0], 
            [2.6, 3.6, 3.8, 2.4, 1.8, 1.6, 2.4, 1.4, 1.8, 1.8, 1.8, 2.2, 1.7, 2.2, 1.3, 1.3, 0, 1.3, 1.1, 1.2, 1.3, 0, 0, 0, 0.9, 0, 0, 0, 0, 0], 
            [3.2, 4.8, 3.2, 1.9, 1.9, 1.8, 2.4, 1.8, 1.6, 1.7, 2.6, 1.8, 1.3, 1.5, 1, 1.1, 2.2, 1.7, 1.3, 1.3, 1.5, 0, 1.1, 0, 0, 0.9, 2.3, 0, 0, 1.3], 
            [2.1, 4.1, 2.3, 1.8, 1.4, 1.5, 1.5, 1.1, 1.2, 1.4, 1.7, 1.3, 1.4, 1.3, 1, 0, 0.9, 1.1, 0.9, 1.1, 1.2, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [5.9, 6.4, 3.4, 2.7, 2.3, 2.4, 2.9, 2.7, 2.8, 2.2, 2.2, 2, 2.4, 1.9, 1.9, 2, 1.8, 1.9, 1.4, 1.4, 1.5, 1.3, 1.4, 1, 0.9, 1.2, 0, 1, 1, 0.9], 
            [5.5, 7.5, 6.9, 3.9, 3.2, 3, 4.4, 3.3, 3, 3.1, 3, 3.3, 2.4, 2.6, 1.9, 2.2, 1.7, 2.2, 1.9, 1.6, 2, 1.1, 1.3, 1.2, 1.6, 1.5, 1.3, 0, 1.2, 0], 
            [6.8, 14, 11.3, 4.7, 4.5, 4.2, 5.4, 3.9, 3.1, 4.3, 5.6, 4.6, 4.3, 4.2, 2.8, 2.2, 3, 4.4, 3.2, 3.6, 5.3, 1.6, 2.2, 1.3, 2.5, 1.2, 3.5, 1.5, 1.7, 1.5], 
            [5.6, 9.2, 11.7, 4.1, 4, 2.6, 4.9, 3.4, 2.6, 3.6, 4.6, 4.3, 3.9, 3.3, 2.2, 2.2, 1.7, 3, 2.5, 2.7, 4.1, 0, 1.7, 1.2, 2.1, 0, 1.4, 0.9, 1.6, 0.9], 
            [5.3, 7.8, 2.2, 2.4, 2.6, 2.8, 2.5, 2.7, 2.4, 2.3, 3.1, 2.5, 2.5, 2, 1.9, 1.4, 2.3, 2.6, 2, 2.4, 2, 1.3, 1.5, 1.1, 1.3, 1.2, 2, 1.2, 0, 1.2], 
            [8.3, 13.3, 27, 8.5, 8.7, 4.2, 13.8, 6.2, 5.4, 5.9, 6.4, 8.9, 5.4, 4.7, 2.8, 4.4, 2.3, 4.8, 4.7, 3.7, 5.4, 1.4, 2.8, 1.4, 3.6, 1.5, 0.9, 1.4, 3.4, 0], 
            [6.4, 8.7, 7.9, 3.8, 3.3, 2.3, 4, 3.3, 2.6, 3.6, 3.4, 3.5, 3, 2.2, 2.1, 1.8, 1.3, 2.9, 2.7, 2.1, 2.7, 1.1, 1.6, 0.9, 1.6, 0, 0.9, 0, 1.4, 0], 
            [5.6, 10, 8.4, 3.3, 3.8, 3, 3.9, 3, 2.4, 3.3, 4.1, 3.7, 3, 2.6, 2, 1.7, 2.6, 3, 2.6, 2.9, 4, 1.2, 1.5, 1, 1.8, 0, 2.8, 1, 1.3, 1.4], 
            [2.4, 4.9, 9.4, 3.1, 2.7, 1, 4.8, 1.4, 1.8, 1.9, 2, 2.8, 1.4, 1.1, 0, 1.2, 0, 1.8, 1.5, 1.2, 2.2, 0, 1, 0, 1.1, 0, 0, 0, 1.4, 0], 
            [6.3, 9.6, 8.5, 3.9, 3.8, 3.3, 4.3, 3.8, 3.1, 3.7, 4.3, 3.4, 3.7, 3.1, 2.4, 2.1, 2.2, 3.1, 2.3, 2.9, 3.5, 1.1, 1.9, 1.2, 2, 1.1, 1.3, 1.1, 1.3, 0.9], 
            [10.7, 11.4, 7.4, 5, 5.6, 4.5, 5.3, 5.3, 4.6, 4.3, 3.9, 4.2, 4.3, 3.7, 3.6, 3.1, 3.5, 3.7, 3, 3.3, 3.1, 2.4, 2.5, 1.7, 2.1, 2, 1.4, 1.9, 1.6, 1.6], 
            [8.5, 18.3, 46.2, 13.1, 13.6, 5.1, 24.1, 8.6, 6.5, 8.2, 8.3, 14.5, 6.9, 5.9, 3.3, 5.8, 2.5, 6.4, 7.1, 4.7, 8, 1.4, 4.3, 1.6, 5.3, 2.2, 0, 1.2, 6.1, 0], 
            [2.2, 6.7, 18.4, 4.8, 4.4, 1.7, 9.1, 2.7, 2.1, 3.2, 2.9, 5.6, 2.6, 2.1, 1.3, 2.1, 1, 2.4, 2.5, 1.5, 3.6, 0, 1.6, 0, 1.9, 0, 0, 0, 2.1, 0], 
            [5.6, 5.9, 2.4, 2.5, 2.6, 2.6, 1.8, 2.2, 2.4, 2.3, 2.3, 1.8, 2.5, 1.7, 1.7, 1.4, 1.4, 1.4, 1.8, 1.6, 1.9, 1.1, 1.6, 0, 1.3, 0.9, 0, 0, 0.9, 0], 
            [10.4, 12.8, 6.2, 4.7, 4.3, 4.7, 4.4, 5.1, 4.4, 4.4, 5.2, 3.7, 4.5, 3.5, 3.2, 3.1, 3.3, 3.9, 3.2, 3.5, 3.2, 2.1, 2.8, 1.6, 2.3, 1.8, 2.1, 1.9, 1.4, 1.7], 
            [8.4, 13, 5.1, 4.5, 4.8, 4.7, 3.2, 4.4, 3.8, 4.1, 4.9, 4, 3.6, 3.9, 3, 2.6, 3.5, 4.1, 3.3, 4.5, 3.6, 1.8, 2.4, 2.5, 2, 1.7, 2.5, 1.6, 1.6, 1.6], 
            [1.4, 2.2, 0, 0, 0, 0, 0, 1, 0, 0, 1.2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 
            [16.5, 16.5, 10.7, 7.7, 6.8, 6.5, 7.1, 6.7, 6.6, 7.2, 6.4, 6.4, 6.2, 5.4, 5, 4.9, 4.1, 4.3, 5.6, 4.9, 4.9, 2.9, 3.1, 3.1, 2.7, 2.1, 2.2, 2.8, 2.6, 2.3], 
            [6.8, 10.6, 15.1, 5.7, 5.3, 3.5, 9.1, 4.5, 3.6, 4.3, 4.2, 5.6, 3.9, 2.9, 2.4, 2.7, 2.2, 3.8, 3.8, 2.7, 3.8, 1.3, 2.4, 1.5, 2.4, 1.4, 1.4, 0.9, 2.1, 1.1], 
            [6.3, 7.9, 3.3, 2.9, 3.1, 3.8, 2.5, 2.8, 2.6, 2.9, 3.3, 2.2, 2.8, 2.2, 1.9, 2.1, 2.8, 2.4, 2.2, 2.4, 2.4, 1.3, 1.4, 1.1, 1.5, 1.2, 2.3, 1.3, 0, 1.3], 
            [4.5, 9.2, 15.1, 4.4, 4.5, 2.5, 6.4, 3.1, 2.5, 3.6, 4.8, 4.7, 3.3, 3.2, 1.7, 2.1, 1.4, 3.2, 2.7, 2.5, 3.9, 0, 1.4, 0.9, 2.1, 0.9, 1.9, 1, 1.8, 0], 
            [3.7, 6.4, 3.5, 2.3, 2, 2.1, 2.4, 2.2, 2.1, 2.3, 2.3, 1.7, 2.8, 1.6, 1.5, 1.4, 1.2, 1.6, 1.5, 1.8, 1.8, 0, 2.1, 0, 1.3, 0, 0, 0, 0.9, 0], 
            [6.3, 13.8, 14.3, 5.1, 4.2, 4.1, 4.2, 3.7, 2.8, 5.1, 6.2, 4.5, 5.4, 4.5, 3.4, 2.1, 1.7, 4.2, 3.7, 3.4, 5.7, 1.3, 1.9, 1.1, 2.3, 1.3, 2.7, 1.3, 2, 1], 
            [5.7, 13.9, 28.3, 8.1, 7.6, 3.4, 12.5, 5.1, 3.9, 5.6, 7.2, 8.5, 5.6, 4.7, 2.8, 3.3, 1.1, 5.6, 4.6, 3.6, 6.2, 1.3, 2.6, 1.2, 3.1, 1.7, 1.2, 0.9, 3.9, 0], 
            [14.4, 21.9, 24.1, 9.6, 9.9, 7.2, 13.3, 8.4, 6.9, 8.1, 7.8, 8.8, 7.6, 5.5, 4.6, 5.6, 4.6, 6.4, 6.9, 5.5, 7.2, 2.7, 4.4, 2.7, 4.7, 2.8, 2.4, 2.8, 3.8, 2], 
            [10.3, 10.7, 4.9, 4.4, 3.8, 4.1, 4.1, 4.7, 4.6, 4.4, 4.8, 3, 3.4, 3.7, 3.7, 3.1, 3.8, 3.8, 2.5, 3, 2.7, 2.4, 2.3, 2, 1.9, 2.2, 2.8, 1.7, 1.3, 2.3], 
            [16.2, 17, 7, 6.1, 6.5, 7, 5.4, 6, 5.9, 6.3, 6.4, 5.2, 6.7, 5.6, 5, 4.8, 5.3, 5.1, 4, 4.7, 4.8, 3, 3.2, 2.8, 3.2, 1.9, 3.2, 3.3, 2, 2.6]
        ])
        y_train = np.array([461150, 463310, 811191, 611111, 611122, 467114, 722511, 465111, 713943, 321910, 812210, 461140, 621111, 466312, 461170, 811112, 811192, 312112, 466212, 611112, 811430, 811499, 465211, 462112, 434211, 463113, 466111, 461213, 522110, 811410, 464113, 434112, 811119, 722412, 434311, 464112, 467113, 541920, 811211, 463215, 931610, 323119, 541110, 541941, 337120, 463213, 812410, 311520, 811492, 813230, 468112, 611132, 811219, 811420, 722512, 311910, 621511, 464121, 465914, 468420, 532282])
        array_vdlc = [x for x in vdlc if isinstance(x, int)]
        
        X_test = np.array([
            array_vdlc
        ])
        negocios = {
                    461150: "Comercio al por menor de leche, otros productos lácteos y embutidos",
                    811191: "Reparación menor de llantas",
                    463310: "Comercio al por menor de calzado",
                    722511: "Restaurantes con servicio de preparación de alimentos a la carta o de comida corrida",
                    713943: "Centros de acondicionamiento físico del sector privado",
                    321910: "Fabricación de productos de madera para la construcción",
                    465111: "Comercio al por menor de artículos de perfumería y cosméticos",
                    467114: "Comercio al por menor de vidrios y espejos",
                    611111: "Escuelas de educación preescolar del sector privado",
                    466312: "Comercio al por menor de plantas y flores naturales",
                    812210: "Lavanderías y tintorerías",
                    621111: "Consultorios de medicina general del sector privado",
                    461140: "Comercio al por menor de semillas y granos alimenticios, especias y chiles secos",
                    811192: "Lavado y lubricado de automóviles y camiones",
                    461170: "Comercio al por menor de paletas de hielo y helados",
                    811112: "Reparación del sistema eléctrico de automóviles y camiones",
                    312112: "Purificación y embotellado de agua",
                    811499: "Reparación y mantenimiento de otros artículos para el hogar y personales",
                    465211: "Comercio al por menor de discos y casetes",
                    611122: "Escuelas de educación primaria del sector público",
                    466212: "Comercio al por menor de teléfonos y otros aparatos de comunicación",
                    811430: "Reparación de calzado y otros artículos de piel y cuero",
                    461213: "Comercio al por menor de bebidas no alcohólicas y hielo",
                    462112: "Comercio al por menor en minisupers",
                    811410: "Reparación y mantenimiento de aparatos eléctricos para el hogar y personales",
                    464113: "Comercio al por menor de productos naturistas, medicamentos homeopáticos y de complementos alimenticios",
                    722412: "Bares, cantinas y similares",
                    434211: "Comercio al por mayor de cemento, tabique y grava",
                    466111: "Comercio al por menor de muebles para el hogar",
                    611112: "Escuelas de educación preescolar del sector público",
                    434311: "Comercio al por mayor de desechos metálicos",
                    463113: "Comercio al por menor de artículos de mercería y bonetería",
                    434112: "Comercio al por mayor de medicamentos veterinarios y alimentos para animales, excepto mascotas",
                    464112: "Farmacias con minisúper",
                    811119: "Otras reparaciones mecánicas de automóviles y camiones",
                    463215: "Comercio al por menor de bisutería y accesorios de vestir",
                    811211: "Reparación y mantenimiento de equipo electrónico de uso doméstico",
                    541920: "Servicios de fotografía y videograbación",
                    931610: "Actividades administrativas de instituciones de bienestar social",
                    541110: "Bufetes jurídicos",
                    323119: "Impresión de formas continuas y otros impresos",
                    467113: "Comercio al por menor de pintura",
                    813230: "Asociaciones y organizaciones civiles",
                    337120: "Fabricación de muebles, excepto cocinas integrales, muebles modulares de baño y muebles de oficina y estantería",
                    812410: "Estacionamientos y pensiones para vehículos automotores",
                    811492: "Reparación y mantenimiento de motocicletas",
                    463213: "Comercio al por menor de lencería",
                    811219: "Reparación y mantenimiento de otro equipo electrónico y de equipo de precisión",
                    468112: "Comercio al por menor de automóviles y camionetas usados",
                    541941: "Servicios veterinarios para mascotas prestados por el sector privado",
                    811420: "Reparación de tapicería de muebles para el hogar",
                    522110: "Banca múltiple",
                    311520: "Elaboración de helados y paletas",
                    311910: "Elaboración de botanas",
                    722512: "Restaurantes con servicio de preparación de pescados y mariscos",
                    532282: "Alquiler de mesas, sillas, vajillas y similares.",
                    611132:	"Escuelas de educación secundaria general del sector público",
                    621511:	"Laboratorios médicos y de diagnóstico del sector privado",
                    464121:	"Comercio al por menor de lentes",
                    465914:	"Comercio al por menor de artículos desechables",
                    468420:	"Comercio al por menor de aceites y grasas lubricantes, aditivos y similares para vehículos de motor"
                }
        name_classification = knn_predict(X_train, y_train, X_test, k=3, task='classification')
        print(negocios[name_classification[0]])
        
        return render(request,'recomender.html',{'name_classification':negocios[name_classification[0]],'code_class':name_classification[0]})
    else:
        return render(request,'recomender.html')

def knn_predict(X_train, y_train, X_test, k=3, task='classification'):
    """
    Algoritmo K-NN para predecir etiquetas de un conjunto de prueba.

    Parameters:
    - X_train: np.array, conjunto de datos de entrenamiento.
    - y_train: np.array, etiquetas del conjunto de entrenamiento.
    - X_test: np.array, conjunto de datos de prueba.
    - k: int, número de vecinos más cercanos a considerar.
    - task: str, 'classification' para clasificación o 'regression' para regresión.

    Returns:
    - predictions: np.array, etiquetas predichas para X_test.
    """
    predictions = []

    # Iterar sobre cada punto de prueba
    for x_test in X_test:
        # Calcular la distancia euclidiana entre x_test y todos los puntos de entrenamiento
        distances = np.sqrt(np.sum((X_train - x_test) ** 2, axis=1))

        # Obtener los índices de los k vecinos más cercanos
        nearest_neighbors_indices = np.argsort(distances)[:k]

        # Extraer las etiquetas correspondientes a los k vecinos más cercanos
        nearest_neighbors_labels = y_train[nearest_neighbors_indices]

        if task == 'classification':
            # Clasificación: elegir la etiqueta más común
            prediction = Counter(nearest_neighbors_labels).most_common(1)[0][0]
        elif task == 'regression':
            # Regresión: calcular el promedio de las etiquetas de los vecinos
            prediction = np.mean(nearest_neighbors_labels)
        else:
            raise ValueError("La tarea debe ser 'classification' o 'regression'")

        predictions.append(prediction)

    return np.array(predictions)

def create_article(request):
    return render(request,'create_article.html')

def view_article(request):
    try:
        article = Article.objects.get(title="Superman", public=True)
        return HttpResponse(f"Articulo: {article.id}{article.title}{article.title}")
    except:
        return HttpResponse("Articulo no encontrado")

def edit_article(request,id):
    article = Article.objects.get(pk=id)
    article.title = "Robin"
    article.content = "Robin es amigo de Batman"
    article.public = True
    article.save()
    return HttpResponse(f"Articulo editado: {article.title} - {article.content}")

def show_predict(request):
    #article = Article.objects.all()
    #article = Article.objects.order_by('id')
    #article = Article.objects.order_by('title')
    #article = Article.objects.order_by('-id')
    #article = Article.objects.order_by('-title') #aplica el ordenamiento de manera descendente
    #article = Article.objects.order_by('-id')[:1] #plica limit a mi consulta
    #article = Article.objects.filter(title = 'Superman', id=8) #aplica un filtro a mi consulta
    #article = Article.objects.filter(title__exact='superman') #aplica un filtro a mi consulta
    #article = Article.objects.filter(id__lt=12) #aplica un filtro de id, menores a 12
    #article = Article.objects.filter(id__lte=10) #aplica un filtro de id, menores a 10 o igual a 10
    #article = Article.objects.filter(id__lte=10, title__contains="2") #aplica un filtro de id, mayores a 10 y que contenga el numero 2 en el titulo
    #article = Article.objects.filter(title = 'Article').exclude(public = False) #metodo que exluya el public a true
    
    #article = Article.objects.raw("SELECT * FROM my_app_article WHERE public=1") #consulta sql
    
    article = Article.objects.filter(
        Q(title__contains="2") | Q(title__contains="3") ) #aplica un filtro de id, menores a 12
    return render(request,'show_predict.html',{'articles':article})

def delete_article(request,id):
    article = Article.objects.get(pk=id)
    article.delete()
    return redirect('show_article')#redireccionar a la vista show_article