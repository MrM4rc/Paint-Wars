from django.shortcuts import render
from django.http import JsonResponse
from random import randint, choice
import time
from threading import Thread

# Create your views here.
# variable that containg o world of game
world = []
# all setting of game
jogo = {}
# players colors
colors = []

# this function init o game
def init_server():
	
	global world
	global jogo
	global colors
	
	world = []
	jogo = {'playersGame': -1, 'world': world, 'players': [], 'you': {}, 'version': 0, 'state': 'available', 'time': 0, 'most_score': ['', -10]}
	colors = ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']

# update time of match
def timer():

	while True:
		
		# end timer when time is equal 3 minutes
		if jogo['time'] == 60*3:
			
			verify_winner()
			break

		time.sleep(1)
		jogo['time'] += 1
		jogo['version'] += 1


# this function verify o winner of match
def verify_winner():
	
	# loop throug each line of world
	for y in world:
		# loop throug each column of world
		for x in y:
			
			# loop throug each player to verify if your color is equal x
			for player in jogo['players']:
				
				# if true, increament +1 in player score
				if player['color'] == x:
					
					player['score'] += 1
	# loop to verify which player done most score
	for player in jogo['players']:

		if jogo['most_score'][1] < player['score']:

			jogo['most_score'][1] = player['score']

			if player['color'] == 'rgb(255, 0, 0)':

				jogo['most_score'][0] = 'Red'

			elif player['color'] == 'rgb(0, 255, 0)':

				jogo['most_score'][0] = 'Green'

			elif player['color'] == 'rgb(0, 0, 255)':

				jogo['most_score'][0] = 'Blue'

	jogo['state'] = 'end'
	jogo['version'] += 1


# this function init new players
def init_player(request):

	global jogo
	global world
	
	if len(jogo) == 0:

		init_server()

	if len(colors) == 0:

		return JsonResponse({'state': 'full'})
	
	# init world
	for c in range(100):

		world.append(['#ffffff' for c in range(100)])

	if request.method == 'GET':
		# choice the player color
		color = choice(colors)
		colors.remove(color)
		# variable that containg all attributes of player
		you = {'name': f'player-{jogo["playersGame"] + 1}', 'X': 0, 'Y': 0, 'width': 10, 'height': 10, 'index': jogo['playersGame'] + 1, 'color': color, 'score': 0}
		# storage player in a list
		jogo['players'].append(you)
		jogo['you'] = you
		jogo['playersGame'] += 1
		jogo['version'] += 1
	# thread that initalize timer count
	thread = Thread(target=timer)
	thread.start()

	return JsonResponse(jogo)


# this function control all keyboard events
def walker(request):

	global jogo
	global world
	
	# verify if player press key up
	if request.GET['direction'] == 'up':
		# verify if player is world limit
		if jogo['players'][int(request.GET['index'])]['Y'] - 1 > -1:
			# move player one pixel
			jogo['players'][int(request.GET['index'])]['Y'] -= 1
	# verify if player press key down
	elif request.GET['direction'] == 'down':
		# verify if player is world limit
		if jogo['players'][int(request.GET['index'])]['Y'] + 10 < 100:
			# move player one pixel
			jogo['players'][int(request.GET['index'])]['Y'] += 1
	# verify if player press key left
	elif request.GET['direction'] == 'left':
		# verify if player is world limit
		if jogo['players'][int(request.GET['index'])]['X'] - 1 > -1:
			# move player one pixel
			jogo['players'][int(request.GET['index'])]['X'] -= 1
	# verify if player press key right
	elif request.GET['direction'] == 'right':
		# verify if player is world limit
		if jogo['players'][int(request.GET['index'])]['X'] + 10 < 100:
			# move player one pixel
			jogo['players'][int(request.GET['index'])]['X'] += 1
	# this for control height pixel of player
	for y in range(jogo['players'][int(request.GET['index'])]['Y'], jogo['players'][int(request.GET['index'])]['Y'] + 10):
		# this for control width puxel of player
		for x in range(jogo['players'][int(request.GET['index'])]['X'], jogo['players'][int(request.GET['index'])]['X'] + 10):
			# update world color
			world[y][x] = jogo['players'][int(request.GET['index'])]['color']

	jogo['version'] += 1

	return JsonResponse(jogo)


# this function send data for all players
def send_data(request):

	global jogo
	
	# not send data while version of jogo is don't updated
	while int(request.GET['version']) == jogo['version']:

		pass

	if jogo['time'] != 60 * 4:

		return JsonResponse(jogo)
	
	else:

		jogo['state'] = 'end'

		
		return JsonResponse(jogo)


