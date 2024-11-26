from django.urls import path
from .views import welcome_view, cadastro_view, login_view, logout_view, home_view, reservar_view, notificar_quando_chegar_view, verifica_validacao_email_view

urlpatterns = [
    path('', welcome_view, name="welcome"),
    path('cadastro/', cadastro_view, name="cadastro"), 
    path('verifica_validacao_email/<str:cliente_email>', verifica_validacao_email_view, name="verifica_validacao_email"),
    path('login/', login_view, name="login"), 
    path('logout/', logout_view, name="logout"), 
    path('home/', home_view, name="home"), 
    path('reservar<carro_id>/', reservar_view, name="reservar"), 
    path('notificar<carro_id>', notificar_quando_chegar_view, name="notificar")
]
