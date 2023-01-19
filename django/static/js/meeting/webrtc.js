const stunServerConfiguration = {
    "iceServers": [{
            "urls": "stun:stun.l.google.com:19302"
        },
        // public turn server from https://gist.github.com/sagivo/3a4b2f2c7ac6e1b5267c2f1f59ac6c6b
        // set your own servers here
        {
            url: 'turn:192.158.29.39:3478?transport=udp',
            credential: 'JZEOEt2V3Qb0y27GRntt2u2PAYA=',
            username: '28224511:1379330808'
        }
    ]
}

// WebRTC

let peers = {};

const offerOption = {
    offerToReceiveAudio: 1,
    offerToReceiveVideo: 1,
}

async function handleNegotiationNeeded(desc, id) {
    // desc 就是 offer 的 description、id 則是與對方連線的 id

    // when set local description, will trigger onicecandidate event, id is others id, not myself
    await peers[id].setLocalDescription(desc);

    // 傳對方的 id，因為要告知 signaling server 使用對方的 websocket 物件傳到對方那邊
    console.log("sending offer...")
    sendSDP("offer", peers[id].localDescription, id);

}

function sendSDP(type, sdp, session_id) {
    socket.send(JSON.stringify({
        "type": type,
        "signal": sdp,
        "session_id": session_id
    }))
}

async function createAnswer(id) {
    // 對方的 id

    answer = await peers[id].createAnswer();

    await peers[id].setLocalDescription(answer);

    sendSDP("answer", answer, id);
}

function sendIceCandidate(event, session_id) {
    if ( event.candidate ) {
        socket.send(JSON.stringify({
            "type": "icecandidate",
            "candidate": event.candidate,
            "session_id": session_id
        }))
    }
}

class WebRTC {
    static setLocalVideoId(session_id) {
        localVideo.setAttribute("id", session_id);
    }

    static async createP2PConnection(session_id, sessions) {
        // session_id 是自己，sessions 是房間的全部人 ids

        console.log("開始建立 P2P Connection...");

        for ( const [key, id] of Object.entries(sessions) ) {
            if ( id == session_id ) {
                continue
            }
            
            // 注意這個 peers[id] 不是自己，都入加入房間的其他人
            if (!peers[id]) {

                peers[id] = new RTCPeerConnection(stunServerConfiguration);

                // 把新進的人建立的 peer 加入舊的自己的媒體流
                // if ( window.stream != undefined ) {

                //     peers[id].addStream(window.stream);
                // }

                // peers[id].onaddtrack = (event) => {
                //     console.log("onaddtrack", event)
                // }
                
                // 這邊如果不執行，對方就無法觸發 ontrack
                await window.stream.getTracks().forEach( track => peers[id].addTrack(track, window.stream))
    
                peers[id].ontrack = ( event ) => {
                    if ( !document.getElementById(id) ) {
                        const div = document.createElement("div");
                        const remoteVideo = document.createElement("video");

                        if (remoteVideo.srcObject !== event.streams[0]) {
                    
                            remoteVideo.srcObject = event.streams[0];
                            remoteVideo.setAttribute('playsinline', true);
                            remoteVideo.setAttribute("class", "max-w-full h-auto rounded-lg");
                            remoteVideo.autoplay = true;

                            let newMicButton = `
                                <div class="removeMicBtn">
                                    <img class="roomMicIcon" src="/static/icons/mic.png" />
                                </div>`

                            div.insertAdjacentHTML('beforeend', newMicButton)
                            div.append(remoteVideo);
                            
                            div.id = id;
                            div.classList.add("videoBlock");
                            remoteVideoArea.append(div);
                        }
                    }
                }
    
                // this won't be trigger immediately until peer.setLocalDescription trigger
                peers[id].onicecandidate = ( event ) => {
                    sendIceCandidate(event, session_id)
                }
                
                // 後加入房間的人送 offer
                if ( sessions[sessions.length - 1] == session_id ) {
                    console.log("create offer...")
                    peers[id].createOffer({
                        offerToReceiveAudio: 1,
                        offerToReceiveVideo: 1,
                    })
                    .then( desc => {
                        handleNegotiationNeeded(desc, id)
                    })
                }

            }
        }

    }

    static async createP2PShareVideoConnection() {
        console.log("share connection start...")
    }

    static async handleComingIceCandidate(event, session_id) {
        await peers[session_id].addIceCandidate(event);
    }

    static async handleSDPOffer(desc, session_id) {
        // desc 是 offer description，session_id 是對方的 id
    
        await peers[session_id].setRemoteDescription(desc);

        // others session id
        console.log("create answer...")
        await createAnswer(session_id)
    }

    static async hanldeSDPAnswer(desc, session_id) {
        // desc 是 answer description，session_id 是對方的 id

        console.log(`新來的返回 answer 了... ${session_id}`)
        await peers[session_id].setRemoteDescription(desc);
    }

    static handleDisconnectRoom(session_id) {
        delete peers[session_id]
    }

    static handleDeleteRemoteVideo(session_id) {

        try {
            const remoteVideoBlock = document.getElementById(session_id);
            remoteVideoArea.removeChild(remoteVideoBlock);
        
        } catch ( error ) {
            console.error(error)
        }

    }
}

document.addEventListener("DOMContentLoaded", async () => {
    // navigator.mediaDevices.enumerateDevices().then(retrieveDevices)
    // videoSelect.onchange = captureLocalVideoStream()
    // 只要切換音訊輸入裝置觸發重新抓取 local stream 的動作
    if ( window.stream === undefined ) {
        console.log("capture local video stream...")

        socket.onopen = async (e) => {
            await captureLocalVideoStream()

            socket.send(JSON.stringify({
                "type": "join"
            }))

        }
        const status = await navigator.permissions.query({name: "camera"});
        status.addEventListener("change", async (event) => {
            await captureLocalVideoStream();

            if ( event.currentTarget.state == "denied") {
                micBtn.style.backgroundColor = forbidColor;
                cameraBtn.style.backgroundColor = forbidColor;
            } else {
                micBtn.style.backgroundColor = allowColor;
                cameraBtn.style.backgroundColor = allowColor;
            }

        });

    }

    new WebRTC();
})
