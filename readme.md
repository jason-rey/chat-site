# Chat Room
A chat room website built using Python and websockets
<br>
Uses [flask-authentication-server](https://github.com/jason-rey/flask-authentication-server) to handle user authentication
<br>
**Currently hosted on https://jason-rey.github.io/chat-site/**
<br>
## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)

## Installation
1. Create .env file with the required variables shown in config.py
2. Install requirements using pip
```bash
pip3 install -r requirements.txt
```

## Usage
To start the chat server, run start_server.py
```bash
python ./start_server.py
```
To connect with a client
```javascript
// Establish the websocket connection
const socket = new WebSocket("ws://SERVER_ADDRESS:SERVER_PORT")

// First message to the server must be the client's username
const connectionInfo = {
    "username": username,
};

socket.onopen = () => socket.send(JSON.stringify(connectionInfo));
```

## Commands
The server accepts commands in the following json format:
```javascript
{
    "token": "the user's token",
    "action": "the command to be executed",
    "args": {"arg1": "data"...} // nested json containing arguments of the desired command
}
```
Responses follow a similar format:
```javascript
{
    "statusCode": "The status of the response ('ok' or 'error')",
    "type": "The type of response",
    "data": {"field1": "data"...} // nested json containing response data
}
```

### Get Rooms
**Description:**
Gets all the current available rooms

**Example:**
```javascript
const command = {
    "token": "user's token",
    "action": "get_rooms",
    "args": {}
};

socket.send(JSON.stringify(command));
```

**Example Response:**
```javascript
{
    "statusCode": "ok",
    "type": "get_rooms",
    "data": {
        "rooms": { // the number beside the room name represents the number of connected users
            "room1": 0,
            "room two": 3
            ...
        }
    }
}
```

### Connect to Room
**Description:**
Connects a user to the given room

**Args**
- `username` (string, required): The user's name.
- `roomName` (string, required): The target room.

**Example:**
```javascript
const command = {
    "token": "user's token",
    "action": "connect_to_room",
    "args": {
        "username": "testUser",
        "roomName": "room one"
    }
};

socket.send(JSON.stringify(command));
```

**Example Response:**
```javascript
{
    "statusCode": "ok",
    "type": "connect_to_room",
    "data": {
            "roomName": "room one",
            "usernames": "[user1, otherUser, ...]" // an array containing the users currently connected to the room
        }
    }
}
```

