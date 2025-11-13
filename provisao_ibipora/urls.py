from django.urls import path
from . import views

app_name = 'provisao_ibipora'

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastros/contasfixas', views.contasfixas, name='contasfixas'),
    path('calendario', views.calendario, name='calendario'),
]