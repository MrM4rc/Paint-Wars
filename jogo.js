const jQuery = require('jquery')

// variables that containing all struct for game
let jogo
let players

// this function init the game
function init_game(){
	// request game data
	resp = jQuery.get('http://127.0.0.1:8000/', dataType='json').done(function(data){

		if(data['state'] == 'available'){

			jogo = data
			// variable that containing all players in game
			players = jogo.players
			// variable that storage your entity in game
			you = jogo['you'].index
			draw_world()
			for(var elemento in players){
				draw_players(players[elemento], players[elemento].color)
			}
			update_screen()
		}

		else{
			// ask if game is full
			window.alert('Jogo esta cheio')
			return 0
		}
	})
}

// this function display the winner
function end_game(){
	window.alert(`Fim!! vencedor: ${jogo.most_score["0"]}`)
}

// this function refresh screen
function update_screen(){

	jQuery.get('http://127.0.0.1:8000/data', data={version: jogo.version}).done(function(data){
		if(data.state == 'available' || data.state == 'full'){

			// variable that containg data of game
			jogo = data
			// variable that containg all players
			players = jogo.players
			// curret time of match
			time = jogo.time
			// update time element
			document.getElementById('progress').style = `width: ${((time/60)/3)*100}`
			// clear screen
			clear_screen()
			// drawin map
			draw_world()

			// loop throug players variable
			for(var elemento in players){
				
				player = players[elemento]
				// drawing the players
				draw_players(player, player.color)
			}
			update_screen()
		}

		else{
			jogo = data
			end_game()
		}
	})

}

// this function move the player
function walker(direction, index){
	jQuery.get('http://127.0.0.1:8000/walker/', data={direction: direction, index: index})
}
// this function clear screen
function clear_screen(){
	contexto.fillStyle = '#ffffff'
	contexto.fillRect(0, 0, 400, 400)
}

function draw_world(){
	
	for(var y in jogo.world){
		for(x=0; x <= 100; x++){
			//window.alert(jogo.world[y][x])
			contexto.fillStyle = jogo.world[y][x]
			contexto.fillRect(x, y, 1, 1)
		}
	}
	
}

// this function draw players
function draw_players(object, style){

	// define style of each player
	contexto.fillStyle = style
	// draw a rectangle
	contexto.fillRect(object.X, object.Y, object.width, object.height)
	// define style of border
	contexto.fillStyle = '#000000'
	//draw border of players
	contexto.strokeRect(object.X, object.Y, object.width, object.height)

}

// Listening all keydown events
document.addEventListener("keydown", function(event){
	// call walker function to move player
	if(event['keyCode'] == 38){
		walker('up', you)
	}
	else if(event['keyCode'] == 40){
		walker('down', you)
	}

	else if(event['keyCode'] == 37){
		walker('left', you)
	}

	else if(event['keyCode'] == 39){
		walker('right', you)
	}
	//#####################################
})

let canvas_bolado = document.getElementById('canvas_bolado')
let contexto = canvas_bolado.getContext("2d")

let you
clear_screen()
init_game()
