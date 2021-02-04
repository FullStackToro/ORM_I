from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('initialize', views.make_data, name="make_data"),
	path('ligas/<op>/', views.consulta_league, name="ligas"),
	path('teams/<op>/', views.consulta_teams, name="teams"),
	path('player/<op>/', views.consulta_player, name="player"),
	path('orm2/teams/<op>', views.orm2_teams, name="teams_orm2"),
]
