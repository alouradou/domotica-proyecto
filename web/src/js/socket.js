const socket = new WebSocket("ws://localhost:8080", "websocket");

console.log("bonjour")
// // Listen for messages
// socket.addEventListener("message", (event) => {
//     console.log("Message from server ", event.data);
// });
//
// socket.addEventListener('message', event => {
//     console.log("Received socket")
//     const messageData = JSON.parse(event.data);
//     const messageContainer = document.getElementById('messageContainer');
//     const messageElement = document.createElement('div');
//     messageElement.textContent = messageData.message;
//     messageContainer.appendChild(messageElement);
// });

