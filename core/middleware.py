from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import resolve
from .models import SessaoUsuario, UsuarioFilial

class VerificacaoPermissaoMiddleware(MiddlewareMixin):
    """
    Middleware para verificar se o usuário tem permissão para acessar o ambiente
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # URLs públicas que não precisam de verificação
        urls_publicas = [
            '/login/',
            '/logout/', 
            '/admin/',
            '/static/',
            '/media/',
            '/selecao-ambiente/',
            '/acessar-ambiente/',
            '/redirecionar/',
        ]
        
        current_path = request.path
        
        # Verifica se a URL atual é pública
        if any(current_path.startswith(url) for url in urls_publicas):
            return None
        
        # Se não está autenticado, redireciona para login
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('login')
        
        print(f"🔐 VERIFICAÇÃO MIDDLEWARE: {request.user.username} acessando {current_path}")
        
        # Para URLs de ambientes específicos, verifica permissão
        if current_path.startswith('/provisao-ibipora/'):
            return self.verificar_permissao_ambiente(request, 'provisao_ibipora')
        
        # Adicione aqui outros ambientes conforme for criando
        # elif current_path.startswith('/outro-ambiente/'):
        #     return self.verificar_permissao_ambiente(request, 'outro_app')
        
        return None
    
    def verificar_permissao_ambiente(self, request, app_name):
        """Verifica se o usuário tem permissão para o ambiente específico"""
        try:
            sessao = SessaoUsuario.objects.get(usuario=request.user)
            
            # Se está em seleção de ambiente, não deveria estar aqui
            if sessao.em_selecao_ambiente:
                print(f"🚫 MIDDLEWARE: {request.user.username} em seleção tentando acessar ambiente")
                return redirect('selecao_ambiente')
            
            # Verifica se tem ambiente e filial definidos
            if not sessao.ultimo_ambiente or not sessao.ultima_filial:
                print(f"🚫 MIDDLEWARE: {request.user.username} sem ambiente/filial definido")
                return redirect('selecao_ambiente')
            
            # Verifica se o app_name do ambiente atual corresponde ao que está sendo acessado
            if sessao.ultimo_ambiente.app_name != app_name:
                print(f"🚫 MIDDLEWARE: Ambiente da sessão ({sessao.ultimo_ambiente.app_name}) não corresponde ao acessado ({app_name})")
                return redirect('selecao_ambiente')
            
            # Verifica permissão específica
            try:
                usuario_filial = UsuarioFilial.objects.get(
                    usuario=request.user,
                    filial=sessao.ultima_filial
                )
                
                if sessao.ultimo_ambiente not in usuario_filial.ambientes.all():
                    print(f"🚫 MIDDLEWARE: {request.user.username} sem permissão para {sessao.ultimo_ambiente.nome}")
                    return redirect('selecao_ambiente')
                else:
                    print(f"✅ MIDDLEWARE: {request.user.username} tem permissão para {sessao.ultimo_ambiente.nome}")
                    
            except UsuarioFilial.DoesNotExist:
                print(f"🚫 MIDDLEWARE: {request.user.username} sem vínculo com {sessao.ultima_filial.nome}")
                return redirect('selecao_ambiente')
                
        except SessaoUsuario.DoesNotExist:
            print(f"🚫 MIDDLEWARE: {request.user.username} sem sessão")
            return redirect('selecao_ambiente')
        
        return None

class RastreamentoSessaoMiddleware(MiddlewareMixin):
    """
    Middleware para rastrear a última URL acessada pelo usuário
    """
    
    def process_response(self, request, response):
        if request.user.is_authenticated and not request.user.is_anonymous:
            # URLs que não devem ser rastreadas
            urls_ignoradas = [
                '/login/',
                '/logout/',
                '/admin/',
                '/static/',
                '/media/',
                '/acessar-ambiente/',
            ]
            
            current_path = request.path
            
            # Verifica se a URL atual deve ser ignorada
            ignorar = any(current_path.startswith(url) for url in urls_ignoradas)
            
            if not ignorar and request.method == 'GET' and response.status_code == 200:
                try:
                    sessao, created = SessaoUsuario.objects.get_or_create(usuario=request.user)
                    
                    # Atualiza a última URL
                    if current_path != '/selecao-ambiente/':
                        sessao.ultima_url = current_path
                        sessao.em_selecao_ambiente = False
                    else:
                        sessao.em_selecao_ambiente = True
                        sessao.ultima_url = None
                    
                    sessao.save()
                    
                except Exception as e:
                    print(f"Erro ao atualizar sessão: {e}")
        
        return response