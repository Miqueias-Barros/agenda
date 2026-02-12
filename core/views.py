from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


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
    eventos = Evento.objects.filter(usuario=user)
    return render(request, 'agenda.html', {'eventos': eventos})

@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')

@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        local_evento = request.POST.get('local_evento')
        usuario = request.user
        Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, local_evento=local_evento, usuario=usuario)

    return redirect('/agenda/')

