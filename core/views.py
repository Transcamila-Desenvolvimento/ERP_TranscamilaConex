from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Filial, Ambiente, UsuarioFilial, SessaoUsuario

def login_view(request):
    # Se já está logado, redireciona para a última sessão
    if request.user.is_authenticated:
        try:
            sessao = SessaoUsuario.objects.get(usuario=request.user)
            return HttpResponseRedirect(sessao.get_redirect_url())
        except SessaoUsuario.DoesNotExist:
            return redirect('selecao_ambiente')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Redireciona para a última sessão
            try:
                sessao = SessaoUsuario.objects.get(usuario=user)
                return HttpResponseRedirect(sessao.get_redirect_url())
            except SessaoUsuario.DoesNotExist:
                return redirect('selecao_ambiente')
        else:
            return render(request, 'core/login.html', {'error': 'Credenciais inválidas'})
    
    return render(request, 'core/login.html')

@login_required
def selecao_ambiente(request):
    # Atualizar sessão para indicar que está na seleção
    sessao, created = SessaoUsuario.objects.get_or_create(usuario=request.user)
    sessao.em_selecao_ambiente = True
    sessao.save()
    
    # Obter filiais e ambientes permitidos para o usuário
    usuario_filiais = UsuarioFilial.objects.filter(usuario=request.user).prefetch_related('ambientes')
    
    context = {
        'usuario_filiais': usuario_filiais,
        'usuario': request.user,
    }
    return render(request, 'core/selecao_ambiente.html', context)

@login_required
def acessar_ambiente(request):
    if request.method == 'POST':
        ambiente_id = request.POST.get('ambiente')  # código numérico
        filial_codigo = request.POST.get('filial')
        
        print(f"DEBUG: Ambiente: {ambiente_id}, Filial: {filial_codigo}")  # Para debug
        
        try:
            ambiente = Ambiente.objects.get(codigo=ambiente_id)
            filial = Filial.objects.get(codigo=filial_codigo)
            
            # Verificar permissão
            usuario_filial = UsuarioFilial.objects.get(
                usuario=request.user, 
                filial=filial
            )
            if ambiente not in usuario_filial.ambientes.all():
                return redirect('selecao_ambiente')
            
            # Atualizar sessão
            sessao, created = SessaoUsuario.objects.get_or_create(usuario=request.user)
            sessao.ultimo_ambiente = ambiente
            sessao.ultima_filial = filial
            sessao.em_selecao_ambiente = False
            sessao.ultima_url = ambiente.get_absolute_url()
            sessao.save()
            
            print(f"DEBUG: Redirecionando para: {ambiente.get_absolute_url()}")  # Para debug
            
            # Redireciona automaticamente para o ambiente
            return HttpResponseRedirect(ambiente.get_absolute_url())
            
        except (Ambiente.DoesNotExist, Filial.DoesNotExist, UsuarioFilial.DoesNotExist) as e:
            print(f"DEBUG: Erro - {e}")  # Para debug
            return redirect('selecao_ambiente')
    
    return redirect('selecao_ambiente')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def redirecionar_ultima_sessao(request):
    """View para redirecionar para a última sessão do usuário"""
    try:
        sessao = SessaoUsuario.objects.get(usuario=request.user)
        return HttpResponseRedirect(sessao.get_redirect_url())
    except SessaoUsuario.DoesNotExist:
        return redirect('selecao_ambiente')