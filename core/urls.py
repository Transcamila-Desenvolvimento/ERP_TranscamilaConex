from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirecionar_ultima_sessao, name='root_redirect'),
    path('login/', views.login_view, name='login'),
    path('selecao-ambiente/', views.selecao_ambiente, name='selecao_ambiente'),
    path('acessar-ambiente/', views.acessar_ambiente, name='acessar_ambiente'),
    path('logout/', views.logout_view, name='logout'),
    path('redirecionar/', views.redirecionar_ultima_sessao, name='redirecionar_ultima_sessao'),
]