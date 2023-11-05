const socket = new WebSocket("wss://chat-site-production-ed03.up.railway.app/")
let username = localStorage.getItem("username");
let token = localStorage.getItem("token");
console.log(token);
let connectionInfo = {
    "username": username,
    "token": token
};

socket.onopen = () => socket.send(JSON.stringify(connectionInfo));

let currentRoom = "";

const msg = {
    "token": token,
    "action": "get_rooms",
    "args": {}
};
sendCommandToServer(JSON.stringify(msg));

document.getElementById("createRoom").addEventListener("click", async function(event) {
    const nameBox = document.getElementById("roomNameBox");
    const roomName = nameBox.value
    nameBox.value = "";
    if (document.getElementById(roomName) != null) {
        alert("room with that name already exists");
        return;
    }

    let createRoomCommand = {
        "token": token,
        "action": "create_room",
        "args": {
            "roomName": roomName,
            "username": username
        }
    };

    await sendCommandToServer(JSON.stringify(createRoomCommand));

    document.getElementById("contentArea").innerHTML = "";
    let connectCommand = {
        "token": token,
        "action": "connect_to_room",
        "args": {
            "username": username,
            "roomName": roomName
        }
    };
    currentRoom = roomName;
    await sendCommandToServer(JSON.stringify(connectCommand));
});

document.getElementById("refreshRooms").addEventListener("click", async function(event) {
    let command = {
        "token": token,
        "action": "get_rooms",
        "args": {}
    };
    await sendCommandToServer(JSON.stringify(command));
});

document.getElementById("disconnectButton").addEventListener("click", async function(event) {
    let dcMsg = {
        "token": token,
        "action": "disconnect_from_room",
        "args": {
            "roomName": currentRoom,
            "username": username
        }
    };
    await sendCommandToServer(JSON.stringify(dcMsg));

    document.getElementById("msgInput").style.visibility = "hidden";
    event.target.style.display = "none";
    document.getElementById("roomControls").style = "";

    await sendCommandToServer(JSON.stringify(msg));
});

let responseActions = {
    "get_rooms" : get_rooms,
    "connect_to_room" : connect_to_room,
    "receive_message" : receive_message
};

function get_rooms(roomInfo) {
    if (roomInfo.rooms === "") {
        return;
    }

    console.log(roomInfo);
    let box = document.getElementById("contentArea");
    box.innerHTML = "";
    for (var name in roomInfo.rooms) {
        let capacity = roomInfo.rooms[name].connectedCount;
        let roomDiv = document.createElement("div");
        roomDiv.id = name;
        roomDiv.className = "roomBox";

        nameDiv = document.createElement("span");
        nameDiv.innerText += name;
        nameDiv.style.float = "left";

        capacityDiv = document.createElement("span");
        capacityDiv.innerText = capacity;
        capacityDiv.style.float = "right";

        roomDiv.appendChild(nameDiv);
        roomDiv.appendChild(capacityDiv);

        roomDiv.addEventListener("click", async function(event) {
            command = {
                "token": token,
                "action": "connect_to_room",
                "args": {
                    "username": username,
                    "roomName": roomDiv.id
                }
            };

            box.innerHTML = "";
            await sendCommandToServer(JSON.stringify(command));
        });

        box.append(roomDiv);
    }
}

async function connect_to_room(roomInfo) {
    currentRoom = roomInfo["roomName"];
    document.getElementById("roomControls").style.display = "none";
    document.getElementById("msgInput").style.visibility = "visible";
    document.getElementById("disconnectButton").style.display = "";
}

async function receive_message(messageData) {
    document.getElementById("contentArea").innerText += `${messageData.author}: ${messageData.message}\n`;
}

socket.addEventListener("message", function(event) {
    let responseInfo = JSON.parse(event.data);
    console.log(responseInfo);

    if (responseInfo.statusCode == "ok" && responseInfo.type != "") {
        let method = responseActions[responseInfo.type];
        method(responseInfo.data);
    } else if (responseInfo.statusCode == "error") {
        alert(responseInfo.data.message);
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

async function sendCommandToServer(message) {
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

let input = document.getElementById("msgInput");

input.addEventListener("keydown", function(event) {
    if (event.key == "Enter") {
        sendChatMessage();
    }
});

async function sendChatMessage() {
    let box = document.getElementById("msgInput");

    messageCommand = {
        "token": token,
        "action": "send_message",
        "args": {
            "roomName": currentRoom,
            "author": username,
            "message": box.value
        }
    };
    await sendCommandToServer(JSON.stringify(messageCommand));
    box.value = "";
}