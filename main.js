const electron = require('electron')
const App = electron.app
const BrowserWindow = electron.BrowserWindow

var win

function criar_janela(){

	win = new BrowserWindow({
	width: 330,
	height: 400,
	resizable: false,
	webPreferences: {
		nodeIntegration: true
	}
	})

	win.loadFile('./base.html')

}

App.on('ready', criar_janela)
