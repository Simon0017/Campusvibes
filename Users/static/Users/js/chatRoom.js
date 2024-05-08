// chatRoom.js
console.log("sanity check from chatRoom.html");

// define the variable and debug from the console
const roomName = JSON.parse(document.getElementById('roomName').textContent);
const roomId = JSON.parse(document.getElementById('roomId').textContent);
let chatSocket = null;
let chatInput  = document.querySelector('#message');
let chatMessageSend =document.querySelector('#chatSend');
const username = JSON.parse(document.getElementById('username').textContent); //from views.py
console.log(roomId);
console.log(username);
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
        'username':username,
    }));
    chatInput.value = "";
};


// add active if the room is active



// function to display the messages 
function addMessageToChatHistory(message,sender) {
    const chatHistory = document.querySelector('.container-two ul');
    
    const messageItem = document.createElement('li');
    messageItem.classList.add('message');

    const time = document.createElement('p');
    time.classList.add('time');
    const timeSpec = new Date();
    var hr = timeSpec.getHours();
    var min = timeSpec.getMinutes();
    // tail is the AM or PM
    var tail = '';
    if (hr>=12){
        tail = 'PM';
        hr -=12;
    }else{
        tail = 'AM';
    }

    if (min < 10){
        min = '0'+ min;
    }

    time.textContent = hr + ':' + min + '' + tail;
    
    const messageData = document.createElement('div');

    const avatar = document.createElement('img');

    
    if (sender === username) {
        time.classList.add('time-rg')
        messageData.classList.add('float-rg');
    }else {
        messageData.classList.add('float-lf');
        avatar.classList.add('avatar');
        avatar.src = "{% static'Users/images/simon.jpg' %}";
        avatar.alt = '';
    }
    messageData.textContent = message;
    
    messageItem.appendChild(time);
    // messageItem.appendChild(messageContent);
    messageItem.appendChild(messageData);
    
    chatHistory.appendChild(messageItem);

    // scroll to last message
    messageItem.scrollIntoView({behavior:'instant',block:'start'});
}

// function to display the chat_history
function addMessageToChatHistory_2(message,sender,timer) {
    const chatHistory = document.querySelector('.container-two ul');
    
    const messageItem = document.createElement('li');
    messageItem.classList.add('message');

    const time = document.createElement('p');
    time.classList.add('time');
    time.textContent = timer;
    
    const messageData = document.createElement('div');

    const avatar = document.createElement('img');

    
    if (sender === username) {
        time.classList.add('time-rg')
        messageData.classList.add('float-rg');
    }else {
        messageData.classList.add('float-lf');
        avatar.classList.add('avatar');
        avatar.src = "{% static'Users/images/simon.jpg' %}";
        avatar.alt = '';
    }
    messageData.textContent = message;
    
    messageItem.appendChild(time);
    // messageItem.appendChild(messageContent);
    messageItem.appendChild(messageData);
    
    chatHistory.appendChild(messageItem);
    
    // scroll to last message
    messageItem.scrollIntoView({behavior:'instant',block:'start'});
}

function connect(){
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/Users/chat_room/" + roomId + "/")
    
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
                addMessageToChatHistory(data.message,data.user);
                break;
            case "chat_history":
                for (let i = 0; i < data.message.length; i++) {
                    addMessageToChatHistory_2(data.message[i].content, data.message[i].user,data.message[i].timestamp);
                }
                break;
            default:
                break;
        }
    }
}

connect();