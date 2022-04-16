const socket = new WebSocket("ws://34.125.169.203:5050")

socket.addEventListener("message", function (event) {
    console.log(event.data)
    div = document.getElementById("textBox");
    div.innerHTML += `<p> ${event.data} </p>`
});

function connect_thing() {
    let msg = document.getElementById("msgBox").value;
    socket.send(msg);
}