"""
URL configuration for dayKards_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login_user'),
    path('baralhos', views.view_list_baralho, name='view_list_baralho'),
    path('cadastro/', views.cadastro_user, name='cadastro'),
    path("cadastro/", views.cadastro_user, name="cadastro"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("baralho/criar/", views.criar_baralho, name="criar_baralho"),
    path("baralho/<int:baralho_id>/deletar/", views.deletar_baralho, name="deletar_baralho"),
    path( "baralho/<int:baralho_id>/card/criar/",views.criar_card,name="criar_card"),
    path("card/<int:card_id>/deletar/",views.deletar_card,name="deletar_card"),
    path("baralho/<int:baralho_id>/revisar/",views.revisar_baralho,name="revisar_baralho"),
    path( "baralho/<int:baralho_id>/revisar/<int:card_id>/",views.revisar_baralho,name="revisar_card"),   
]



