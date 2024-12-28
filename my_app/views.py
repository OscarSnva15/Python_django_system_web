#django tiene mucho modulos, que podemos utilizar
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

#YO PUEDO TENER UN PLANTILLA QUE PUEDE SER CONCATENADA EN CADA URL LLAMADA
# def new_func():
#     layout ="""
#         <h1>Sitio web con Django | Oscar Suarez Nava </h1>
#         <hr>
#         <ul>
#             <li>
#             <a href="/home">Inicio</a>
#             </li>
#             <li>
#             <a href="/abouth/">nosotros</a>
#             </li>
#             <li>
#             <a href="/proyectos/0">proyectos</a>
#             </li>
#             <li>
#             <a href="/contactos-dos/">contactos</a>
#             </li>
#         </ul>
#         <hr>
# """
#    
layout = """ layput sin sentido"""

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

    #en lugar de generar aui la vista o rederizarla se hace el llamado de un template
    return render(request, 'index.html')#pasar el nombre de la template que queremos cargar

def inicio(request):
    return render(request,'inicio.html')

def abouth(request):
    return HttpResponse(layout+"""
        <h2>NOSOTROS</h2>
        <p>We are an company dedicate to support of aplications web on line</p>
    """)

def pagina(request, redirigir=0):

    if redirigir == 1:
        return redirect('contacto', nombre= 'oscar', apellidos= 'suarez')

    proyectos_template = """
            <h2>Proyectos Dev OscarSnva15</h2>
            <p>Hasta ahora son:</p>
            <ul>
        """
    proyectos = ['proyecto1', 'proyecto2', 'proyecto3', 'proyecto4']
    for proyecto in proyectos:
        proyectos_template += f"<li>{proyecto}</li>"

    proyectos_template += "</ul>"

    return render(request, 'pagina.html')

def contactos(request, nombre="", apellidos=""):
    if nombre and apellidos:
        html = f"<p>El nombre completo es: {nombre} {apellidos}</p>"
    else:
        html = f"<p>No se ingreso nungun nombre: {apellidos}</p>"

    return HttpResponse(layout+html)