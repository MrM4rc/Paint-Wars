function movimentar(event){

	if(event['keyCode'] == 38){
		quadrado.Y -= 1
	}
	else if(event['keyCode'] == 40){
		quadrado.Y += 1
	}

	else if(event['keyCode'] == 37){
		quadrado.X -= 1
	}

	else if(event['keyCode'] == 39){
		quadrado.X += 1
	}
	
	contexto.rect(0, 0, 400, 400)
	contexto.fillStyle = "#ffffff"
	contexto.fill()

	contexto.fillStyle = 'rgb(12, 93, 150)'
	contexto.fillRect(quadrado.X, quadrado.Y, quadrado.width, quadrado.height)
}
