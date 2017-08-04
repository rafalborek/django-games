
var allCards = [];

//var suit = ["Clubs", "Diamonds", "Hearts", "Spades"];
var suit = ["C", "D", "H", "S"];
var rank = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"];

$( document ).ready(function() {
	
	
	for(var i=0; i<13; i++) {
		allCards.push(suit[0] + " " + rank[i]);				
	}	
	for(var i=0; i<13; i++) {
		allCards.push(suit[1] + " " + rank[i]);				
	}	
	for(var i=0; i<13; i++) {
		allCards.push(suit[2] + " " + rank[i]);				
	}	
	for(var i=0; i<13; i++) {
		allCards.push(suit[3] + " " + rank[i]);				
	}	
	
	
	var playing = false;
	var auctionMove = false;
	
	var suitGame = "...";
	var pointsToGet = 0;
	var suitAuction = "...";
	var pointsAuction = "0";
	var pointsTake = 0;
	var winnerAuction = "None";
	var secondPlaying = "None";
	
	
    var canvas=document.getElementById("gameBridgeCanvas");
    var context=canvas.getContext("2d");
    context.beginPath();
    context.arc(95,50,40,0,2*Math.PI);
    context.stroke();
    var cards = {};
    //bottom
    cards.my = [];
    //top
    cards.teamMate= [];
    //left
    cards.opponentFirst =[];
    //right
    cards.opponentSecond =[];
    
    
    
    cards.mySide="South";
    cards.teamMateSide = "North";
    cards.opponentFirstSide = "West";
    cards.opponentSecondSide = "East";
    
    var sideGame = "South";
    var sideGameTeamMate = "North";
    	
    	
    context.clearRect(0, 0, canvas.width, canvas.height);    
    
    
    coordinatesOfCards();
    
    
    //drawCardsRect();
    
    drawElementsInCanvas();
    
    $('#auctionButtons').hide();
    
	var socket = new WebSocket("ws://" + window.location.host + "/bridge/");

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
		if(receiveData.hasOwnProperty('bridgeRoomsHtml'))
			$('#rooms').html(receiveData.bridgeRoomsHtml);
		//console.log(e.data);
		
		if(receiveData.hasOwnProperty('sideGame')){
			sideGame = receiveData.sideGame;
			
	            var bottomText = "South"
	            
	            var topText = "North";
	            var leftText = "West";
	            var rightText = "East";
	            
	            if(sideGame=="North"){
	                
	            	cards.mySide = "North";
	            	bottomText = "North";
	                
	            	cards.teamMateSide="South";
	                topText = "South";
	                
	                cards.opponentFirstSide = "East";
	                leftText = "East";
	                cards.opponentSecondSide = "West";
	                rightText = "West";
	            }	
	            else if(sideGame=="East"){
	            	cards.mySide ="East";
	                bottomText = "East";
	                
	                cards.teamMateSide="West";
	                topText = "West";
	                
	                cards.opponentFirstSide="South";
	                leftText = "South";
	                
	                cards.opponentSecondSide = "North";
	                rightText = "North";
	            }	
	            else if(sideGame=="West"){
	            	cards.mySide = "West";
	                bottomText = "West";
	                cards.teamMateSide = "East";
	                topText = "East";
	                
	                cards.opponentFirstSide="North";
	                leftText = "North";
	                
	                cards.opponentSecondSide = "South";
	                rightText = "South";
	            }	
		}
		
		if(receiveData.hasOwnProperty('pointsAuction')){
			pointsToGet = parseInt(receiveData.pointsAuction);
			
		}
		
		if(receiveData.hasOwnProperty('suitGame')){
			suitGame = receiveData.suitGame;
			
		}
		if(receiveData.hasOwnProperty('secondPlaying')){
			secondPlaying = receiveData.secondPlaying;
			
		}
		if(receiveData.hasOwnProperty('winnerAuction')){
			winnerAuction = receiveData.winnerAuction;
			
		}  		
		if(receiveData.hasOwnProperty('cardsSecond')){
			cardsSecond = receiveData.cardsSecond;
	        if(secondPlaying==cards.teamMateSide){
				for(var i=0; i< cardsSecond.length;i++){
					cards.teamMate[i].value = cardsSecond[i];
				}	        	
	        }
	        if(secondPlaying==cards.opponentFirstSide){
				for(var i=0; i< cardsSecond.length;i++){
					cards.opponentFirst[i].value = cardsSecond[i];
				}	        	
	        }
	        if(secondPlaying==cards.opponentSecondSide){
				for(var i=0; i< cardsSecond.length;i++){
					cards.opponentSecond[i].value = cardsSecond[i];
				}	        	
	        }        
			
			
			
		}  		
	    
		if(receiveData.hasOwnProperty('cards')){
			var receiveCards = receiveData.cards;
			for(var i=0; i< receiveCards.length;i++){
				cards.my[i].value = receiveCards[i];
				//console.log(cards.my[i]);
/*		        context.fillStyle = "#000000";
		        context.font = "14px Arial";
		        context.textAlign="center"; 
		        context.textBaseline = "middle";
		        if(i<13)
		        	context.fillText(receiveCards[i].toString(),cards.my[i].x+(cards.my[i].width/2),cards.my[i].y+(cards.my[i].height/2));
		        else if(i>=13 && i<26) {
		        	var j=i-13;
		        	context.fillText(receiveCards[i].toString(),cards.teamMate[j].x+(cards.teamMate[j].width/2),cards.teamMate[j].y+(cards.teamMate[j].height/2));
				}
		        else if(i>=26 && i<39) {
		        	var j=i-26;
		        	context.fillText(receiveCards[i].toString(),cards.opponentFirst[j].x+(cards.opponentFirst[j].width/2),cards.opponentFirst[j].y+(cards.opponentFirst[j].height/2));

		        }
		        else if(i>=39) {
		        	var j=i-39;
		        	context.fillText(receiveCards[i].toString(),cards.opponentSecond[j].x+(cards.opponentSecond[j].width/2),cards.opponentSecond[j].y+(cards.opponentSecond[j].height/2));

		        }*/
			}
		}
		
		if(receiveData.hasOwnProperty('myTurn')){
			var myTurn = receiveData.myTurn
			if (myTurn) {
				playing = true
			}
			else {
				playing = false
			}
		}
		
		if(receiveData.hasOwnProperty('auctionMove')){
			auctionMove = receiveData.auctionMove
			if (auctionMove) {
				$('#auctionButtons').show();
			}
			else {
				$('#auctionButtons').hide();
			}
		}
		drawElementsInCanvas();
        //socket.send(JSON.stringify(data));	    
	}
    socket.onclose = function(){ 
    };
	
	
	setInterval(getGameBoard, 500);

	$('button#resign').hide();
	

	/*
	var cw = $('.cell').width();
	$('.cell').css({'height':cw+'px'});
	*/
	
/*	$(window).resize(function() {
		changeCoordinatesOfCardsResize()
	});*/


	
	$('button#player1').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer1": true}
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			  
			});
			
	});
	$('button#player2').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer2": true}
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			  
			});
		/*
		if($(this).prop('disabled') && $('button#player1').prop('disabled')){
			$('button#startGame').prop('disabled',false);
		}
		*/
		
	});
	
	
	$('button#player3').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer3": true}
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			  
			});
	});
	$('button#player4').on('click', function() {
		$(this).prop('disabled',true);
		
		var data = {"buttonPlayer4": true}
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			  
			});
	});
	$('button#startGame').on('click', function() {
		$('button#startGame').prop('disabled',false);
		
		var ready = true
		var data = {"readyToPlay" : ready};
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			});
		
	});
	
	$('button#resign').on('click', function() {
		$('button#resign').prop('disabled',false);
		
		var resign = true
		var data = {"resign" : resign};
		
		$.post( "/bridgeStartGame/", data, function( json ) {
			$('button#resign').hide();
			});
		
	});

	
	/*
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
	*/
	
	
	$("button.auctionOptionPoints").on('click', function(event) {
		//if(auctionMove) {
			var value = $(this).text();
			console.log(value);
			pointsAuction = value;
			$("#auctionResult").html(pointsAuction + suitAuction);
			if(parseInt(pointsAuction)>pointsToGet && 
			(suitAuction=="C" || suitAuction=="D" || suitAuction=="H" || suitAuction =="S"
				|| suitAuction =="NT")){
				$('button#buttonOK').prop('disabled',false);
				
			}
			else if(parseInt(pointsAuction)==pointsToGet && suitGame != "NT" 
				&& (suitAuction> suitGame || suitAuction=="NT" )){
				$('button#buttonOK').prop('disabled',false);
			}
			else {
				$('button#buttonOK').prop('disabled',true);
			}
		//}
	});
	
	$("button.auctionOptionSuit").on('click', function(event) {
		//if(auctionMove) {
			var value = $(this).text();
			suitAuction = value;
			$("#auctionResult").html(pointsAuction + suitAuction);
			
			if(parseInt(pointsAuction)>pointsToGet && 
			(suitAuction=="C" || suitAuction=="D" || suitAuction=="H" || suitAuction =="S"
				|| suitAuction =="NT")){
				$('button#buttonOK').prop('disabled',false);
					
			}
			else if(parseInt(pointsAuction)==pointsToGet && suitGame != "NT" 
				&& (suitAuction> suitGame || suitAuction=="NT" )){
				$('button#buttonOK').prop('disabled',false);
			}
			else {
				$('button#buttonOK').prop('disabled',true);
			}
		//}
	});
	
	
	$("button#buttonOK").on('click', function(event) {
		
		var dataToSend = {};
		dataToSend.auctionMove = true;
		dataToSend.pointsAuction=pointsAuction;
		dataToSend.suitAuction = suitAuction;
		console.log(dataToSend)
		if(parseInt(pointsAuction)>pointsToGet && 
				(suitAuction=="C" || suitAuction=="D" || suitAuction=="H" || suitAuction =="S"
					|| suitAuction =="NT")){
			socket.send(JSON.stringify(dataToSend));
				
		}
		else if(parseInt(pointsAuction)==pointsToGet && suitGame != "NT" 
			&& (suitAuction> suitGame || suitAuction=="NT" )){
			socket.send(JSON.stringify(dataToSend));
		}
		
		$("#auctionResult").html("");
		$('#auctionButtons').hide();
		$('button#buttonOK').prop('disabled',true);
	});
	
	$("button#buttonPass").on('click', function(event) {
		var dataToSend = {};
		dataToSend.auctionMove = true;
		dataToSend.pass = true;
		socket.send(JSON.stringify(dataToSend));
		
		
		$("#auctionResult").html("");
		$('button#buttonOK').prop('disabled',true);
		$('#auctionButtons').hide();
	});
	
	// http://stackoverflow.com/questions/5014851/get-click-event-of-each-rectangle-inside-canvas
    canvas.addEventListener('click', function(e) {
    	
    	var x = (e.offsetX / $('#gameBridgeCanvas').width()) *1000;  
    	var y = (e.offsetY / $('#gameBridgeCanvas').height())*1000;  
    	
    	//var x = e.offsetX;
    	//var y = e.offsetY;
    	
        console.log('clickOffsetX: ' + e.offsetX + '/' + e.offsetY);
        console.log('clickOffResize: ' + x + '/' + y);
        var rect = collides(cards.my,x,y);
        if (rect) {
            console.log('collision: ' + rect.x + '/' + rect.y);
            var index = cards.my.indexOf(rect);
            if(index != -1)
                cards.my.splice( index, 1 );
            changeCoordinatesOfCards();
            console.log("here");
            drawElementsInCanvas();
            console.log(cards.my);
            
        } else {
            //console.log('no collision');
        }
        
        rect = collides(cards.teamMate, x,y);
        if (rect) {
            console.log('collision: ' + rect.x + '/' + rect.y);
        } else {
            //console.log('no collision');
        }
        
        rect = collides(cards.opponentFirst,x,y);
        if (rect) {
            console.log('collision: ' + rect.x + '/' + rect.y);
        } else {
            //console.log('no collision');
        }
        
        rect = collides(cards.opponentSecond,x,y);
        if (rect) {
            console.log('collision: ' + rect.x + '/' + rect.y);
        } else {
            //console.log('no collision');
        }
        
            
        
    }, false);
	
    
    function drawElementsInCanvas(){
    	context.clearRect(0, 0, canvas.width, canvas.height); 
    	
    	drawCardsRect();
        
    	context.fillStyle = "#000000";
        context.font = "30px Arial";
        context.textAlign="center"; 
        context.textBaseline = "middle";
        
        var bottomText = "South"
        
        var topText = "North";
        var leftText = "West";
        var rightText = "East";
        
        if(sideGame=="North"){
            bottomText = "North"
            topText = "South";
            leftText = "East";
            rightText = "West";
        }	
        else if(sideGame=="East"){
        	cards.mySide ="East";
            bottomText = "East";
            
            cards.teamMateSide="West"
            topText = "West";
            
            cards.opponentFirstSide="South"
            leftText = "South";
            rightText = "North";
        }	
        else if(sideGame=="West"){
            bottomText = "West"
            topText = "East";
            leftText = "North";
            rightText = "South";
        }	
        
        
        context.fillText(topText,canvas.width/2, 150);        	
        context.fillText(bottomText,canvas.width/2,canvas.height- 150);
        context.fillText(leftText,150,canvas.height/2);  
        context.fillText(rightText,canvas.width-150,canvas.height/2);
        
        
        context.fillText(pointsToGet.toString() + suitGame,canvas.width-50, 50);
        context.fillText(pointsTake.toString(),canvas.width-50, 100);
        
        
        context.fillStyle = "#000000";
        context.font = "14px Arial";
        context.textAlign="center"; 
        context.textBaseline = "middle";
        for(var i =0; i< cards.my.length; i++) {
        	if(cards.my[i].value<0) { 
        		context.fillText(cards.my[i].value.toString(),cards.my[i].x+(cards.my[i].width/2),cards.my[i].y+(cards.my[i].height/2));
        	}
        	else {
        		context.fillText(allCards[cards.my[i].value],cards.my[i].x+(cards.my[i].width/2),cards.my[i].y+(cards.my[i].height/2)); 		
        	}	
        }
        
        if(secondPlaying==cards.teamMateSide){
			for(var i=0; i< cards.teamMate.length;i++){
	        	context.fillText(allCards[cards.teamMate[i].value],cards.teamMate[i].x+(cards.teamMate[i].width/2),cards.teamMate[i].y+(cards.teamMate[i].height/2));
			}	        	
        }
        if(secondPlaying==cards.opponentFirstSide){
			for(var i=0; i< cards.opponentFirst.length;i++){
	        	context.fillText(allCards[cards.opponentFirst[i].value],cards.opponentFirst[i].x+(cards.opponentFirst[i].width/2),cards.opponentFirst[i].y+(cards.opponentFirst[i].height/2));
			}	        	
        }
        if(secondPlaying==cards.opponentSecondSide){
			for(var i=0; i< cards.opponentSecond.length;i++){
	        	context.fillText(allCards[cards.opponentSecond[i].value],cards.opponentSecond[i].x+(cards.opponentSecond[i].width/2),cards.opponentSecond[i].y+(cards.opponentSecond[i].height/2));
			}	        	
        }   

        
        
    }
    
    function drawCardsRect(){
        for (var i = 0, len = cards.my.length; i < len; i++) {
        	context.fillStyle = "#ffffff";
            context.fillRect(cards.my[i].x, cards.my[i].y, cards.my[i].width, cards.my[i].height);
          }

        for (var i = 0, len = cards.teamMate.length; i < len; i++) {
        	context.fillStyle = "#ffffff";
            context.fillRect(cards.teamMate[i].x, cards.teamMate[i].y, cards.teamMate[i].width, cards.teamMate[i].height);
          }

        for (var i = 0, len = cards.opponentFirst.length; i < len; i++) {
        	context.fillStyle = "#ffffff";
            context.fillRect(cards.opponentFirst[i].x, cards.opponentFirst[i].y, cards.opponentFirst[i].width, cards.opponentFirst[i].height);
          }
        for (var i = 0, len = cards.opponentSecond.length; i < len; i++) {
        	context.fillStyle = "#ffffff";
            context.fillRect(cards.opponentSecond[i].x, cards.opponentSecond[i].y, cards.opponentSecond[i].width, cards.opponentSecond[i].height);
          }        
    	
    }
    
    
    function coordinatesOfCards(){
        for (var i=0, len=13; i<len; i++){
        	cards.my.push(
        		{x: (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i, y: canvas.height - 100, width: 50, height: 80, value: -1}
        	);
        	cards.teamMate.push(
            		{x: (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i, y: 20, width: 50, height: 80, value:-1}
            );
        	cards.opponentFirst.push(
            		{x: 20, y: (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i, width: 80, height: 50, value: -1}
            );
        	cards.opponentSecond.push(
            		{x: canvas.width - 100, y: (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i, width: 80, height: 50, value: -1}
            );
        	
        }
        
    }

    
    function changeCoordinatesOfCards(){
    	
    	console.log("i am in change");
        for (var i=0, len=cards.my.length; i<len; i++){
        	console.log("i am in for");
        	console.log(len);
        	cards.my[i].x = (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i;
        	cards.my[i].y = canvas.height - 100;
        }
        for (var i=0, len=cards.teamMate.length; i<len ; i++){
        	cards.teamMate[i].x = (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i;
        	cards.teamMate[i].y = 20;
        }
        for (var i=0, len = cards.opponentFirst.length; i<len; i++){
        	cards.opponentFirst[i].x = 20;
        	cards.opponentFirst[i].y = (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i;
        }
        for (var i=0, len = cards.opponentSecond.length; i<len; i++){
        	cards.opponentSecond[i].x = canvas.width - 100;
        	cards.opponentSecond[i].y = (canvas.width/2) - (50/2) - (len/2)*50 + 5*i +50*i;
        }
        
    }    
    
});

// http://stackoverflow.com/questions/5014851/get-click-event-of-each-rectangle-inside-canvas
//function collides(rects, x, y) {
//    var isCollision = false;
//    for (var i = 0, len = rects.length; i < len; i++) {
//        var left = rects[i].x, right = rects[i].x+rects[i].width;
//        var top = rects[i].y, bottom = rects[i].y+rects[i].height;
//        if ((left + right) >= x
//            && left <= x
//            && (top + bottom) >= y
//            && top <= y)  {
//            isCollision = rects[i];
//        }
//    }
//    return isCollision;
//}

//http://stackoverflow.com/questions/5014851/get-click-event-of-each-rectangle-inside-canvas
function collides(rects, x, y) {
    var isCollision = false;
    for (var i = 0, len = rects.length; i < len; i++) {
        var left = rects[i].x, right = rects[i].x+rects[i].width;
        var top = rects[i].y, bottom = rects[i].y+rects[i].height;
        if (right >= x
            && left <= x
            && bottom >= y
            && top <= y) {
            isCollision = rects[i];
        }
    }
    return isCollision;
}







function sendDataGameBoard(){
	$.post( "/bridgeStartGame/", data, function( json ) {
	});
}

function getGameBoard(){
    $.get('/bridgeGameBoard/', function(json){
    	
    
    	if(json.hasOwnProperty('namePlayer1'))
    		$('button#player1').html(json.namePlayer1);
    	
    	if(json.hasOwnProperty('namePlayer2'))
    		$('button#player2').html(json.namePlayer2);
    	
    	if(json.hasOwnProperty('namePlayer3'))
    		$('button#player3').html(json.namePlayer3);
    	
    	if(json.hasOwnProperty('namePlayer4'))
    		$('button#player4').html(json.namePlayer4);
    	
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
    	if(json.hasOwnProperty('player3Button')){
    	    if (json.player3Button){
    	    	$('button#player3').prop('disabled',false);
    	    }
    	    else {
    	    	$('button#player3').prop('disabled',true);
    	    }
    	}
    	if(json.hasOwnProperty('player4Button')){
    	    if (json.player4Button){
    	    	$('button#player4').prop('disabled',false);
    	    }
    	    else {
    	    	$('button#player4').prop('disabled',true);
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