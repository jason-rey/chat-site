const socket = new WebSocket("ws://34.145.26.131:5050")

// const KEY = "2197c9893de94f5fa2bc4373e7eb6886"
// socket.onopen = () => socket.send(KEY)

let nameBox = document.getElementById("usernameInput");
let passwordBox = document.getElementById("passwordInput");
let outputText = document.getElementById("outputText");
let displayLoginOutput = true;

socket.addEventListener("message", function(event) {
    let response = event.data.split("|");
    let statusCode = response[0];
    console.log(statusCode);
    let data = response[1];

    if (displayLoginOutput) {
        if (statusCode == 1) {
            outputText.innerHTML = "login successful";
            localStorage.setItem("username", nameBox.value);
            localStorage.setItem("sessionID", data);
            window.location.href = "chat_page.html";
            socket.close();
        } else if (statusCode == 0) {
            outputText.innerHTML = "incorrect username / password";
        }
    } else {
        if (statusCode == 1) {
            outputText.innerHTML = "registration successful";
        } else if (statusCode == 0) {
            outputText.innerHTML = "username taken";
        }
    }
});

document.getElementById("registerBtn").addEventListener("click", function(event) {
    let username = nameBox.value;
    let password = passwordBox.value;
    if (username == "" || password == "") {
        outputText.innerHTML = "username / password cannot be blank";
    } else {
        socket.send(`reg|${username}|${password}`);
        displayLoginOutput = false;
    }
})

document.getElementById("loginBtn").addEventListener("click", function(event) {
    let username = nameBox.value;
    let password = passwordBox.value;
    
    socket.send(`auth|${username}|${password}`);
    displayLoginOutput = true;
});
