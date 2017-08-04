$(document).ready(function() {

    $('#all-message').on('scroll', function(){
        scrolling = true;
    });
    setInterval(getMessages, 500);	
	
     $('#send-chat').prop('disabled',true);
     $('#message-to-send').keyup(function() {
        if($(this).val() != '') {
           $('#send-chat').prop('disabled',false);
        }
        else {
        $('#send-chat').prop('disabled',true);
        }
     });
 });


var scrolling = false;

$('#form-to-send-data').on('submit', function(event){
    event.preventDefault();
    data = { "msgbox" : $('#message-to-send').val() }
	$.post( "/addMessagesToChat/", data, function( json ) {
        $('#message-to-send').val('');
        var chatlist = document.getElementById('all-message');
        chatlist.scrollTop = chatlist.scrollHeight;		
	})
});

function getMessages(){
    if (!scrolling) {
        $.get('/getMessagesFromChat/', function(messages){
            $('#message-list').html(messages);
            var chatlist = document.getElementById('all-message');
            chatlist.scrollTop = chatlist.scrollHeight;
        });
    }
    scrolling = false;
}

