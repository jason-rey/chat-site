const socket = new WebSocket("ws://127.0.0.1:5050")
let username = localStorage.getItem("username");
let token = localStorage.getItem("token");

// let username = "testUser";
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
sendMessage(JSON.stringify(msg));

document.getElementById("createRoom").addEventListener("click", async function(event) {
    let roomName = document.getElementById("roomNameBox").value;
    let createRoomCommand = {
        "token": token,
        "action": "create_room",
        "args": {
            "roomName": roomName,
            "username": username
        }
    };
    await sendMessage(JSON.stringify(createRoomCommand));

    document.getElementById("textBox").innerHTML = "";
    let connectCommand = {
        "token": token,
        "action": "connect_to_room",
        "args": {
            "username": username,
            "roomName": roomName
        }
    };
    currentRoom = roomName;
    await sendMessage(JSON.stringify(connectCommand));
});

document.getElementById("refreshRooms").addEventListener("click", async function(event) {
    let command = {
        "token": token,
        "action": "get_rooms",
        "args": {}
    };
    await sendMessage(JSON.stringify(command));
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
    if (roomInfo.rooms === "") {
        return;
    }

    console.log(roomInfo);
    let box = document.getElementById("textBox");
    box.innerHTML = "";
    for (var name in roomInfo.rooms) {
        let capacity = roomInfo.rooms[name].connectedCount;
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
                "token": token,
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
        "token": token,
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