// chatRoom.js
console.log("sanity check from chatRoom.html");

const roomName = JSON.parse(document.getElementById('roomName').textContent);
let chatSocket = null
let chatInput  = document.querySelector('#message');
let chatMessageSend =document.querySelector('#chatSend');

console.log(roomName);
chatInput.focus();

// submit if the user presses the enter key
chatInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatInput.value,
    }));
    chatInput.value = "";
};

function connect(){
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/Users/chat_room/" + roomName + "/")
    
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
    chatSocket.onmessage = function(e){
        const data = JSON.parse(e.data);
        console.log(data)
        switch (data.type) {
            case "chat_message":
                
                break;
        
            default:
                break;
        }
    }
}

connect();