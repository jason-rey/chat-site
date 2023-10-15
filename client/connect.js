const socket = new WebSocket("ws://34.145.26.131:5473")
let username = localStorage.getItem("username");
let sessionID = localStorage.getItem("sessionID");

// let username = "testUser";
let connectionInfo = {
    "username": username,
    "sessionID": sessionID
};

socket.onopen = () => socket.send(JSON.stringify(connectionInfo));

let currentRoom = "";

const msg = {
    "action": "get_rooms",
    "args": {}
};
sendMessage(JSON.stringify(msg));

document.getElementById("createRoom").addEventListener("click", async function(event) {
    let roomName = document.getElementById("roomNameBox").value;
    let createRoomCommand = {
        "action": "create_room",
        "args": {
            "roomName": roomName,
            "username": username
        }
    };
    await sendMessage(JSON.stringify(createRoomCommand));

    document.getElementById("textBox").innerHTML = "";
    let connectCommand = {
        "action": "connect_to_room",
        "args": {
            "username": username,
            "roomName": roomName
        }
    };
    currentRoom = roomName;
    await sendMessage(JSON.stringify(connectCommand));
});

document.getElementById("disconnectButton").addEventListener("click", async function(event) {
    let dcMsg = {
        "action": "disconnect_from_room",
        "args": {
            "roomName": currentRoom,
            "username": username
        }
    };
    await sendMessage(JSON.stringify(dcMsg));

    event.target.style.display = "none";
    document.getElementById("roomControls").style = "";

    await sendMessage(JSON.stringify(msg));
});

let responseActions = {
    "get_rooms" : get_rooms,
    "connect_to_room" : connect_to_room,
    "receive_message" : receive_message
};

socket.addEventListener("message", function(event) {
    let responseInfo = JSON.parse(event.data);
    console.log(responseInfo);

    if (responseInfo.type != "") {
        let method = responseActions[responseInfo.type];
        method(responseInfo.data);
    }
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

function get_rooms(roomInfo) {
    let roomData = roomInfo.rooms.split("|");
    let rooms = {};
    for (let i = 0; i < roomData.length; i++) {
        let currRoomData = roomData[i].split(",");
        let roomName = currRoomData[0];
        let connectedCount = currRoomData[1];

        rooms[roomName] = connectedCount;
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
            document.getElementById("textBox").innerHTML = "";
            command = {
                "action": "connect_to_room",
                "args": {
                    "username": username,
                    "roomName": roomDiv.id
                }
            };

            await sendMessage(JSON.stringify(command));
            currentRoom = event.target.id;
        });

        box.append(roomDiv);
    }
}

async function connect_to_room(connectedUsers) {
    // document.getElementById("textBox").innerHTML = "";
    document.getElementById("roomControls").style.display = "none";
    document.getElementById("disconnectButton").style = "";
}

async function receive_message(messageData) {
        // await waitForConnection();
    document.getElementById("textBox").innerText += `${messageData.author}: ${messageData.message}\n`;
        // document.getElementById("textBox").innerHTML += `${messageData[0]}: ${messageData[1]}\n`

}

let input = document.getElementById("msgInput");

input.addEventListener("keydown", function(event) {
    if (event.key == "Enter") {
        sendChatMessage();
    }
});

async function sendChatMessage() {
    let box = document.getElementById("msgInput");

    messageCommand = {
        "action": "send_message",
        "args": {
            "roomName": currentRoom,
            "author": username,
            "message": box.value
        }
    };
    await sendMessage(JSON.stringify(messageCommand));
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