$( document ).ready(function() {
	
	var playing = false
	
	var socket = new WebSocket("ws://" + window.location.host + "/gomoku/");

	socket.onopen = function() {
		var data = {};
		data.inRoom = "True";
	    socket.send(JSON.stringify(data));
	    
	}
	if (socket.readyState == WebSocket.OPEN) socket.onopen();
	socket.onmessage = function(e) {
		var receiveData = JSON.parse(e.data);
		console.log(e.data);
		if(receiveData.hasOwnProperty('playersOnlineHtml'))
			$('#playersOnline').html(receiveData.playersOnlineHtml);
		if(receiveData.hasOwnProperty('gomokuRoomsHtml'))
			$('#rooms').html(receiveData.gomokuRoomsHtml);
		//console.log(e.data);
		if(receiveData.hasOwnProperty('board')){
			var board = receiveData.board
			for (var i = 0; i<15; i++){
				for (var j=0; j<15; j++) {
					if (board[i][j]=='x')
						$('#cell-' + i + '-' + j).css("background-color","yellow");
					else if (board[i][j]=='o')
						$('#cell-' + i + '-' + j).css("background-color","green");
					else
						$('#cell-' + i + '-' + j).css("background-color","#b1eff5");
				}
			}
		}
		
		if(receiveData.hasOwnProperty('myTurn')){
			myTurn = receiveData.myTurn
			if (myTurn) {
				playing = true
			}
			else {
				playing = false
			}
		}		
        //socket.send(JSON.stringify(data));	    
	}
    socket.onclose = function(){ 
    };
	
	
	setInterval(getGameBoard, 500);

	$('button#resign').hide();
	

	
	var cw = $('.cell').width();
	$('.cell').css({'height':cw+'px'});
	
	
	$(window).resize(function() {
		cw = $('.cell').width();
		$('.cell').css({'height':cw+'px'});
	});

	$('button#player1').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer1": true}
		
		$.post( "/gomokuStartGame/", data, function( json ) {
			  
			});
			
	});
	$('button#player2').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer2": true}
		
		$.post( "/gomokuStartGame/", data, function( json ) {
			  
			});
		/*
		if($(this).prop('disabled') && $('button#player1').prop('disabled')){
			$('button#startGame').prop('disabled',false);
		}
		*/
		
	});
	$('button#startGame').on('click', function() {
		$('button#startGame').prop('disabled',false);
		
		var ready = true
		var data = {"readyToPlay" : ready};
		
		$.post( "/gomokuStartGame/", data, function( json ) {
			});
		
	});
	
	$('button#resign').on('click', function() {
		$('button#resign').prop('disabled',false);
		
		var resign = true
		var data = {"resign" : resign};
		
		$.post( "/gomokuStartGame/", data, function( json ) {
			$('button#resign').hide();
			});
		
	});

	$("div.cell").on('click', function(event) {
		if(playing) {
			var target = event.target || event.srcElement;
			var id = target.id;
			var values = id.split('-');
			for(var i=0;i<values.length;i++) console.log(values[i]);
			//$(this).css("background-color","yellow");
			console.log(id);
			var dataToSend = {};
			dataToSend.move = {}
			dataToSend.move.i = parseInt(values[1]);
			dataToSend.move.j = parseInt(values[2]);
			socket.send(JSON.stringify(dataToSend));
		}
	});	
	
        
});




function sendDataGameBoard(){
	$.post( "/gomokuStartGame/", data, function( json ) {
	});
}

function getGameBoard(){
    $.get('/gomokuGameBoard/', function(json){
    	
    
    	if(json.hasOwnProperty('namePlayer1'))
    		$('button#player1').html(json.namePlayer1);
    	
    	if(json.hasOwnProperty('namePlayer2'))
    		$('button#player2').html(json.namePlayer2);
    	
    	if(json.hasOwnProperty('startButton')){
    		if (json.startButton){
    			$('button#startGame').prop('disabled',false);
    		}
    		else {
    			$('button#startGame').prop('disabled',true);
    		}
    	}
    	if(json.hasOwnProperty('startButtonName'))
    		$('button#startGame').html(json.startButtonName);
    	if(json.hasOwnProperty('player1Button')){
    		if (json.player1Button){
    			$('button#player1').prop('disabled',false);
    		}
    		else {
    			$('button#player1').prop('disabled',true);
    		}
    	}
    	if(json.hasOwnProperty('player2Button')){
    	    if (json.player2Button){
    	    	$('button#player2').prop('disabled',false);
    	    }
    	    else {
    	    	$('button#player2').prop('disabled',true);
    	    }
    	}
    	if(json.hasOwnProperty('playerResign')){
    	    if (json.playerResign){
    	    	$('button#resign').show();
    	    }
    	    else {
    	    	$('button#resign').hide();
    	    }

    	}    	
    });    	
}