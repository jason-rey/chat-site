const socket = new WebSocket("ws://26.146.230.220:5050")

socket.addEventListener("message", function(event) {
    console.log(event.data)
    div = document.getElementById("textBox");
    div.innerHTML += `
    <span class="message"> ${event.data} </span>
    <br>
    `
    let textBox = document.getElementById("textBox");
    textBox.scrollTop = textBox.scrollHeight;
});

let input = document.getElementById("msgInput");

input.addEventListener("keydown", function(event) {
    if (event.key == "Enter") {
        console.log("wh");
        send_message();
    }
});

function send_message() {
    let msg = document.getElementById("msgInput").value;
    socket.send(msg);
}