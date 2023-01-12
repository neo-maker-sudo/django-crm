

const localVideo = document.querySelector(".localVideo");
const replayVideo = document.getElementById("replayVideo");
const shareVideo = document.getElementById("shareVideo");
const videoSelect = document.getElementById("videoSource");

const cameraBtn = document.getElementById('cameraBtn');
const micBtn = document.getElementById("micBtn");

const audioInputSelect = document.getElementById("audioSource");
const audioOutputSelect = document.getElementById("audioOutput");

const stopAudioBtn = document.getElementById("stopAudio");
const captureAudioBtn = document.getElementById("captureAudio");

const captureScreenShotBtn = document.getElementById("captureScreenShot");

const selectors = [audioInputSelect, audioOutputSelect, videoSelect]

const filtersSelect = document.querySelector('select#filter');

const videoRecordBtn = document.getElementById("videoRecord");
const videoReplayBtn = document.getElementById("videoReplay");
const videoDownloadBtn = document.getElementById("videoDownload");

const shareScreenBtn = document.getElementById("shareScreen");

const sideBar = document.querySelector(".sidebar");
const sideBarToggle = document.getElementById("sidebarToggle");
const sidebarClose = document.getElementById("sidebarClose");

const chatArea = document.getElementById("chatArea");
const roomChatIcon = document.getElementById("roomChatIcon");

roomChatIcon.onclick = () => {
    if ( !chatArea.classList.contains("showChatArea")) {
        chatArea.classList.add("showChatArea");
        // localVideo.classList.remove("localVideoWidth");
        videoArea.style.width = "75%";
        // videoArea.classList.add("videoAreaWidth");
    } else {
        chatArea.classList.remove("showChatArea");
        // localVideo.classList.add("localVideoWidth");
        // videoArea.classList.remove("videoAreaWidth");
        videoArea.style.width = "100%";
    }
}

let buffer = [];
let mediaRecorder;

const videoRecordOptions = {
    mimeType: "video/webm;codecs=vp8"
}

// audioOutputSelect.disabled = !('sinkId' in HTMLMediaElement.prototype)

function retrieveDevices(devicesInfo) {
    // if select has child, wipe all of elements out
    const selectValues = selectors.map( select => {
        if ( select.hasChildNodes() ) {
            while (select.firstChild) {
                select.removeChild(select.firstChild)
            }
        }
        return select.value
    })

    for (let deviceInfo of devicesInfo) {

        const option = document.createElement("option");
        
        // 將裝置的 id 設定給每個 option，切換輸出裝置時可以取得裝置 id 並切換裝置
        option.value = deviceInfo.deviceId

        if ( deviceInfo.kind == "audioinput" ) {
            option.text = deviceInfo.label || `microphone ${audioInputSelect.length + 1}`
            audioInputSelect.appendChild(option)
        } else if ( deviceInfo.kind == "audiooutput" ) {
            option.text = deviceInfo.label || `speaker ${audioOutputSelect.length + 1}`
            audioOutputSelect.appendChild(option)
        } else if ( deviceInfo.kind == "videoinput" ) {
            option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`
            videoSelect.appendChild(option)
        } else {
            console.log("what the fuck is this device ", deviceInfo)
        }
    }

    // 如果觸發的話，輸入裝置的 select value 為空
    selectors.forEach( ( select, index ) => {
        // 如果 select 裡面的 option 只要有一個裝置的 id 為空，就將 select 的 value 設為空
        if ( 
            Array.prototype.slice
            .call(select.childNodes)
            .some( option => option.value === selectValues[index] )
        ) {
            select.value = selectValues[index]
        }
    });
}

function handleLocalMediaStreamError(error) {
    if ( error ) {
        alert("請操作瀏覽器授權存取你的攝影機，並重新整理")
    }

    console.error("getUserMedia error:", error)
}

// ========  取得視訊媒體流
function retrieveLocalMediaStream(mediaStream) {
    window.stream = mediaStream

    if ("srcObject" in localVideo) {
        localVideo.srcObject = mediaStream;
    } else {
        localVideo.src = window.URL.createObjectURL(mediaStream);
    }

    return navigator.mediaDevices.enumerateDevices()
}
// ========

// ========  開啟視訊
async function captureLocalVideoStream() {
    const audioSource = audioInputSelect.value
    const videoSource = videoSelect.value

    const mediaStreamConstraints = {
        "video": {
            "width": {min:640, ideal:1920, max:1920},
            "height": {min:480, ideal:1080, max:1080},
            "deviceId": videoSource ? { exact: videoSource } : undefined
        },
        // 音訊輸入
        "audio": {
            "deviceId": audioSource ? { exact: audioSource } : undefined
        },
    }

    // ask client user whether grant video/audio streaming authorization or not.
    await navigator.mediaDevices.getUserMedia(mediaStreamConstraints)
    .then(retrieveLocalMediaStream)
    .then(retrieveDevices)
    .catch(handleLocalMediaStreamError)
}
cameraBtn.onclick = () => {
    let videoTrack = window.stream.getTracks().find(track => track.kind === 'video')

    if(videoTrack.enabled){
        videoTrack.enabled = false
        cameraBtn.style.backgroundColor = 'rgb(255, 80, 80)'
    }else{
        videoTrack.enabled = true
        cameraBtn.style.backgroundColor = '#363739'
    }

}
// ========

micBtn.onclick = () => {
    let audioTrack = window.stream.getTracks().find(track => track.kind === 'audio')

    if(audioTrack.enabled){
        audioTrack.enabled = false
        micBtn.style.backgroundColor = 'rgb(255, 80, 80)'
    }else{
        audioTrack.enabled = true
        micBtn.style.backgroundColor = '#363739'
    }
}


// // ========  取得分享畫面媒體流
// function retrieveShareMediaStream(mediaStream) {
//     const shareStream = mediaStream;

//     if ("srcObject" in shareVideo) {
//         shareVideo.srcObject = shareStream;
//     } else {
//         shareVideo.src = window.URL.createObjectURL(mediaStream);
//     }

//     window.shareStream = shareStream;
// }
// // ========

// // ========  分享畫面
// async function shareLocalVideoStream() {
//     const shareConstraints = {
//         frameRate: 15,
//         width: 640,
//     }

//     // ask client user whether grant video/audio streaming authorization or not.
//     navigator.mediaDevices.getDisplayMedia(shareConstraints)
//     .then(retrieveShareMediaStream)
//     .catch(handleLocalMediaStreamError)
// }
// shareScreenBtn.onclick = shareLocalVideoStream
// // ========  

// // ========  切換輸出裝置
// function swapAudioOutputDevice() {
//     if ( typeof localVideo.sinkId !== 'undefined') {
//         // video 設定選擇好的裝置 id
//         localVideo.setSinkId(audioOutputSelect.value)
//         .then( () => {
//             console.log(`audio output device attached ${audioOutputSelect.value}`)
//         })
//         .catch((error) => {
//             let errorMessage = error
//             if (error.name === 'SecurityError') {
//                 errorMessage = `You need to use HTTPS for selecting audio output device: ${error}`
//             }
//             console.error(errorMessage)
//             // Jump back to first output device in the list as it's the default.
//             audioOutputSelect.selectedIndex = 0
//         })
//     }

// }
// // ========

// // ======== 截圖
// function downloadScreenShot(url) {
//     const a = document.createElement("a");

//     a.download = "Image.jpg"
//     a.href = url

//     document.body.appendChild(a);
//     a.click();
//     a.remove();
// }
// captureScreenShotBtn.onclick = () => {
//     const vw = localVideo.videoWidth
//     const vh = localVideo.videoHeight

//     const canvas = document.createElement("canvas");

//     canvas.width = vw
//     canvas.height = vh

//     const ctx = canvas.getContext("2d");

//     // WIP, dynamic loading filter effects if turn on filter
//     ctx.filter = "sepia(0.8)"
//     ctx.drawImage(localVideo, 0, 0, vw, vh)

//     const canvas_url = canvas.toDataURL("image/jpeg");
    
//     downloadScreenShot(canvas_url);
    
// }
// // ========

// // ======== 開始與停止錄影
// function startVideoRecord() {
//     buffer = [];

//     if(!MediaRecorder.isTypeSupported(videoRecordOptions.mimeType)) {
//         alert(`${videoRecordOptions.mimeType} is not supported`)
//         return
//     }

//     try {
//         if ( mediaRecorder == undefined ) {
//             mediaRecorder = new MediaRecorder(window.stream, videoRecordOptions);
//         }

//     } catch ( error ) {
//         alert(`failed to create MediaRecorder`, e)
//         return
//     }

//     // here will keep accepting video stream data
//     mediaRecorder.ondataavailable = (e) => {
//         buffer.push(e.data)
//     }
//     mediaRecorder.start(10)

// }

// function stopVideoRecord() {
//     // cut accepting vidfeo stream data
//     mediaRecorder.stop();
// }

// videoRecordBtn.onclick = (e) => {
//     if (e.target.dataset.record.toLowerCase() == "false") {
//         startVideoRecord()
//         videoRecordBtn.textContent = "停止"
//         e.target.dataset.record = "true"
//         videoReplayBtn.disabled = true
//         videoDownloadBtn.disabled = true

//         localVideo.classList.add("record-border");
//     } else {
//         stopVideoRecord()
//         videoRecordBtn.textContent = "錄影"
//         e.target.dataset.record = "false"
//         videoReplayBtn.disabled = false
//         videoDownloadBtn.disabled = false
//         localVideo.classList.remove("record-border");
//     }
// }
// // ========

// // ========  關閉視訊
// function stopLocalMediaStream () {
//     if ( window.stream ) {
//         const localStream = window.stream.getVideoTracks();

//         localStream.forEach(stream => {
//             stream.stop();
//         });

//         localVideo.srcObject = null;
//         window.stream = undefined;
//     }
// }
// // ========  

// // ======== 開始麥克風
// captureAudioBtn.onclick = () => {
//     window.stream.getAudioTracks()[0].enabled = true;
// }
// // ========

// // ======== 關閉麥克風
// stopAudioBtn.onclick = () => {
//     window.stream.getAudioTracks()[0].enabled = false;
// }
// // ========

// // ======== 錄影回放
// videoReplayBtn.onclick = () => {
//     let blob = new Blob(buffer, { type: "video/webm" })

//     replayVideo.src = window.URL.createObjectURL(blob);
//     replayVideo.srcObject = null;
//     replayVideo.controls = true;
//     replayVideo.play();
// }
// // ========

// // ======== 視訊濾鏡 css
// function swapLocalVideoFilter() {
//     for ( let child of filtersSelect.children) {
//         if ( localVideo.classList.contains(child.value) ) {
//             localVideo.classList.remove(child.value)
//         }

//     }

//     localVideo.classList.add(filtersSelect.value)

// }
// // ========

// // ========  下載錄影 video
// function downloadRecordVideo(blob) {
//     let url = window.URL.createObjectURL(blob);
//     const a = document.createElement("a");

//     a.href = url

//     a.download = "video.webm"
//     a.click();

// }
// videoDownloadBtn.onclick = () => {
//     let blob = new Blob(buffer, { type: "video/webm" });

//     downloadRecordVideo(blob);
// }
// // ========

// // ======== 側邊攔閉合
// sideBarToggle.onclick = () => {
//     sideBar.classList.toggle("show-sidebar");
// }

// sidebarClose.onclick = () => {
//     sideBar.classList.remove("show-sidebar");
// }
// // ========

// audioInputSelect.onchange = captureLocalVideoStream

// audioOutputSelect.onchange = swapAudioOutputDevice
// // 只要切換視訊裝置觸發重新抓取 local stream 的動作
// videoSelect.onchange = captureLocalVideoStream

// filtersSelect.onchange = swapLocalVideoFilter