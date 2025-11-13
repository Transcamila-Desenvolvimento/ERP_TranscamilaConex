# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import SessaoUsuario
from .models import ContaFixa

@login_required
def home(request):
    try:
        sessao = SessaoUsuario.objects.get(usuario=request.user)
        ambiente = sessao.ultimo_ambiente
        filial = sessao.ultima_filial
    except SessaoUsuario.DoesNotExist:
        return redirect('selecao_ambiente')
    
    context = {
        'ambiente': ambiente,
        'filial': filial,
        'usuario': request.user,
    }
    return render(request, 'provisao_ibipora/home.html', context)


@login_required
def contasfixas(request):
    # 1. Buscar todas as contas com ordenação
    contas_list = ContaFixa.objects.all().order_by('filial', 'chegada', 'fornecedor')

    # 2. Paginação
    paginator = Paginator(contas_list, 10)  # 10 por página
    page = request.GET.get('page')

    try:
        contas = paginator.page(page)
    except PageNotAnInteger:
        contas = paginator.page(1)
    except EmptyPage:
        contas = paginator.page(paginator.num_pages)

    # 3. Contexto para o template
    context = {
        'contas': contas,
        'page_obj': contas,  # compatível com o template
        'paginator': paginator,
        'is_paginated': contas.has_other_pages(),
    }

    return render(request, 'provisao_ibipora/cadastrocontas.html', context)


    

@login_required
def calendario(request):
    return render(request, 'provisao_ibipora/calendario.html')
