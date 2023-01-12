let socket;
let roomName = document.getElementById('room-name');
const chatTextarea = document.getElementById("chatTextarea");
const messageInput = document.getElementById("messageInput");
const messageSubmitBtn = document.getElementById("messageSubmit");
const dropdownMenuBtn = document.getElementById("dropdownMenu");

roomName = JSON.parse(roomName.textContent);

const ws = (window.location.protocol === 'https:') ? 'wss://' : 'ws://';

socket = new WebSocket(
    ws
    + window.location.host
    + '/ws/meeting/'
    + roomName
    + '/'
);

function addMessageToDom(name, message) {
    let newMessage = `<div class="message__wrapper">
                        <div class="message__body">
                            <strong class="message__author">${name}</strong>
                            <p class="message__text">${message}</p>
                        </div>
                    </div>`

    chatTextarea.insertAdjacentHTML('beforeend', newMessage)

    let lastMessage = document.querySelector('#messages .message__wrapper:last-child')
    if( lastMessage ){
        lastMessage.scrollIntoView()
    }
}

function addBotMessageToDom(botMessage) {
    let newMessage = `<div class="message__wrapper">
                        <div class="message__body__bot">
                            <strong class="message__author__bot">🤖 Robot</strong>
                            <p class="message__text__bot">${botMessage}</p>
                        </div>
                    </div>`

    chatTextarea.insertAdjacentHTML('beforeend', newMessage)

    let lastMessage = document.querySelector('#messages .message__wrapper:last-child')
    if(lastMessage){
        lastMessage.scrollIntoView()
    }
}

socket.onmessage = (e) => {
    const data = JSON.parse(e.data);

    if ( data.type == "join") {
        addBotMessageToDom(`Welcome ${data.username} joined room`);

        if ( data.totals > 1 ) {
            // session_id 是自己，sessions 是房間的全部人
            WebRTC.createP2PConnection(data.session_id, data.sessions);
        }

    } else if ( data.type == "chatting" ) {
        addMessageToDom(data.username, data.message);
    } else if ( data.type == "candidate" ) {
        if ( data.candidate != null ) {
            WebRTC.handleComingIceCandidate(data.candidate, data.session_id);
        }
    } else if ( data.type == "offer" ) {
        WebRTC.handleSDPOffer(data.message, data.session_id);
    } else if ( data.type == "answer" ) {
        WebRTC.hanldeSDPAnswer(data.message, data.session_id);
    } else if ( data.type == "disconnect" ) {
        WebRTC.handleDisconnectRoom(data.session_id);

        addBotMessageToDom(`${data.username} has left room`);

        WebRTC.handleDeleteRemoteVideo(data.session_id)
    }
}

socket.onclose = (e) => {
    alert("聊天室已關閉，若要使用請重新整理瀏覽器");
}

messageSubmitBtn.onclick = (e) => {
    const message = messageInput.value;

    socket.send(JSON.stringify({
        "type": "chatting",
        'message': message,
        "username": dropdownMenuBtn.dataset.username
    }));

    messageInput.value = '';
}