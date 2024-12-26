#django tiene mucho modulos, que podemos utilizar
from django.shortcuts import render
from django.http import HttpResponse

#YO PUEDO TENER UN PLANTILLA QUE PUEDE SER CONCATENADA EN CADA URL LLAMADA
layout ="""
        <h1>Sitio web con Django | Oscar Suarez Nava </h1>
        <hr>
        <ul>
            <li>
            <a href="/home">Inicio</a>
            </li>
            <li>
            <a href="/abouth/">nosotros</a>
            </li>
            <li>
            <a href="/proyects/">proyectos</a>
            </li>
        </ul>
        <hr>
"""

# Create your views here. send files html
def index(request):
    #podemos usar cualquier tipo de instruciones para devolver cualquier cosa
    html = """
        <h2>HTML</h2>
        <p>AÑOS HASTA EL 2050!</p>
        <ul>
    """
    year = 2021
    while year <= 2050:
        if year % 2 == 0:
            html += f"<li>{str(year)}</li>"
        year +=1

    html += "</ul>"


    return HttpResponse(layout+html)

def inicio(request):
    return HttpResponse(layout+"""
        <h2>HOME</h2>
        <p>Inicio home!</p>
    """)

def abouth(request):
    return HttpResponse(layout+"""
        <h2>NOSOTROS</h2>
        <p>We are an company dedicate to support of aplications web on line</p>
    """)

def proyectos(request):

    proyectos_template = """
            <h2>Proyectos Dev OscarSnva15</h2>
            <p>Hasta ahora son:</p>
            <ul>
        """
    proyectos = ['proyecto1', 'proyecto2', 'proyecto3', 'proyecto4']
    for proyecto in proyectos:
        proyectos_template += f"<li>{proyecto}</li>"

    proyectos_template += "</ul>"

    return HttpResponse(layout+"""
        <h2>PROYECTOS</h2>
        <p>We are an company dedicate to support of aplications web on line</p>
    """+ proyectos_template)
