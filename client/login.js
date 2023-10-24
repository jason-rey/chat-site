const URL = "http://127.0.0.1:5000/"

document.getElementById("registerBtn").addEventListener("click", async () => {
    const username = document.getElementById("usernameInput").value;
    const password = document.getElementById("passwordInput").value;
    let endpoint = URL + "register-user";
    let response = await fetch(
        endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        }
    );
    
    const outputBox = document.getElementById("outputText");
    let responseData = await response.json();
    if (response.status == 201) {
        outputBox.innerText = "Account creation successful";
    } else {
        outputBox.innerText = "Username exists, please use another";
    }    
});

document.getElementById("loginBtn").addEventListener("click", async () => {
    const username = document.getElementById("usernameInput").value;
    const password = document.getElementById("passwordInput").value;
    let endpoint = URL + "login-user";
    let response = await fetch(
        endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "username": username,
                "password": password
            })
        }
    );

    const outputBox = document.getElementById("outputText");
    let responseData = await response.json();
    if (response.status == 200) {
        outputBox.innerText = "Login successful";
        localStorage.setItem("username", username);
        localStorage.setItem("token", responseData["token"]);
        window.location.href = "chat_page.html";
    } else {
        outputBox.innerText = "Incorrect username and/or password";
    }    
});

