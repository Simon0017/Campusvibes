// spaceChat.js to control and connect the webScoket for the group discussion
console.log('Sanity check from spaceChat.js');

// defining of the variables 
const roomId = JSON.parse(document.getElementById('roomId').textContent);
const username = JSON.parse(document.getElementById('username').textContent); //from views.py
const admin = JSON.parse(document.getElementById('admin').textContent); //from views.py
let chatSocket = null;
let chatInput = document.querySelector('#message');
let chatMessageSend =document.querySelector('#chatSend');
console.log(roomId);
console.log(username);
console.log(admin);

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
    chatInput.focus();
};

// function to add the messages to the chat history
function GroupMessage(message,sender){
    const chatHistory = document.querySelector('.chat');
    const MessageContainer = document.createElement('li');

    const msg = document.createElement('div');
    msg.classList.add('msg');

    const mess = document.createElement('p');
    mess.textContent = message;

    const user = document.createElement('div');

    const adminSpan = document.createElement('span');

    const time = document.createElement('time');
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

    if (sender === username ){
        MessageContainer.classList.add('self');
        
    }else{
        MessageContainer.classList.add('other');
        user.classList.add('user');
        user.textContent = sender;
    }
    
    if (admin.includes(sender)){
        adminSpan.classList.add('range','admin');
        adminSpan.textContent = 'Admin';
    }


    chatHistory.appendChild(MessageContainer);
    MessageContainer.appendChild(msg);
    msg.appendChild(user);
    msg.appendChild(mess);
    msg.appendChild(time);
    user.appendChild(adminSpan);

    // scroll to last message
    MessageContainer.scrollIntoView({behavior:'instant',block:'start'});
}

// function to add the messages to the chat history retrieved from the database
function GroupMessage_2(message,sender,timer){
    const chatHistory = document.querySelector('.chat');
    const MessageContainer = document.createElement('li');

    const msg = document.createElement('div');
    msg.classList.add('msg');

    const mess = document.createElement('p');
    mess.textContent = message;

    const user = document.createElement('div');

    const adminSpan = document.createElement('span');

    const time = document.createElement('time');
    time.textContent = timer;

    if (sender === username ){
        MessageContainer.classList.add('self');
        
    }else{
        MessageContainer.classList.add('other');
        user.classList.add('user');
        user.textContent = sender;
    }
    
    if (admin.includes(sender)){
        adminSpan.classList.add('range','admin');
        adminSpan.textContent = 'Admin';
    }

    chatHistory.appendChild(MessageContainer);
    MessageContainer.appendChild(msg);
    msg.appendChild(user);
    msg.appendChild(mess);
    msg.appendChild(time);
    user.appendChild(adminSpan);

    // scroll to last message
    MessageContainer.scrollIntoView({behavior:'instant',block:'start'});
}


// connect to the websocket
function connect(){
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/Users/space/" + roomId + "/")
    
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
            case "groupMessage":
                GroupMessage(data.message,data.user);
                break;
            case "chat_history":
                for (let i = 0; i < data.message.length; i++) {
                    GroupMessage_2(data.message[i].content, data.message[i].user,data.message[i].timestamp)
                }
                break;
            default:
                break;
        }
    }
}

connect();

