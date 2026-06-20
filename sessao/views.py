from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from filmes.forms import FilmeForm
from sessao.models import Utilizador, Admin, Moderador


# Create your views here.

def criar_user(request, form, tipo_user):
    username = request.POST['username']
    genero_preferido = ""
    if User.objects.filter(username=username).exists():
        return render(request, 'sessao/registar.html', {
            'error_message': "Username já existe",
        })
    email = request.POST['email']
    if User.objects.filter(email=email).exists():
        return render(request, 'sessao/registar.html', {
            'error_message': "Email já está registado",
        })
    if form.is_valid():
        genero_preferido = form.cleaned_data.get("generos")
    passwd = request.POST['password']
    user = User.objects.create_user(username, email, passwd)
    if tipo_user == "U":
        u = Utilizador(user=user, genero_preferido=genero_preferido)
        u.save()
    elif tipo_user == "M":
        m = Moderador(user=user, group=Group.objects.get(name="Moderador"), genero_preferido=genero_preferido)
        user.groups.add(Group.objects.get(name="Moderador"))
        user.is_staff = True
        user.save()
        m.save()


def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(username=username, password=passwd)
        if user is not None:
            if not hasattr(user, 'utilizador') or not user.utilizador.banido:
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect(reverse('filmes:index'))
            else:
                return render(request, 'sessao/loginview.html', {
                    'error_message': "utilizador banido",
                })
        else:
            return render(request, 'sessao/loginview.html', {
                'error_message': "utilizador não existe",
            })
    else:
        return render(request, 'sessao/loginview.html')


def registar(request):
    form = FilmeForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        criar_user(request, form, "U")
        return HttpResponseRedirect(reverse('sessao:loginview'))
    else:
        return render(request, 'sessao/registar.html', context)


def criarmoderador(request):
    form = FilmeForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        criar_user(request, form, "M")
        return HttpResponseRedirect(reverse('filmes:index'))
    else:
        return render(request, 'sessao/criarmoderador.html', context)


def informacao(request):
    user = User.objects.get(username=request.session.get('username'))
    if hasattr(user, 'moderador'):
        tipo = Moderador.objects.get(user=user)
    elif hasattr(user, 'utilizador'):
        tipo = Utilizador.objects.get(user=user)
    else:
        tipo = Admin.objects.get(user=user)
    generos_preferidos = tipo.genero_preferido
    if generos_preferidos:
        generos_preferidos = eval(generos_preferidos)
    form = FilmeForm(request.POST or None, initial={'generos': generos_preferidos})

    if request.method == 'POST':
        if user.check_password(request.POST['password']):
            if len(request.POST['username']) != 0:
                username = request.POST['username']
                if User.objects.filter(username=username).exists():
                    return render(request, 'sessao/registar.html', {
                        'error_message': "Username já existe",
                        'form': form,
                        'user': user,
                    })
                request.session['username'] = username
                user.username = username
            if len(request.POST['email']) != 0:
                if User.objects.filter(email=request.POST['email']).exists():
                    return render(request, 'sessao/registar.html', {
                        'error_message': "Email já está registado",
                        'form': form,
                        'user': user,
                    })
                user.email = request.POST['email']
            if form.is_valid():
                tipo.genero_preferido = form.cleaned_data["generos"]
            else:
                tipo.genero_preferido = ""
            tipo.save()
            if len(request.POST['nova_password']) != 0:
                user.set_password(request.POST['nova_password'])
            user.save()
            return HttpResponseRedirect(reverse('sessao:informacao'))
        else:
            context = {'form': form}
            return render(request, 'sessao/informacao.html', {
                'error_message': "Digite corretamente a password atual",
            }, context)

    else:
        context = {
            'form': form,
            'user': user,
            'error_message': "Edição efetuada com sucesso",
        }
        return render(request, 'sessao/informacao.html', context)


def fazer_uploaduser(request):
    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            return render(request, 'sessao/fazer_uploaduser.html', {
                'error_message': "Selecione um ficheiro antes de dar upload",
            })
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.SESSAO_ROOT)
        if not myfile.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return render(request, 'sessao/fazer_uploaduser.html', {
                'error_message': "Dê upload de uma imagem png ou jpg",
            })
        filename = request.session.get('username') + ".jpg"
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'sessao/fazer_uploaduser.html', {
            'uploaded_file_url': uploaded_file_url
        }
                      )
    return render(request, 'sessao/fazer_uploaduser.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('sessao:loginview'))
