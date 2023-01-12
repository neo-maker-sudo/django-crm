# django-crm


### WebRTC 流程

1. 一開始進入房間先跟後端連線 websocket。**websocket.js line 10**

2. 後端 client 加入房間，並把 websocket 物件加入到 memory，像是 redis 或是 runtime memory。**consumers.py line 15**

3. 詢問是否開啟視訊 ( 本地媒體流 )。**webrtc.js line 148**

4. 獲取完媒體流會直接使用 websocket 傳送加入房間的 message。**entrance.js line 128**

5. 後端收到之後回傳房間相關資訊給前端。**consumers.py line 47、consumers.py line 94**
    - 房間目前有幾人
    - 目前這位連線的 client sessionid
    - 以及目前房間所有人的 session_id

6. 前端收到後先判斷房間人數，如果只有一個人就不做任何動作，到這邊為止，超過一人的話，前端呼叫建立 p2p 連線 function 並傳入兩個參數。**websocket.js line 24**
    - 目前連線該 client 的 sessionid
    - 房間裡面目前全部人的 ids ( sessions )

7. 這邊簡化以 A、B 為範例，假設 A 是第一個進入房間的，B 是第二個，兩個仁都會收到 websocket 加入房間的 message，主要的差異在於新加入房間的人會 create offer。
    - for loop 房間的 ids ( sessions )，判斷如果 loop 裡面的 id 是等同於剛傳入的第一個參數，代表就是自己的 id，那就將 id 設為本地 local video 的 id 值，並結束動作，而如果 id 是其他人的話 **webrtc.js line 74**
    - 判斷 id 是否在 peers 的物件裡面 ( 並免重覆加入 ) **webrtc.js line 81**
    - 實例化 p2p object，並存入 peers 物件 **webrtc.js line 83**
    - 將本地媒體流加入 p2p object **webrtc.js line 86**
    - p2p object 套用 ontrack 傾聽事件，一但連線成功，calling callback function **webrtc.js line 90**
    - p2p object 套用 oncandidate 傾聽事件，一但 create offer 設定 localdescription ( 就是新加入房間的人 ) 就會被直接觸發，並透過 websocket 傳送 candidate，並將候選人以及自己的 session id 傳到後端 **webrtc.js line 107**
    - B 使用之前加入房間每個人的 peers 物件 create offer ( 因為 B 是後加入房間的人 ) **webrtc.js line 112**
    - 呼叫 handleNegotiationNeeded，設定 setLocalDescription，發送 offer 與 A 的 id 給 signaling server **webrtc.js line 119**
    - singaling server 收到後，透過收到的 id，傳到 A 端，內容包含 B 的 id，以便讓 A 可以 setRemoteDescription **consumers.py line 72**
    - A 端收到後，設定 setRemoteDescription，create answer **webrtc.js line 130**
    - A 端 setLocalDescription，發送 answer 與 B 的 id 給 signaling server **webrtc.js line 47**
    - singaling server 收到後，透過收到的 id，傳到 B 端，內容包含 A 的 id，以便讓 B 可以 setRemoteDescription **consumers.py line 78**
    - B 端 setRemoteDescription **webrtc.js line 142**
