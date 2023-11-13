# Chat Room
A chat room website built using Python and websockets
<br>
<br>
**Currently hosted on https://jason-rey.github.io/chat-site/**
<br>

## Dependencies
- [flask-authentication-server](https://github.com/jason-rey/flask-authentication-server) for handling user authentication

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Client Commands](#client-commands)
- [Server Messages](#server-messages)

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

## Client Commands
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
```

### Disconnect From Room
**Description:**
Disconnects a user to the given room

**Args**
- `username` (string, required): The user's name.
- `roomName` (string, required): The target room.

**Example:**
```javascript
const command = {
    "token": "user's token",
    "action": "disconnect_from_room",
    "args": {
        "username": "testUser",
        "roomName": "room one"
    }
};

socket.send(JSON.stringify(command));
```

### Create Room
**Description:**
Creates a new room

**Args**
- `username` (string, required): The user's name.
- `roomName` (string, required): The new room's name.

**Example:**
```javascript
const command = {
    "token": "user's token",
    "action": "create_room",
    "args": {
        "username": "testUser",
        "roomName": "room one"
    }
};

socket.send(JSON.stringify(command));
```

### Send Message
**Description:**
Sends a message to the given room

**Args**
- `roomName` (string, required): The target room
- `author` (string, required): The user's name.
- `message` (string, required): The message to be sent.

**Example:**
```javascript
const command = {
    "token": "user's token",
    "action": "send_message",
    "args": {
        "roomName": "room one",
        "author": "testUser",
        "message": "example message"
    }
};

socket.send(JSON.stringify(command));
```

## Server Messages

### Receive Message
**Description:**
A message sent from another connected user to the current user's room

**Example:**
```javascript
{
    "statusCode": "ok",
    "type": "receive_message",
    "data": {
        "author": "testUser",
        "message": "this is an example message"
    }
}
```

