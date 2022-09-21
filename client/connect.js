const socket = new WebSocket("ws://34.125.85.254:5050")

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
    let box = document.getElementById("msgInput")
    socket.send(box.value);
    box.value = "";
}