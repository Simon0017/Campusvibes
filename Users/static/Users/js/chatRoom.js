console.log("sanity check from chatRoom.html");

let chatSocket = null

function connect(){
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/Users/chat")
    
    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };
}
