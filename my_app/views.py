#django tiene mucho modulos, que podemos utilizar
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from my_app.models import Article,Category
from django.db.models import Q

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

def proyect(request):
    return render(request,'proyect.html')

def contacs(request):
    return render(request,'contacs.html')

def create_article_(request,title,content,public):
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
        numero = request.GET['numero']
        
        return HttpResponse(f"<h2>Numero recibido: {numero} para enviar menssaje de whatsapp mediante la conexión al web service whatsapp</h2><a href='http://wa.me/{numero}'>Enviar mensaje</a>")
    else:
        return HttpResponse("<h2>No se ha podido guardar el articulo</h2>")
    
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

def show_article(request):
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
    return render(request,'articles.html',{'articles':article})

def delete_article(request,id):
    article = Article.objects.get(pk=id)
    article.delete()
    return redirect('show_article')#redireccionar a la vista show_article