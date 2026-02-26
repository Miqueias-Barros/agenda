from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404
from django.http import JsonResponse


@csrf_exempt
def submit_login(request):
    ...

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('/agenda/')
        else:
            messages.error(request, "Usuário ou senha inválidos!")

    return redirect('/login/')

@login_required(login_url='/login/')
def lista_eventos(request):
    user = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    eventos = Evento.objects.filter(usuario=user, 
                                    data_evento__gt=data_atual)
    return render(request, 'agenda.html', {'eventos': eventos})

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local_evento = request.POST.get('local_evento')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       data_evento=data_evento,
                                                       descricao=descricao,
                                                       local_evento=local_evento)
        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, local_evento=local_evento, usuario=usuario)

    return redirect('/agenda/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()    
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/agenda/')

@login_required(login_url='/login/')
def json_lista_evento(request):
    user = request.user
    eventos = Evento.objects.filter(usuario=user).values('id', 'titulo')
    return JsonResponse(list(eventos), safe=False)
