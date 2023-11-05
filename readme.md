# Chat-Room Server
A chat room server built using Python and websockets
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
