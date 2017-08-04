$( document ).ready(function() {
	
	var socket = new WebSocket("ws://" + window.location.host + "/bridge/");

	socket.onopen = function() {
	}
	if (socket.readyState == WebSocket.OPEN) socket.onopen();
	socket.onmessage = function(e) {
		var json = JSON.parse(e.data);
		if(json.hasOwnProperty('playersOnlineHtml'))
			$('#playersOnline').html(json.playersOnlineHtml);
		if(json.hasOwnProperty('bridgeRoomsHtml'))
			$('#rooms').html(json.bridgeRoomsHtml);
		console.log(e.data);
        
		//socket.send(JSON.stringify(data));	    
	}
    socket.onclose = function(){ 
    };	
	
	//setInterval(getPlayers, 500);


    
});

function getPlayers(){
    $.get('/gomokuRooms/', function(message){
        $('#rooms').html(message);
    });

    $.get('/gomokuPlayers/', function(message){
        $('#playersOnline').html(message);
    });

}