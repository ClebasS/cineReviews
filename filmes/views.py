import os
from datetime import datetime

from _decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from sessao.models import Admin, Utilizador, Moderador
from .forms import FilmeForm
from .models import Filme, Comentario, Seguidor, Notificacao


# Create your views here.
def fazeravaliacao(filme):
    comentarios = Comentario.objects.filter(filme_id=filme)
    num_comentarios = comentarios.count()
    total_avaliacao = sum([c.avaliacao for c in comentarios])
    if num_comentarios > 0:
        avaliacao_media = Decimal(total_avaliacao) / Decimal(num_comentarios)
    else:
        avaliacao_media = 0.0
    filme.avaliacao_media = avaliacao_media
    filme.save()


def mandarnotificacao(user, comentario):
    seguidores = Seguidor.objects.filter(seguido=user)
    for seguidor in seguidores:
        n = Notificacao(destinatario=seguidor.seguidor, remetente=seguidor.seguido, comentario=comentario)
        n.save()


def hasphoto(user):
    filename = f"{user.username}.jpg"
    path = os.path.join("filmes/static/sessao/", filename)
    return os.path.exists(path)


def index(request):
    filmes = Filme.objects.order_by('-data_lancamento')[:5]
    if request.session.get('username'):
        user = User.objects.get(username=request.session.get('username'))
        has_photo = hasphoto(user)
        request.session['has_photo'] = has_photo
        notificacoes_count = Notificacao.objects.filter(destinatario=user, visto=False).count()
        if notificacoes_count > 0:
            request.session['notificacoes_count'] = notificacoes_count
    return render(request, 'filmes/index.html', {'filmes': filmes})


def lista(request):
    form = FilmeForm(request.POST or None)
    filmes = Filme.objects.order_by('-data_lancamento')

    if request.method == "POST":
        titulo = request.POST['titulo_filme']
        diretor = request.POST['diretor_filme']
        ator = request.POST['ator_filme']
        if titulo:
            filmes = filmes.filter(titulo__icontains=titulo)
        if diretor:
            filmes = filmes.filter(diretor__icontains=diretor)
        if ator:
            filmes = filmes.filter(elenco__icontains=ator)
        if form.is_valid():
            generos = form.cleaned_data.get("generos")
            for genero in generos:
                filmes = filmes.filter(genero__icontains=genero)
        context = {
            'form': form,
            'filmes': filmes,
        }
        return render(request, 'filmes/lista.html',
                    context)

    else:
        context = {
            'form': form,
            'filmes': filmes,
        }
        return render(request, 'filmes/lista.html',
                     context)


@permission_required('filmes.add_filme', login_url=reverse_lazy('sessao:loginview'))
def adicionarfilme(request):
    form = FilmeForm(request.POST or None)
    context = {'form': form}

    if request.method == 'POST':
        titulo = request.POST['titulo']
        if Filme.objects.filter(titulo=titulo).exists():
            return render(request, 'filmes/adicionarfilme.html', {
                'error_message': "Título do filme já existe",
                'form': form,
            })
        generos = ""
        if form.is_valid():
            generos = form.cleaned_data.get("generos")
        sinopse = request.POST['descricao']
        diretor = request.POST['diretor']
        elenco = request.POST['elenco']
        avaliacao_imdb = request.POST['imdb']
        data_lancamento = request.POST['data_lancamento']
        data = datetime.strptime(data_lancamento, '%Y-%m-%d').date()
        f = Filme(titulo=titulo, genero=generos, descricao=sinopse, diretor=diretor, elenco=elenco, data_lancamento=data, avaliacao_imdb=avaliacao_imdb)
        f.save()
        request.session['filme_titulo'] = titulo
        return render(request, 'filmes/fazer_uploadfilme.html')

    else:
        return render(request, 'filmes/adicionarfilme.html', context)


def fazer_uploadfilme(request):
    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            return render(request, 'filmes/fazer_uploadfilme.html', {
                'error_message': "Selecione um ficheiro antes de dar upload",
            })
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.FILMES_ROOT)
        if not myfile.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return render(request, 'filmes/fazer_uploadfilme.html', {
                'error_message': "Dê upload de uma imagem png ou jpg",
            })
        filename = request.session.get('filme_titulo') + ".jpg"
        if fs.exists(filename):
            fs.delete(filename)
        fs.save(filename, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'filmes/fazer_uploadfilme.html', {
                'uploaded_file_url': uploaded_file_url
            }
        )
    return render(request, 'filmes/fazer_uploadfilme.html')


def avaliacao(request, filme_id, comentario_id=None):
    filme = get_object_or_404(Filme, pk=filme_id)
    if request.method == 'POST':
        comentario = Comentario.objects.get(pk=comentario_id)
        comentario.delete()
        fazeravaliacao(filme)
        return render(request, 'filmes/avaliacao.html',
                      {'filme': filme})
    else:
        return render(request, 'filmes/avaliacao.html',
                      {'filme': filme})


@permission_required('filmes.change_filme', login_url=reverse_lazy('sessao:loginview'))
def editarfilme(request, filme_id):
    filme = get_object_or_404(Filme, pk=filme_id)
    generos = filme.genero
    if generos:
        generos = eval(generos)
    form = FilmeForm(request.POST or None, initial={'generos': generos})

    if request.method == 'POST':
        if len(request.POST['titulo']) != 0:
            if Filme.objects.filter(titulo=request.POST['titulo']).exists():
                return render(request, 'filmes/editarfilme.html', {
                    'error_message': "Título do filme já existe",
                    'form': form,
                    'filme': filme,
                })
            filme.titulo = request.POST['titulo']
        if form.is_valid():
            filme.genero = form.cleaned_data["generos"]
        else:
            filme.genero_preferido = ""
        if len(request.POST['descricao']) != 0:
            filme.descricao = request.POST['descricao']
        if len(request.POST['diretor']) != 0:
            filme.diretor = request.POST['diretor']
        if len(request.POST['elenco']) != 0:
            filme.elenco = request.POST['elenco']
        if len(request.POST['imdb']) != 0:
            filme.avaliacao_imdb = request.POST['imdb']
        if len(request.POST['data_lancamento']) != 0:
            filme.data_lancamento = request.POST['data_lancamento']
        filme.save()
        return render(request, 'filmes/avaliacao.html',
                      {'filme': filme})

    else:
        context = {
            'form': form,
            'filme': filme
        }
        return render(request, 'filmes/editarfilme.html', context)


@login_required(login_url='/sessao/')
def criarcomentario(request, filme_id):
    if request.method == 'POST':
        user = User.objects.get(username=request.session.get('username'))
        filme = get_object_or_404(Filme, pk=filme_id)
        if Comentario.objects.filter(filme_id=filme, user_id=user).exists():
            return render(request, 'filmes/criarcomentario.html', {
                'filme_id': filme_id,
                'error_message': "Já publicou uma avaliação para este filme",
            })
        avaliacao = request.POST['avaliacao']
        if len(request.POST['texto_comentario']) != 0:
            texto_comentario = request.POST['texto_comentario']
        else:
            texto_comentario = ""
        c = Comentario(filme=filme, user=user, texto=texto_comentario, avaliacao=avaliacao, data_criacao=timezone.now())
        c.save()
        fazeravaliacao(filme)
        mandarnotificacao(user, c)
        return HttpResponseRedirect(reverse('filmes:avaliacao', args=(filme_id,)))
    return render(request, 'filmes/criarcomentario.html', {'filme_id': filme_id})


@login_required(login_url='/sessao/')
def editarcomentario(request, filme_id):
    user = User.objects.get(username=request.session.get('username'))
    comentario = get_object_or_404(Comentario, filme=filme_id, user=user.id)
    if request.method == 'POST':
        if request.POST['avaliacao']:
            comentario.avaliacao = request.POST['avaliacao']
        if len(request.POST['texto_comentario']) != 0:
            comentario.texto = request.POST['texto_comentario']
        comentario.save()
        filme = get_object_or_404(Filme, pk=filme_id)
        fazeravaliacao(filme)
        return render(request, 'filmes/editarcomentario.html', {
            'filme_id': filme_id,
            'comentario': comentario,
            'message': "Avaliação publicada",
        })
    else:
        context = {
            'filme_id': filme_id,
            'comentario': comentario,
        }
        return render(request, 'filmes/editarcomentario.html',
                        context)


@login_required(login_url='/sessao/')
def seguir(request, filme_id, user_id):
    user = User.objects.get(id=user_id)
    if hasattr(user, 'moderador'):
        s = Moderador.objects.get(user=user)
    elif hasattr(user, 'utilizador'):
        s = Utilizador.objects.get(user=user)
    else:
        s = Admin.objects.get(user=user)
    if Seguidor.objects.filter(seguidor=request.user, seguido=user):
        segue = True
    else:
        segue = False
    context = {'utilizador': s,
               'segue': segue,
               'filme_id': filme_id
               }
    has_photo = hasphoto(user)
    request.session['visited_user_has_photo'] = has_photo
    if hasattr(user, 'utilizador') and s.banido:
        context = {'utilizador': s,
                   'segue': segue,
                   'filme_id': filme_id,
                   'error_message': "Utilizador Banido",
                   }
        return render(request, 'filmes/seguir.html', context)
    return render(request, 'filmes/seguir.html', context)


def seguiruser(request, user_id):
    # crie um objeto Seguidor com o usuário logado como seguidor e o usuário da página como seguido
    seguido = User.objects.get(id=user_id)
    seguidor = request.user
    s = Seguidor(seguidor=seguidor, seguido=seguido, data_follow=timezone.now())
    s.save()
    data = {'unfollow': 'unfollow-button',
            'follow': 'follow-button'}
    return JsonResponse(data)


def deixarseguir(request, user_id):
    seguimento = Seguidor.objects.filter(seguidor=request.user, seguido=User.objects.get(id=user_id))
    seguimento.delete()
    data = {'unfollow': 'unfollow-button',
            'follow': 'follow-button'}
    return JsonResponse(data)


def demotemoderador(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = False
    user.save()
    m = Moderador.objects.get(user=user)
    genero_preferido = m.genero_preferido
    m.delete()
    u = Utilizador(user=user, genero_preferido=genero_preferido)
    u.save()
    data = {'novo_texto_botao': 'Banir utilizador'}
    return JsonResponse(data)


def banuser(request, user_id):
    user = User.objects.get(id=user_id)
    u = Utilizador.objects.get(user_id=user)
    u.banido = True
    u.save()
    comentarios = Comentario.objects.filter(user_id=user)
    for comentario in comentarios:
        filme = get_object_or_404(Filme, pk=comentario.filme_id.id)
        comentario.delete()
        fazeravaliacao(filme)
    seguidores = Seguidor.objects.filter(seguido=user)
    seguidores.delete()
    seguidos = Seguidor.objects.filter(seguidor=user)
    seguidos.delete()
    data = {'nome_style': 'none'}
    return JsonResponse(data)


def notificacoes(request, user_id, notificacao_id=None):
    if request.method == 'POST':
        notificacao = Notificacao.objects.get(pk=notificacao_id)
        notificacao.delete()
    user = User.objects.get(id=user_id)
    notificacoes = Notificacao.objects.filter(destinatario=user).order_by('-id')
    notificacoes_sem_visto = Notificacao.objects.filter(destinatario=user, visto=False)
    for notificacao in notificacoes_sem_visto:
        notificacao.visto = True
        notificacao.save()
    context = {
        'notificacoes': notificacoes,
        'notificacoes_sem_visto': notificacoes_sem_visto,
    }
    if 'notificacoes_count' in request.session:
        del request.session['notificacoes_count']
    return render(request, 'filmes/notificacoes.html', context)
