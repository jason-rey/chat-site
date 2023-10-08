const socket = new WebSocket("ws://35.247.117.41:5473")
let username = localStorage.getItem("username");
// let sessionID = localStorage.getItem("sessionID");

socket.onopen = () => socket.send(username);

let currentRoom = "";
sendMessage("get_rooms|");

document.getElementById("createRoom").addEventListener("click", function(event){
    socket.send("get_rooms|");
});

let responseActions = {
    "get_rooms" : updateRooms,
    "connect_to_room" : connect_to_room,
    "receive_message" : receive_message
};

socket.addEventListener("message", function(event) {
    let responseInfo = event.data.split("|");
    let method = responseActions[responseInfo[1]];
    method(responseInfo.slice(2));

});

function waitForConnection(socket) {
    return new Promise(function(resolve, reject) {
        let delay = 100;
        let maxAttempts = 100;
        let currAttempt = 0;
        let interval = setInterval(function() {
            if (currAttempt >= maxAttempts) {
                clearInterval(interval);
                reject("connection timed out");
            } else if (socket.readyState === socket.OPEN) {
                clearInterval(interval);
                resolve();
            }
            currAttempt += 1;
        }, delay);
    });
}

async function sendMessage(message) {
    try {
        if (socket.readyState !== socket.OPEN) {
            await waitForConnection(socket);
            socket.send(message);
        } else {
            socket.send(message);
        }
    } catch (err) {
        console.log(err);
    }
}

function updateRooms(roomInfo) {
    let rooms = {};
    for (let i = 0; i < roomInfo.length; i++) {
        let data = roomInfo[i].split(",");
        let rName = data[0];
        let rCapacity = data[1];
        rooms[rName] = rCapacity;
    }

    let box = document.getElementById("textBox");
    box.innerHTML = "";
    for (var name in rooms) {
        let capacity = rooms[name]
        let roomDiv = document.createElement("div");
        roomDiv.id = name;
        roomDiv.className = "roomBox"
        roomDiv.innerHTML += `
            <div style="float:left; margin-left:5px;">${name}</div>
            <div style="float:right; margin-right:5px;">${capacity}</dov>
        `

        roomDiv.addEventListener("click", async function(event) {
            console.log(`clicked ${event.target.id}`);
            document.getElementById("textBox").innerHTML = "";
            await sendMessage(`connect_to_room|${username}|${event.target.id}`);
            currentRoom = event.target.id;
        });

        box.append(roomDiv);
    }
}

function connect_to_room(connectedUsers) {
    // document.getElementById("textBox").innerHTML = "";
    document.getElementById("roomControls").style.display = "none";
    console.log(connectedUsers);
}

async function receive_message(messageData) {
    console.log(messageData)
        // await waitForConnection();
    document.getElementById("textBox").innerText += `${messageData[0]}: ${messageData[1]}\n`
        // document.getElementById("textBox").innerHTML += `${messageData[0]}: ${messageData[1]}\n`

}

let input = document.getElementById("msgInput");

input.addEventListener("keydown", function(event) {
    if (event.key == "Enter") {
        sendChatMessage();
    }
});

function sendChatMessage() {
    let box = document.getElementById("msgInput")
    socket.send(`send_message|${currentRoom}|${username}|${box.value}`);
    box.value = "";
}

function parse_reply() {

}

function execute_message(serverMsg) {

}

// document.getElementById("createRoom").addEventListener("click", function(event) {
//     let newBox = `
//         <div class="roomBox">
//             <div style="float:left; margin-left:5px;">Room</div>
//             <div style="float:right; margin-right:5px;">5</dov>
//         </div>
//     `;
//     document.getElementById("textBox").innerHTML += newBox;
// });