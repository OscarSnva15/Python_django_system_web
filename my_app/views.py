#django tiene mucho modulos, que podemos utilizar
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from my_app.models import Article,Category

# Create your views here. send files html
def index(request):
    #podemos usar cualquier tipo de instruciones para devolver cualquier cosa
    # html = """
    #     <h2>HTML</h2>
    #     <p>AÑOS HASTA EL 2050!</p>
    #     <ul>
    # """
    # year = 2021
    # while year <= 2050:
    #     if year % 2 == 0:
    #         html += f"<li>{str(year)}</li>"
    #     year +=1
    # html += "</ul>"
    nombre = 'OscarSnva15'
    lenguajes = ['Python','JavaScript','C++','Java']
    year = 2024
    hasta = range(year,2051)
    #lenguajes = []

    #en lugar de generar a1ui la vista o rederizarla se hace el llamado de un template
    return render(request, 'index.html', {
        'title':'Inicio',
        'nombre':nombre,
        'mi_variable':'soy un dato que esta en la vista',
        'lenguajes':lenguajes,
        'years':hasta
        })#pasar el nombre de la template que queremos cargar

def abouth(request):
    return render(request,'abouth.html')

def proyect(request):
    return render(request,'proyect.html')

def contacs(request):
    return render(request,'contacs.html')

def create_article(request,title,content,public):
    #print(title,content,public)
    #crear un objeto de tipo articulo en la base de datos
    article = Article(
        title = title,
        content = content,
        public = public
    )
    article.save()
    
    return HttpResponse(f"article_made: {article.title} - {article.content} - {article.public} - {article.image} - {article.created_at} - {article.update_at}")

