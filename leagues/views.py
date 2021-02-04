from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Q
from django.db.models import Count

from . import team_maker

def index(request):

	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}

	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")

def consulta_league(request, op):

	if op == '1':
		temp = League.objects.filter(sport__istartswith="Baseball")
	elif op == '2':
		temp = League.objects.filter(name__contains='Woman')  #MODIFICAR
	elif op == '3':
		temp = League.objects.filter(sport__contains='Hockey')
	elif op == '4':
		temp = League.objects.exclude(sport__contains='Football').exclude(sport__contains='Soccer')
	elif op == '5':
		temp = League.objects.filter(name__contains='Conference')
	elif op == '6':
		temp = League.objects.filter(name__contains='Woman')
		#MODIFICAR
	else:
		return redirect('index')
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		'ligas': temp,
	}
	return render(request, f"leagues/ligas.html", context)

def consulta_teams(request, op):

	if op == '1':
		temp=Team.objects.filter(team_name__iexact='raptors') #MODIFICAR
	elif op == '2':
		temp=Team.objects.filter(team_name__iexact='raptors')
	elif op == '3':
		temp=Team.objects.filter(location__contains='City')
	elif op == '4':
		temp=Team.objects.filter(team_name__istartswith='T')
	elif op== '5':
		temp=Team.objects.all().order_by('location')
	elif op == '6':
		temp=Team.objects.all().order_by('-team_name')
	else:
		return redirect('index')
	if len(temp)>0:
		context = {
			"leagues": League.objects.all(),
			"teams": Team.objects.all(),
			"players": Player.objects.all(),
			'equipos': temp,
		}
	else:
		pass
	return render(request, f"leagues/teams.html", context)

def consulta_player(request, op):
	if op == '1':
		temp=Player.objects.filter(last_name__iexact='cooper')
	elif op == '2':
		temp = Player.objects.filter(first_name__iexact='Joshua')
	elif op == '3':
		temp = Player.objects.filter(last_name__iexact='cooper').exclude(first_name__iexact='Joshua')
	elif op == '4':
		temp = Player.objects.filter(first_name__iexact='Alexander')|Player.objects.filter(first_name__iexact='Wyatt')
	else:
		return redirect('index')

	for player in temp:
		last_team=player.all_teams.all()
		print(player.all_teams.all())
		for equipo in last_team:
			print(f'Jugador {player.first_name} {player.last_name}; Equipo', equipo.team_name)

	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		'jugadores': temp,
	}
	return render(request, f"leagues/player.html", context)

def orm2_teams(request, op):
	if op == '1':
		temp1 = League.objects.filter(name__iexact="National Soccer Association")
		temp = Team.objects.filter(league__in=temp1)
		for team in temp:
			print(team.id, team.team_name, team.location, team.league.name)
	if op == '2':
		temp1 =Team.objects.filter(team_name__iexact="Boston Penguins")
		temp = Player.objects.filter(curr_team__in=temp1)
		print(temp)
		for player in temp:
			print(player.id, player.first_name, player.curr_team.team_name)
	if op =='3':
		temp2 = League.objects.filter(name__iexact="International Collegiate Basketball Conference")
		temp1 =Team.objects.filter(league__in=temp2)
		temp=Player.objects.filter(curr_team__in=temp1)
		for player in temp:
			print(player.id, player.first_name, player.last_name, player.curr_team.team_name, player.curr_team.league.name)
	if op=='4':
		temp2 = League.objects.filter(name__iexact="Conferencia Americana de Fútbol Amateur")
		temp1 =Team.objects.filter(league__in=temp2)
		temp=Player.objects.filter(curr_team__in=temp1).filter(last_name__iexact="López")
		for player in temp:
			print(player.id, player.first_name, player.last_name, player.curr_team.team_name, player.curr_team.league.name)

	if op == '5':
		temp=Player.objects.filter(all_teams__league__sport__iexact="Football") | Player.objects.filter(all_teams__league__sport__iexact="Soccer")

		for player in temp:
			for team in player.all_teams.all():
				print(player.id, player.first_name, player.last_name, team.team_name)

	if op =='6':
		temp = Team.objects.filter(curr_players__first_name__icontains="Sophia")
		for team in temp:
			for jugador in team.curr_players.all():
				if jugador.first_name == "Sophia":
					print("Name:", jugador.first_name, jugador.last_name, "\nTeam:", team.team_name, "\n")

	if op=='7':
		temp =League.objects.filter(teams__curr_players__first_name__icontains="Sophia").all().distinct()
		for league in temp:
			print(league.name)
			for team in league.teams.all():
				for jugador in team.curr_players.all():
					pass

	if op=='8':
		temp = Player.objects.filter(last_name__icontains="Flores").exclude(curr_team__team_name="Washington Roughriders")
		for jugador in temp:
				print(jugador.first_name, jugador.last_name, jugador.curr_team.team_name)

	if op == '9':
		temp =Team.objects.filter(curr_players__first_name__icontains="Samuel", curr_players__last_name__icontains="Evans")
		for team in temp:
			print("equipo", team.team_name)

	if op =='10':
		temp = Player.objects.filter(all_teams__team_name__icontains="Manitoba Tiger-Cats")

	if op=='11':
		temp=Player.objects.filter(all_teams__team_name__icontains="Wichita Vikings").exclude(curr_team__team_name__icontains="Wichita Vikings")
		for team in temp:
			print("equipo", team.team_name)

	if op == '12':
		temp =Team.objects.filter(all_players__first_name__icontains="Jacob", all_players__last_name__icontains="Gray")

		# Alternativa para realizar un AND
		# Alt_1=Team.objects.filter(all_players__first_name__icontains="Jacob")&Team.objects.filter(all_players__last_name__icontains="Gray")

		# Alternativa para Realizar un OR (Se debe realizar un from django.db.models import Q)
		# alt_2=Team.objects.filter(Q(all_players__first_name__icontains="Jacob")|Q(all_players__last_name__icontains="Gray"))
		# alt_3=Team.objects.filter(Q(all_players__first_name__icontains="Jacob")&Q(all_players__last_name__icontains="Gray"))

		for team in temp:
			for jugador in team.all_players.all():
				#if jugador.first_name=="Jacob":
				print("equipo", team.team_name, "jugador", jugador.first_name, jugador.last_name)

	if op=='13':
		temp=Player.objects.filter(all_teams__league__name__icontains="Atlantic Federation of Amateur Baseball Players")

	if op == '14':
		temp = Team.objects.annotate(Count('all_players')).filter(all_players__count__gt=11)
		for team in temp:
			print(team.team_name, team.all_players__count)

	if op == '15':
		temp = Player.objects.annotate(Count('all_teams')).order_by('-all_teams__count')
		for jugador in temp:
			print(jugador.first_name, jugador.last_name, jugador.all_teams__count)


	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),

	}
	return render(request, f"leagues/orm2_teams.html", context)